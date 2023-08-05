# encoding: utf-8

import os
import MySQLdb
import ConfigParser
import pandas as pd

from config.file import FILE
from config.sql  import SQL
from sqlalchemy  import create_engine


class DB_SQL(object):


    def __init__(self, f):
        self.__restart__(f)


    def __config__(self, f):
        # config
        cfg  = ConfigParser.SafeConfigParser()

        # path = os.path.split(os.path.realpath(__file__))[0]

        # print path
        # print os.getcwd()

        # cfg.read(os.path.join(path, FILE.FILE))

        cfg.read(f)

        # config args
        self.user     = cfg.get(SQL.MYSQL   , SQL.MYSQL_USER)
        self.password = cfg.get(SQL.MYSQL   , SQL.MYSQL_PASSWORD)
        self.host     = cfg.get(SQL.MYSQL   , SQL.MYSQL_HOST)
        self.port     = cfg.getint(SQL.MYSQL, SQL.MYSQL_PORT)
        self.db       = cfg.get(SQL.MYSQL   , SQL.MYSQL_DB)


    def connection1(self):
        conn_url       = 'mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
                             self.user,
                             self.password,
                             self.host,
                             self.port,
                             self.db
                         )   
        self.conn1 = create_engine(conn_url)


    def connection2(self):
        db = MySQLdb.connect(host   = self.host,
                             user   = self.user,
                             passwd = self.password,
                             db     = self.db,
                             port   = self.port)

        self.conn2 = db.cursor()


    def __refresh__(self):
        self.connection1()
        self.connection2()


    def __restart__(self, f):
        self.__config__(f)
        self.__refresh__()


    def select(self, query):

        self.__refresh__()

        self.conn2.execute(query)
        return self.conn2.fetchall()


    def select_pdf(self, query_or_table, index_col=None, parse_dates=None, columns=None):

        self.__refresh__()

        return pd.read_sql(query_or_table,
                           self.conn1,
                           index_col   = index_col,
                           parse_dates = parse_dates,
                           columns     = columns)


    def update(self):
        pass


    def save_pdf(self, df, table, schema=None, mode='fail', index=False, index_label=None, chunksize=None):
        """ Save Pandas DataFrame
        """

        self.__refresh__()

        df.to_sql(table, self.conn1,
                  dtype       = schema,
                  if_exists   = mode,
                  index       = index,
                  index_label = index_label,
                  chunksize   = chunksize)
