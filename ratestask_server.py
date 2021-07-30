from flask.wrappers import Response
from config import Config
from constants import Constants
from logger import Logger
from db_connection_pool import DBConnectionPool
from flask import Flask
from ratestask_helper import RatestaskHelper as rsh


class RatesTaskServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.create_routes()


    def server_run(self):
        """
        Starting flask server
        """
        flask_config = config.get('flask', {})
        flask_host = flask_config.get('host', Constants.APP_HOST)
        flask_port = flask_config.get('port', Constants.APP_PORT)
        self.app.run(
            host=flask_host,
            port=flask_port,
            debug=True
        )


    def create_routes(self):
        """
        Create routes in application
        """
        @self.app.route('/rates/')
        def rates():
            """
            Create route rates which calculates average price between origin and destination for a day
            """
            rates_params = rsh.common_api_functionality()
            if isinstance(rates_params, Response):
                return rates_params
            rates_list = rsh.get_rate_list(
                            date_from=rates_params['date_from'],
                            date_to=rates_params['date_to'],
                            origin_port_codes=rates_params['origin_port_codes'],
                            dest_port_codes=rates_params['dest_port_codes']
                        )
            return rsh.create_response(rates_list, 200)


        @self.app.route('/rates_ports/')
        def rates_between_ports():
            """
            Create route rates_ports which calculates average price between ports for a day.
            """
            rates_params = rsh.common_api_functionality()
            if isinstance(rates_params, Response):
                return rates_params
            rates_list_between_ports = rsh.get_rate_list_between_ports(
                                            date_from=rates_params['date_from'],
                                            date_to=rates_params['date_to'],
                                            origin_port_codes=rates_params['origin_port_codes'],
                                            dest_port_codes=rates_params['dest_port_codes']
                                        )

            return rsh.create_response(rates_list_between_ports, 200)


if __name__ == '__main__':
    config = Config()
    __builtins__.config = config
    logger = Logger()
    __builtins__.logger = logger
    db_conn_pool = DBConnectionPool()
    __builtins__.db_conn_pool = db_conn_pool
    rts = RatesTaskServer()
    rts.server_run()