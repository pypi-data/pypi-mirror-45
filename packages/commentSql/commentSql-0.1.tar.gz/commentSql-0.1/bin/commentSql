#!/usr/bin/env python3
import pymysql


def get_defalut_clause(default_value):

    if (default_value is None):
        return ""
    if (default_value is ""):
        return "DEFAULT ''"
    return "DEFAULT " + default_value


def get_table_schema(db_name, table_name, conn):
    cursor = conn.cursor()
    cursor.execute('desc ' + table_name)
    columns = cursor.fetchall()

    cursor.execute(
        "select a.COLUMN_NAME, a.COLUMN_COMMENT from information_schema.`COLUMNS` a where a.TABLE_SCHEMA='{}' and a.TABLE_NAME='{}'".format(db_name, table_name))
    comments = cursor.fetchall()
    comments = dict((x, y) for x, y in comments)

    modify_sql = '/**********alter table {}*********/  \n'.format(table_name)
    modify_sql += 'ALTER TABLE {}'.format(table_name)

    for column in columns:
        (col_name, col_type, col_nullable, col_key, col_default, extra) = column

        nullable_clause = " " if col_nullable == "YES" else " NOT NULL "
        default_clause = get_defalut_clause(col_default)
        modify_sql += '\nCHANGE COLUMN `{}` `{}` {} {} {} {} COMMENT \'{}\','.format(
            col_name, col_name, col_type, nullable_clause, default_clause, extra, comments[col_name])
    modify_sql = modify_sql[:-1] + ";\n\n"
    modify_sql += 'ALTER TABLE {} COMMENT "";\n\n'.format(table_name)
    return modify_sql


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', type=int, default=3306,
                    help='db port', required=False)
parser.add_argument('-host', help='db host', type=str)
parser.add_argument('-d', help='db name', type=str)
parser.add_argument('-u', help='db user', type=str)
parser.add_argument('-pw', help='db password', type=str)

args = vars(parser.parse_args())


if (args.get('host') is None):
    print("请填写数据库地址, -h")
    exit()
if (args.get('u') is None):
    print("请填写数据库用户, -u")
    exit()
if (args.get('pw') is None):
    print("请填写数据库密码, -pw")
    exit()
if (args.get('d') is None):
    print("请填写数据库名称, -d")
    exit()

conn = pymysql.connect(host=args.get('host'),
                       port=args.get('p'),
                       user=args.get('u'),
                       password=args.get('pw'),
                       database=args.get('d'))

cursor = conn.cursor()
cursor.execute("SHOW TABLES;")
table_names = [t[0] for t in cursor]
cursor.close()


result = ""
for table in table_names:
    sql = get_table_schema(args.get('d'), table, conn)
    result += sql

with open("alter_{}.sql".format(args.get('d')), "w") as f:
    f.write(result)

print("export successfully")
