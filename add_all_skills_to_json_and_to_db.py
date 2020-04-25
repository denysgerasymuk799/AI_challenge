import os
# import Python's JSON lib
import json
# import the new JSON method from psycopg2
import psycopg2
from psycopg2.extras import Json

from sea_db import config


def write_json_in_db(record_list):
    # create a nested list of the records' values
    values = list(record_list.values())

    # get the column names
    columns = list(record_list.keys())

    # value string for the SQL string
    values_str = []

    # enumerate over the records' values
    for i, record in enumerate(values):

        # declare empty list for values
        val_list = []

        # append each value to a new list of values
        for v, val in enumerate(record):
            if type(val) == str:
                val = str(Json(val)).replace('"', '')
            val_list += [str(val)]
        if not val_list:
            val_list += ['0']
        # put parenthesis around each record string
        values_str.append("[" + ', '.join(val_list) + "]")
        # values_str += "(" + ', '.join(val_list) + "),\n"

    # remove the last comma and end SQL with a semicolon
    # values_str = values_str[:-2] + ";"

    # concatenate the SQL string
    table_name = "skills_for_all_professions"

    conn = None
    try:
        # read database configuration
        params = config.config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # create table one by one
        for num in range(len(columns)):
            sql_string = """INSERT INTO {0} ({1})\nVALUES ({2});""".format(
                table_name,
                ', '.join(["job_title", "skills_list"]),
                ', '.join(["'{}'".format(columns[num]), 'ARRAY'+values_str[num]])
            )

            cur.execute(sql_string)

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    skills_for_all_professions = json.loads('{}')
    for file in os.listdir(os.path.join(os.getcwd(), 'user_data')):
        with open(os.path.join(os.getcwd(), 'user_data', file), 'r',
                  encoding='utf-8') as json_file:
            courses_for_professions = json.load(json_file)

            title_file = file.split('.')
            skills_for_all_professions[title_file[0]] = list(courses_for_professions.keys())

    write_json_in_db(skills_for_all_professions)
