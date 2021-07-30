import psycopg2
from psycopg2 import pool
from constants import Constants

class DBConnectionPool:
    __instance = None

    @staticmethod
    def get_instance():
        if DBConnectionPool.__instance == None:
            DBConnectionPool()
        return DBConnectionPool.__instance


    def __init__(self):
        if DBConnectionPool.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.__create_db_pool()
            DBConnectionPool.__instance = self


    def __create_db_pool(self):
        logger.info('Creating DB Connection Pool.')
        db_config = config.get('db', {})
        db_min_conn = db_config.get('min_conn', Constants.DEFAULT_DB_MIN_CONN)
        db_max_conn = db_config.get('max_conn', Constants.DEFAULT_DB_MAX_CONN)
        db_host = db_config.get('host', Constants.DEFAULT_DB_HOST)
        db_port = db_config.get('port', Constants.DEFAULT_DB_PORT)
        db_database = db_config.get('database', Constants.DEFAULT_DB_DATABASE)
        db_user = db_config.get('user', Constants.DEFAULT_DB_USER)
        db_password = db_config.get('password', Constants.DEFAULT_DB_PASSWORD)
        try:
            self.__db_conn_pool = pool.ThreadedConnectionPool(
                minconn=db_min_conn,
                maxconn=db_max_conn,
                host=db_host,
                port=db_port,
                dbname=db_database,
                user=db_user,
                password=db_password
            )
            logger.info('Successfully created DB Connection pool.')
        except Exception as e:
            logger.exception('Error in creating database connection pool. Exiting.')
            raise e


    def execute_query(self, query:str, params:dict):
        db_conn = cursor = None
        try:
            logger.debug(f"Executing query: {query}  with params: {params}")
            db_conn = self.__db_conn_pool.getconn()
            cursor = db_conn.cursor()
            # cursor.execute(query.format(**params))
            logger.debug(f"Getting SQL equivalent query: {cursor.mogrify(query, params)}")
            cursor.execute(query, params)
            rows = cursor.fetchall()
            logger.debug("Query executed")
            cursor.close()
            self.__db_conn_pool.putconn(db_conn)
            db_conn = cursor = None
            return rows
        except Exception as e:
            logger.exception(f"Error in executing query: {query}. Traceback: {e} ")
            raise e
        finally:
            if cursor:
                cursor.close()
            if db_conn:
                self.__db_conn_pool.putconn(db_conn)
