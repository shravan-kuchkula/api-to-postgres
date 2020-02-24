"""Extract data from an API and store it in a table.

Makes a GET request to FrameIO's account API for the specified
date range and parses the response to only keep actions related
to comment and asset creation. Stores the results into a postgres
database table contains unique user_ids and their actions.

"""
import configparser
import psycopg2
import sys
from frameio import DBConnection
from frameio import validation_queries

def validation():

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

    # run validation queries
    for result in db.fetch(validation_queries):
        print("Executing: {}".format(result.query))
        print("Output: ")
        rows = result.fetchall()
        for row in rows:
            print(row)

    # close the db connection
    db.close()

if __name__ == '__main__':
    validation()
