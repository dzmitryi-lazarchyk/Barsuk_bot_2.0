import sqlite3



def logger(statement):
    print(f"""_____________
Executing:
{statement}
_______________""")

class Database():
    # def __init__(self, path_to_db="sqlite.db"):
    #     self.path_to_db = path_to_db

    # @property
    # def connection(self):
    #     return sqlite3.connect(self.path_to_db)

    path_to_db = "sqlite.db"
    connection=sqlite3.connect(path_to_db)
    table = None

    # ************Database******************
    @classmethod
    async def execute(cls, sql:str, parameters:tuple=tuple(),
                fetchone=False, fetchall=False, commit=False):
        connection= cls.connection
        connection.set_trace_callback(logger)
        cursor=connection.cursor()
        data=None

        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchone:
            data=cursor.fetchone()
        if fetchall:
            data=cursor.fetchall()
        return data

    @classmethod
    async def create_tables(cls):
        sql=[]

        users_table_sql="""
        CREATE TABLE IF NOT EXISTS Users(
        id int NOT NULL,
        Name varchar(255) NOT NULL,
        PRIMARY KEY(id)
        );"""

        taps_table_sql = """
        CREATE TABLE IF NOT EXISTS Taps(
        tap int NOT NULL,
        Name varchar(255) NOT NULL,
        brewery varchar(255) NOT NULL,
        link varchar(255) NOT NULL,
        image varchar(255) NOT NULL,
        sort varchar(255) NOT NULL,
        price_list varchar(255) NOT NULL,
        PRIMARY KEY(tap)
        );"""

        jars_table_sql = """
        CREATE TABLE IF NOT EXISTS Jars(
        Name varchar(255) NOT NULL,
        brewery varchar(255) NOT NULL,
        link varchar(255) NOT NULL,
        image varchar(255) NOT NULL,
        sort varchar(255) NOT NULL,
        price_list varchar(255) NOT NULL,
        PRIMARY KEY(Name)
        );"""

        sql.append(users_table_sql)
        sql.append(taps_table_sql)
        sql.append(jars_table_sql)

        for command in sql:
            await cls.execute(command, commit=True)

    @staticmethod
    def format_args(sql, parameters:dict):
        sql+=" AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

#     **************************Children**************************


    @classmethod
    async def get(cls, **kwargs):
        sql = f"SELECT * FROM {cls.table} WHERE "
        sql, parameters = cls.format_args(sql, kwargs)
        args = await cls.execute(sql, parameters=parameters, fetchone=True)
        if args:
            return User(*args)
        else:
            return None



    @classmethod
    async def delete(cls, **kwargs):
        sql = f"DELETE FROM {cls.table} WHERE "
        sql, parameters = cls.format_args(sql, kwargs)
        await cls.execute(sql, parameters=parameters, commit=True)

class User(Database):

    table="Users"

    def __init__(self, id:int=None, name:str=None):
        super().__init__()
        self.id = id
        self.name = name

    @classmethod
    async def add(cls, **kwargs):
        sql = f"INSERT INTO {cls.table}(id, Name) VALUES(?, ?)"
        parameters = tuple(kwargs.values())
        print(sql)
        await cls.execute(sql, parameters=parameters, commit=True)

    @classmethod
    async def get_all(cls, **kwargs):
        sql = f"SELECT * FROM {cls.table} "
        args = await cls.execute(sql, fetchall=True)
        objects = []
        for i in args:
            objects.append(User(*i))
        return objects

    @classmethod
    async def get_several(cls, **kwargs):
        sql = f"SELECT * FROM {cls.table} WHERE "
        sql, parameters = cls.format_args(sql, kwargs)
        args = await cls.execute(sql, parameters=parameters, fetchall=True)
        if args:
            return Tap(*args)
        else:
            return None

