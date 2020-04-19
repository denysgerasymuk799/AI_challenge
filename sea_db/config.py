# !/usr/bin/python
import os
from configparser import ConfigParser


def config(filename="./sea_db/courses_and_skills_db.ini", section='postgresql'):
    db = {}
    try:
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    except:
        print('config error - if parser.has_section(section):')
    return db