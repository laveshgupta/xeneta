import json
import datetime
from flask import current_app
import traceback


class RatestaskHelper:

    @staticmethod
    def execute_query(query:str, params:dict):
        return db_conn_pool.execute_query(query=query, params=params)


    @staticmethod
    def create_response(res_body:str, res_code:int):
        output = res_body
        mime_type = 'text/plain'
        separators = (", ", ": ")
        try:
            output = json.dumps(res_body, indent=4, separators=separators)
            mime_type = 'application/json'
        except Exception as e:
            logger.warning("Error in json dumps")
            print(traceback.print_exc(e))
        return current_app.response_class(
            response=output,
            status=res_code,
            mimetype=mime_type
        )


    @staticmethod
    def validate_date(date_text):
        date_correct = True
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            date_correct = False
        return date_correct


    @staticmethod
    def is_port_code(code:str):
        # query = "SELECT COUNT(*) from ports po where po.code='{code}'"
        query = """SELECT COUNT(*) from ports po where po.code=%(code)s"""
        params = {'code': code}

        rows = RatestaskHelper.execute_query(query=query, params=params)
        print(f"rows: {rows}")
        count = rows[0][0]
        if count:
            return True
        return False


    @staticmethod
    def is_region_slug(region_slug:str):
        # query = "SELECT COUNT(*) from regions re where re.slug='{region_slug}'"
        query = "SELECT COUNT(*) from regions re where re.slug=%(region_slug)s"
        params = {'region_slug': region_slug}
        rows = RatestaskHelper.execute_query(query=query, params=params)
        count = rows[0][0]
        if count:
            return True
        return False


    @staticmethod
    def code_or_region_slug(text:str):
        is_code = is_region = False
        if len(text) == 5:
            is_code = RatestaskHelper.is_port_code(text)
        if not is_code:
            is_region = RatestaskHelper.is_region_slug(text)
        return is_code, is_region


    @staticmethod
    def get_rate_list(date_from, date_to, orig_codes, dest_codes):
        query = """
            SELECT p.orig_code, p.dest_code, p.day, COUNT(p.price), case when COUNT(p.price) > 2 THEN AVG(p.price) ELSE null END AS Average
            FROM prices p
            WHERE p.orig_code IN {orig_codes} AND p.dest_code IN {dest_codes} AND p.day >= {date_from} AND p.day <= {date_to}
            GROUP BY p.orig_code, p.dest_code, p.day
            ORDER BY p.day;
        """
        query = """
            SELECT p.orig_code, p.dest_code, p.day, COUNT(p.price), case when COUNT(p.price) > 2 THEN AVG(p.price) ELSE null END AS Average
            FROM prices p
            WHERE p.orig_code = ANY(%(orig_codes)s) AND p.dest_code = ANY(%(dest_codes)s) AND p.day >= %(date_from)s AND p.day <= %(date_to)s
            GROUP BY p.orig_code, p.dest_code, p.day
            ORDER BY p.day;
        """
        params = {
            'orig_codes': orig_codes,
            'dest_codes': dest_codes,
            'date_from': date_from,
            'date_to': date_to
        }

        rows = RatestaskHelper.execute_query(query=query, params=params)
        rate_list = []
        for row in rows:
            print(row)
            rate_list.append({
                'origin': row[0],
                'destination': row[1],
                'day': row[2].strftime('%Y-%m-%d'),
                'average_price': int(row[4]) if row[4] else row[4]
            })
        return rate_list


    @staticmethod
    def get_child_region_for_region(region):
        query = """
            WITH RECURSIVE region_tree(slug, parent_slug)
            AS (SELECT slug, parent_slug FROM regions where slug=%(region)s
                UNION ALL
                SELECT r.slug, r.parent_slug FROM regions r, region_tree rt where r.parent_slug = rt.slug)
            SELECT rt.slug as region, rt.parent_slug As parent_region from region_tree rt where rt.parent_slug is not NULL ORDER By rt.parent_slug;
        """
        params = {'region': region}
        rows = RatestaskHelper.execute_query(query=query, params=params)
        all_regions = []
        for row in rows:
            print(row)
            all_regions.append(row[0])
        return all_regions


    @staticmethod
    def get_port_code_for_region(region):
        all_regions = RatestaskHelper.get_child_region_for_region(region=region)
        print(f"\n\nall_regions: {all_regions}")
        query = """
            SELECT p.code
            FROM ports p
            WHERE parent_slug = ANY(%(all_regions)s)
        """
        params = {'all_regions': all_regions}
        rows = RatestaskHelper.execute_query(query=query, params=params)
        port_codes = []
        for row in rows:
            print(f"\n {row}")
            port_codes.append(row[0])
        return port_codes