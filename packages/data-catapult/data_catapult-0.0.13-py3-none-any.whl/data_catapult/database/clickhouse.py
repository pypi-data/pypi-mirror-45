import clickhouse_driver
from clickhouse_driver.errors import ErrorCodes


class ClickhouseDriver(object):
    def __init__(self, **kwargs):
        self.host = kwargs.get("host", "localhost")
        self.port = int(kwargs.get("port", 9000))
        self.database = kwargs.get("database", "default")
        self.user = kwargs.get("user", "default")
        self.password = kwargs.get("password", "")

    def get_data(self, df, dtypes, has_header=True):
        return list(df.values)

    def derive_kind(self, d, nullable=True, if_exists="fail"):
        d = str(d)
        if d in ['real', 'float', 'float64', 'real64']:
            return "Nullable(Float32)" if nullable else "Float32"
        elif d in ['int', 'int64']:
            return "Nullable(Int64)" if nullable else "Int64"
        return "Nullable(String)" if nullable else "String"

    def to_sql(self, source_df, name, if_exists="fail", nullable_list=None, pk=None, dtype=None):
        # print source, type(source)
        # header_df = pd.read_csv(source, nrows=50000)
        columns = source_df.columns
        kinds = zip(columns, [self.derive_kind(d, nullable=columns[idx] in nullable_list if nullable_list else False) for idx, d in enumerate(source_df.dtypes)])
        kinds = ['"{}" {}'.format(c, k) for c, k in kinds]
        table_name = name
        if not pk:
            raise ValueError("At this time, you Must specify primary key for MergeTree Engine! Pass a list of column names as arguments, e.g. pk=['col1', 'col2']")
        engine = "MergeTree() ORDER BY ({})".format(",".join(pk))
        create_table_sql = '''CREATE TABLE {} ({}) ENGINE = {}'''.format(table_name, ",".join(kinds), engine)
        client = clickhouse_driver.Client(host=self.host, port=self.port,
                                          database=self.database, user=self.user,
                                          password=self.password)
        try:
            client.execute(create_table_sql)
        except clickhouse_driver.errors.ServerException as err:
            if if_exists == "fail":
                print("Error when trying to create table. table already exists?")
                raise ValueError("Mode is set to fail and table already exists")
            elif if_exists == "append":
                if err.code == ErrorCodes.TABLE_ALREADY_EXISTS:
                    pass # Allow the program to continue
                else:
                    raise RuntimeError("Could not import table!", str(err))
        # -- using list for now, but eventually use generator to stream inserts
            elif if_exists == "drop":
                 print("** ALERT! Droppping table ", table_name)
                 drop_table_sql = 'DROP TABLE {};'.format(table_name)
                 client.execute(drop_table_sql)
                 client.execute(create_table_sql)
            else:
                raise ValueError(if_exists, "bad value for if_exists")
        data = self.get_data(source_df, source_df.dtypes.values)
        # source_df.seek(0)
        my_sql_str = "INSERT INTO {} FORMAT CSV".format(table_name)
        client.execute(my_sql_str, data)
        client.disconnect()
        # return source

