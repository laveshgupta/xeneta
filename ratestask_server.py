from config import Config
from constants import Constants
from logger import Logger
from db_connection_pool import DBConnectionPool
from flask import Flask
from flask import request as frequest
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
            rates_between_ports()


        @self.app.route('/rates_ports/')
        def rates_between_ports():
            date_from, date_to, origin, destination = rsh.common_api_functionality()
            logger.debug(f"------ INSIDE RATES date_from: {date_from}  date_to: {date_to}  origin: {origin} destination: {destination}")
            is_origin_code, is_origin_region = rsh.code_or_region_slug(origin)
            Logger.get_instance().debug(f"is_origin_code: {is_origin_code}    is_origin_region: {is_origin_region}")
            if not is_origin_code and not is_origin_region:
                return rsh.create_response(
                    res_body=f"Request cannot be processed as origin parameter: {origin} is neither port code or region slug",
                    res_code=400
                )

            is_dest_code, is_dest_region = rsh.code_or_region_slug(destination)
            Logger.get_instance().debug(f"is_dest_code: {is_dest_code}    is_dest_region: {is_dest_region}")
            if not is_dest_code and not is_dest_region:
                return rsh.create_response(
                    res_body=f"Request cannot be processed as destination parameter: {destination} is neither port code or region slug",
                    res_code=400
                )

            orig_codes = [origin]
            dest_codes = [destination]

            if is_origin_region:
                orig_codes = rsh.get_port_code_for_region(region=origin)

            if is_dest_region:
                dest_codes = rsh.get_port_code_for_region(region=destination)

            if not orig_codes:
                return rsh.create_response(
                    res_body=f"Request cannot be processed as no port code exists for specified origin region: {origin}",
                    res_code=400
                )

            if not dest_codes:
                return rsh.create_response(
                    res_body=f"Request cannot be processed as no port code exists for specified destination region: {destination}",
                    res_code=400
                )

            rates_list = rsh.get_rate_list(date_from=date_from, date_to=date_to, orig_codes=orig_codes, dest_codes=dest_codes)

            return rsh.create_response(rates_list, 200)


if __name__ == '__main__':
    config = Config()
    print(f"config: {config}")
    __builtins__.config = config
    print(f"config: {config}")
    logger = Logger()
    __builtins__.logger = logger
    print(Constants.APP_CONFIG_FILE_PATH)
    db_conn_pool = DBConnectionPool()
    print(f"{db_conn_pool}")
    print(f"{DBConnectionPool.get_instance()}")
    __builtins__.db_conn_pool = db_conn_pool
    rts = RatesTaskServer()
    rts.server_run()