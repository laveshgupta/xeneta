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
        flask_config = config.get('flask', {})
        flask_host = flask_config.get('host', Constants.APP_HOST)
        flask_port = flask_config.get('port', Constants.APP_PORT)
        self.app.run(
            host=flask_host,
            port=flask_port,
            debug=True
        )


    def create_routes(self):
        @self.app.route('/rates/')
        def rates():
            date_from, date_to, origin_port_codes, dest_port_codes = rsh.common_api_functionality()
            rates_list = rsh.get_rate_list(
                            date_from=date_from,
                            date_to=date_to,
                            origin_port_codes=origin_port_codes,
                            dest_port_codes=dest_port_codes
                        )
            return rsh.create_response(rates_list, 200)


        @self.app.route('/rates_ports/')
        def rates_between_ports():
            date_from, date_to, origin_port_codes, dest_port_codes = rsh.common_api_functionality()
            rates_list_between_ports = rsh.get_rate_list_between_ports(
                                            date_from=date_from,
                                            date_to=date_to,
                                            origin_port_codes=origin_port_codes,
                                            dest_port_codes=dest_port_codes
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