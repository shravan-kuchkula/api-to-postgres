"""Extract data from an API and store it in a table.

Makes a GET request to FrameIO's account API for the specified
date range and parses the response to only keep actions related
to comment and asset creation. Stores the results into a postgres
database table contains unique user_ids and their actions.

"""
import requests
import configparser
import psycopg2
import sys
from frameio import DBConnection
from frameio import APIClient
from frameio import drop_table_queries, create_table_queries, insert_table_queries

def etl():

    # read the configs
    config = configparser.ConfigParser()
    config.read('configs.cfg')

    # get a database connection
    try:
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DB'].values()))
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as err:
        print("Error while connecting to DB: {}".format(err))
        sys.exit("Check if given DB exists and is running")

    # create a db connection
    db = DBConnection(conn, cur)

    # drop tables
    db.run(drop_table_queries)

    # create tables
    db.run(create_table_queries)

    # get the API creds
    account_id = config.get('API', 'ACCOUNT_ID')
    token = config.get('API', 'TOKEN')

    # get date range
    start_date = config.get('FILTER', 'START_DATE')
    end_date = config.get('FILTER', 'END_DATE')

    # build the request
    date_filter = '''?filter[inserted_at][op]=gte&filter[inserted_at][value]={}T00:00:00Z\
    &filter[inserted_at][op]=lte&filter[inserted_at][value]={}T00:00:00Z'''.format(start_date, end_date)
    api_url = "https://api.frame.io/v2/accounts/{}/audit_logs{}".format(account_id, date_filter)
    headers = {"Authorization": "Bearer {}".format(token)}

    # make the request, parse the response, insert into table
    with requests.Session() as session:
        try:
            client = APIClient(api_url, headers, session)
            # iterate over the generator representing paginated results
            for page in client.get_pages():
                for log in page:
                    if log['action'] == 'CommentCreated':
                        # insert values: user_id, is_comment, is_asset
                        db.insert_row(insert_table_queries['insert_comment'], (log['id'], 'yes', 'no'))
                    elif log['action'] == 'AssetCreated':
                        # insert values: user_id, is_comment, is_asset
                        db.insert_row(insert_table_queries['insert_asset'], (log['id'], 'no', 'yes'))
        except (Exception, requests.HTTPError) as err:
            print("Error while connecting to API: {}".format(err))

    # close the db connection
    db.close()

if __name__ == '__main__':
    etl()
