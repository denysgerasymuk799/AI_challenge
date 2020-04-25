#!/usr/bin/python
import json
import os
import ssl

import psycopg2
from sea_db import config


def get_parts(retrieve_parameters, title_table, filename):
    """ query parts from the parts table """
    params = config.config(filename=filename)
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute("SELECT {} FROM {}".format(', '.join(retrieve_parameters), title_table))
    rows = cur.fetchall()
    rows_copy = []
    for row in rows:
        rows_copy.append(row)

    cur.close()
    return rows_copy


def create_table(online_platform_name, filename):
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    conn = None
    try:
        # read database configuration
        params = config.config(filename=filename)
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS {} (course_title character varying, price character varying,
         image character varying, course_duration character varying,
          number_of_students character varying, short_description character varying,
           long_description character varying, url character varying)'''.format(online_platform_name))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def connect_to_db(filename):
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    conn = None
    try:
        # read database configuration
        params = config.config(filename=filename)
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()

        return cur, conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def transform_data_from_table_in_json(table_name, filename):
    list_from_db = get_parts(["course_title", "price",
                              "image", "course_duration",
                              "number_of_students", "short_description",
                              "long_description", "url"], table_name, filename=filename)

    page_courses_json = json.loads('{}')
    table_columns = ["course_title", "price",
                     "image", "course_duration",
                     "number_of_students", "short_description",
                     "long_description", "url"]

    for course_data in list_from_db:
        course_data = list(course_data)
        course_title = course_data.pop(0)
        page_courses_json[course_title] = {}

        for column in table_columns[1:]:
            page_courses_json[course_title][column] = course_data.pop(0)

    print(list_from_db)
    print(page_courses_json)
    return page_courses_json


def insert_sql(table_name, answers):
    """ insert a new vendor into the vendors table """
    n_values = ['%s'] * len(answers)
    n_values = ', '.join(map(str, n_values))

    name_columns = ''

    if table_name == 'users_data':
        name_columns = 'username, language, n_videos'

    elif table_name == 'answers_on_survey':
        name_columns = 'username, question1, question2, question3, question4'

    sql = """INSERT INTO {0} ({1}) 
            VALUES ({2})""".format(table_name, name_columns, n_values)
    conn = None
    try:
        # read database configuration
        params = config.config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, answers)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def update_sql(name_table, name_parameter, username, parameter):
    """ update vendor name based on the vendor id """
    print("update")
    sql = """ UPDATE {}
                SET {} = %s
                WHERE username = %s""".format(name_table, name_parameter)
    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config.config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (str(parameter), username))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


def if_course_in_db(course_name, retrieve_parameters, table_name, filename):
    course_inf = get_parts(retrieve_parameters, table_name, filename)
    # search course_name in database
    for course_data in course_inf:
        if course_data[0] == course_name:
            return True

    return False


if __name__ == '__main__':
    # insert_sql('users_data', username, "uk", 0)
    transform_data_from_table_in_json("Coursera")
