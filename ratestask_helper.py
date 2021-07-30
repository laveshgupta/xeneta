import json
import datetime
from flask import current_app
from flask import request as frequest
from constants import Constants


class RatestaskHelper:

    @staticmethod
    def execute_query(query: str, params: dict):
        """
        Helper function to execute query
        """
        return db_conn_pool.execute_query(query=query, params=params)


    @staticmethod
    def create_response(res_body: str, res_code: int=200):
        """
        Function to create response for request
        """
        output = res_body
        mime_type = 'text/plain'
        separators = (", ", ": ")
        try: #if json dumps is successful then mimetype is changed to json.
            output = json.dumps(res_body, indent=4, separators=separators)
            mime_type = 'application/json'
        except Exception as e:
            logger.warning("Error in json dumps. Hence creating message as plain text.")
        return current_app.response_class(
            response=output,
            status=res_code,
            mimetype=mime_type
        )


    @staticmethod
    def validate_date(date_text: str):
        """
        Function which validate date against input date format
        """
        date_correct = True
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            date_correct = False
        return date_correct


    @staticmethod
    def is_port_code(port_code:str):
        """
        Function to find whether the origin or destination is port
        """
        query = """SELECT COUNT(*) from ports po where po.code=%(port_code)s"""
        params = {'port_code': port_code}

        rows = RatestaskHelper.execute_query(query=query, params=params)
        count = 0
        if rows:
            count = rows[0][0]
        if count:
            return True
        return False


    @staticmethod
    def is_region_slug(region_slug:str):
        """
        Function to find whether the origin or destination is region
        """
        query = "SELECT COUNT(*) from regions re where re.slug=%(region_slug)s"
        params = {'region_slug': region_slug}

        rows = RatestaskHelper.execute_query(query=query, params=params)
        count = 0
        if rows:
            count = rows[0][0]
        if count:
            return True
        return False


    @staticmethod
    def port_or_region(text:str):
        """
        Function to find whether the origin or destination is port or region
        """
        port_region_code = Constants.PORT_REGION_CODE['none']
        if len(text) == 5:
            if RatestaskHelper.is_port_code(text):
                port_region_code = Constants.PORT_REGION_CODE['port']
        if not port_region_code:
            if RatestaskHelper.is_region_slug(text):
                port_region_code = Constants.PORT_REGION_CODE['region']
        return port_region_code


    @staticmethod
    def get_rate_list(date_from, date_to, origin_port_codes, dest_port_codes):
        """
        Function to get average price between origin and destination for a particular day. This takes into account
        ports for a region
        """
        query = """
            SELECT p.day, COUNT(p.price), case when COUNT(p.price) > 2 THEN AVG(p.price) ELSE null END AS Average
            FROM prices p
            WHERE p.orig_code = ANY(%(origin_port_codes)s) AND p.dest_code = ANY(%(dest_port_codes)s) AND p.day >= %(date_from)s AND p.day <= %(date_to)s
            GROUP BY p.day
            ORDER BY p.day;
        """
        params = {
            'origin_port_codes': origin_port_codes,
            'dest_port_codes': dest_port_codes,
            'date_from': date_from,
            'date_to': date_to
        }

        rows = RatestaskHelper.execute_query(query=query, params=params)
        rate_list = []
        for row in rows:
            rate_list.append({
                'day': row[0].strftime('%Y-%m-%d'),
                'average_price': int(row[2]) if row[2] else row[2]
            })
        return rate_list


    @staticmethod
    def get_rate_list_between_ports(date_from, date_to, origin_port_codes, dest_port_codes):
        """
        Function to get average price between port codes beloning to origin and destination for a particular day. This takes into account
        ports for a region
        """
        # query = """
        #     SELECT p.orig_code, p.dest_code, p.day, COUNT(p.price), case when COUNT(p.price) > 2 THEN AVG(p.price) ELSE null END AS Average
        #     FROM prices p
        #     WHERE p.orig_code IN {orig_codes} AND p.dest_code IN {dest_codes} AND p.day >= {date_from} AND p.day <= {date_to}
        #     GROUP BY p.orig_code, p.dest_code, p.day
        #     ORDER BY p.day;
        # """
        query = """
            SELECT p.orig_code, p.dest_code, p.day, COUNT(p.price), case when COUNT(p.price) > 2 THEN AVG(p.price) ELSE null END AS Average
            FROM prices p
            WHERE p.orig_code = ANY(%(origin_port_codes)s) AND p.dest_code = ANY(%(dest_port_codes)s) AND p.day >= %(date_from)s AND p.day <= %(date_to)s
            GROUP BY p.orig_code, p.dest_code, p.day
            ORDER BY p.day;
        """
        params = {
            'origin_port_codes': origin_port_codes,
            'dest_port_codes': dest_port_codes,
            'date_from': date_from,
            'date_to': date_to
        }

        rows = RatestaskHelper.execute_query(query=query, params=params)
        rate_list = []
        for row in rows:
            rate_list.append({
                'origin': row[0],
                'destination': row[1],
                'day': row[2].strftime('%Y-%m-%d'),
                'average_price': int(row[4]) if row[4] else row[4]
            })
        return rate_list


    @staticmethod
    def get_child_region_for_region(region):
        """
        Function which returns all child region for a particular region
        """
        query = """
            WITH RECURSIVE region_tree(slug, parent_slug)
            AS (SELECT slug, parent_slug FROM regions where slug=%(region)s
                UNION ALL
                SELECT r.slug, r.parent_slug FROM regions r, region_tree rt where r.parent_slug = rt.slug)
            SELECT rt.slug as region, rt.parent_slug As parent_region from region_tree rt ORDER By rt.parent_slug;
        """
        params = {'region': region}
        rows = RatestaskHelper.execute_query(query=query, params=params)
        all_regions = []
        for row in rows:
            all_regions.append(row[0])
        return all_regions


    @staticmethod
    def get_port_codes_for_region(region):
        """
        Function which returns port code for regions
        """
        all_regions = RatestaskHelper.get_child_region_for_region(region=region)
        query = """
            SELECT p.code
            FROM ports p
            WHERE parent_slug = ANY(%(all_regions)s)
        """
        params = {'all_regions': all_regions}
        rows = RatestaskHelper.execute_query(query=query, params=params)
        port_codes = []
        for row in rows:
            port_codes.append(row[0])
        return port_codes


    @staticmethod
    def common_api_functionality():
        """
        Function implementing common functionality for both api.
        It validates the input.
        Returns port codes for origin and destination
        """

        #Validates if fields are present in request
        date_from = frequest.args.get('date_from', type=str)
        date_to = frequest.args.get('date_to', type=str)
        origin = frequest.args.get('origin', type=str)
        destination = frequest.args.get('destination', type=str)
        logger.debug(f"------ INSIDE RATES date_from: {date_from}  date_to: {date_to}  origin: {origin} destination: {destination}")
        parameters_not_present = []
        if not date_from:
            parameters_not_present.append('date_from')
        if not date_to:
            parameters_not_present.append('date_to')
        if not origin:
            parameters_not_present.append('origin')
        if not destination:
            parameters_not_present.append('destination')
        if parameters_not_present:
            return RatestaskHelper.create_response(
                res_body=f"Request cannot be processed as these parameters {parameters_not_present} are not passed",
                res_code=400
            )

        #Validates date passed in request
        dates_not_correct = []
        if not RatestaskHelper.validate_date(date_text=date_from):
            dates_not_correct.append('date_from')
        if not RatestaskHelper.validate_date(date_text=date_to):
            dates_not_correct.append('date_to')
        if dates_not_correct:
            return RatestaskHelper.create_response(
                res_body=f"Request cannot be processed as these dates {dates_not_correct} are not correct",
                res_code=400
            )

        #Find whether origin is port code or region. If it none then HTTP 400 error is reported
        origin_port_or_region = RatestaskHelper.port_or_region(origin)
        logger.debug(f"origin_port_or_region: {origin_port_or_region}")
        if origin_port_or_region == Constants.PORT_REGION_CODE['none']:
            return RatestaskHelper.create_response(
                res_body=f"Request cannot be processed as origin parameter: {origin} is neither port code or region slug",
                res_code=400
            )

        #Find whether destination is port code or region. If it none then HTTP 400 error is reported
        dest_port_or_region = RatestaskHelper.port_or_region(destination)
        logger.debug(f"dest_port_or_region: {dest_port_or_region}")
        if dest_port_or_region == Constants.PORT_REGION_CODE['none']:
            return RatestaskHelper.create_response(
                res_body=f"Request cannot be processed as destination parameter: {destination} is neither port code or region slug",
                res_code=400
            )

        origin_port_codes = [origin]
        dest_port_codes = [destination]

        #Getting port codes if origin is region
        if origin_port_or_region == Constants.PORT_REGION_CODE['region']:
            origin_port_codes = RatestaskHelper.get_port_codes_for_region(region=origin)

        #Getting port codes if destination is region
        if dest_port_or_region == Constants.PORT_REGION_CODE['region']:
            dest_port_codes = RatestaskHelper.get_port_codes_for_region(region=destination)

        if not origin_port_codes:
            return RatestaskHelper.create_response(
                res_body=f"Request cannot be processed as no port code exists for specified origin region: {origin}",
                res_code=400
            )

        if not dest_port_codes:
            return RatestaskHelper.create_response(
                res_body=f"Request cannot be processed as no port code exists for specified destination region: {destination}",
                res_code=400
            )

        return {
            'date_from': date_from,
            'date_to': date_to,
            'origin_port_codes': origin_port_codes,
            'dest_port_codes': dest_port_codes
        }