class Tap(Database):
    table = "Taps"

    def __init__(self, tap: int=None, name: str=None,brewery:str=None, link: str=None,
                 image: str=None, sort: str=None, price_list: str=None):
        self.tap = tap
        self.name = name
        self.brewery = brewery
        self.link = link
        self.image = image
        self.sort = sort
        self.price_list = price_list

    def __str__(self):
        return f"{self.tap}. {self.name}:{self.brewery}"

    @classmethod
    async def add(cls, beer):
        sql = f"INSERT INTO {cls.table}(tap, Name, brewery, link, image,sort,price_list) VALUES(?, ?, ?, ?, ?, ?, ?)"
        parameters = beer.tap, beer.name, beer.brewery, beer.link,\
                     beer.image, beer.sort, beer.price_list
        await cls.execute(sql, parameters=parameters, commit=True)

    @classmethod
    async def get_all(cls):
        sql = f"SELECT * FROM {cls.table} "
        args = await cls.execute(sql, fetchall=True)
        objects = []
        for i in args:
            objects.append(Tap(*i))
        return objects

    @classmethod
    async def get(cls, **kwargs):
        sql = f"SELECT * FROM {cls.table} WHERE "
        sql, parameters = cls.format_args(sql, kwargs)
        args = await cls.execute(sql, parameters=parameters, fetchone=True)
        if args:
            return Tap(*args)
        else:
            return None

    @classmethod
    async def get_several(cls, **kwargs):
        sql = f"SELECT * FROM {cls.table} WHERE "
        sql, parameters = cls.format_args(sql, kwargs)
        args = await cls.execute(sql, parameters=parameters, fetchall=True)
        if args:
            return Tap(*args)
        else:
            return None

class Jar(Database):
    table = "Jars"

    def __init__(self, name: str=None,brewery:str=None, link: str=None,
                 image: str=None, sort: str=None, price_list: str=None):
        self.name = name
        self.brewery = brewery
        self.link = link
        self.image = image
        self.sort = sort
        self.price_list = price_list

    def __str__(self):
        return f"{self.name}:{self.brewery}"

    @classmethod
    async def add(cls, beer):
        sql = f"INSERT INTO {cls.table}(Name, brewery, link, image,sort,price_list) VALUES(?, ?, ?, ?, ?, ?)"
        parameters = beer.name, beer.brewery, beer.link, \
                     beer.image, beer.sort, beer.price_list
        await cls.execute(sql, parameters=parameters, commit=True)

    @classmethod
    async def get_all(cls):
        sql = f"SELECT * FROM {cls.table} "
        args = await cls.execute(sql, fetchall=True)
        objects = []
        for i in args:
            objects.append(Jar(*i))
        return objects

    @classmethod
    async def get(cls, **kwargs):
        sql = f"SELECT * FROM {cls.table} WHERE "
        sql, parameters = cls.format_args(sql, kwargs)
        args = await cls.execute(sql, parameters=parameters, fetchone=True)
        if args:
            return Jar(*args)
        else:
            return None

    @classmethod
    async def get_several(cls, **kwargs):
        sql = f"SELECT * FROM {cls.table} WHERE "
        sql, parameters = cls.format_args(sql, kwargs)
        args = await cls.execute(sql, parameters=parameters, fetchall=True)
        jars=[]
        if args:
            for i in args:
                jars.append(Jar(*i))
            return jars
        # else:
        #     return None


    @classmethod
    async def get_column(cls, column:str="*"):
        sql = f"SELECT \"{column.strip()}\" FROM {cls.table} "
        args = await cls.execute(sql, fetchall=True)
        res = set()
        for i in args:
            res.add(i[0])
        return res

    @classmethod
    async def get_by_sort(cls, sort: str = "*"):
        sql = f"SELECT * FROM {cls.table} WHERE \"sort\" LIKE '%{sort}%'"
        args = await cls.execute(sql, fetchall=True)
        beers = []
        if args:
            for i in args:
                beers.append(Jar(*i))
            return beers

