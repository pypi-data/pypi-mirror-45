"""Populate database with atomic data."""
import os
import psycopg2
from atomicdataMB import make_gvalue_table, make_photo_table


def initialize_atomicdata(database='thesolarsystemmb'):
    with psycopg2.connect(host='localhost', database='postgres') as con:
        con.autocommit = True
        cur = con.cursor()
        cur.execute('select datname from pg_database')
        dbs = [r[0] for r in cur.fetchall()]

        if database not in dbs:
            print(f'Creating database {database}')
            cur.execute(f'create database {database}')
        else:
            pass

    with psycopg2.connect(host='localhost', database=database) as con:
        con.autocommit = True
        cur = con.cursor()
        cur.execute('select table_name from information_schema.tables')
        tables = [r[0] for r in cur.fetchall()]

        if 'gvalues' not in tables:
            make_gvalue_table(con)
        else:
            pass

        if 'photorates' not in tables:
            make_photo_table(con)
        else:
            pass
