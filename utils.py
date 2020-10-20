import datetime
import socket
import subprocess
import re
import sqlite3
from functools import wraps
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)

    except Error as e:
        print(e)


def send_to_db(func):
    @wraps(func)
    def wrapper():
        ips, names = func()
        today = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        for ip, name in zip(ips, names):
            new_entry(ip, name, today)
        return (ips, names)
    return wrapper


def new_entry(ip: str, name: str, date: str):
    """
    """
    sql = """INSERT INTO visitors (ip, name, date)
    VALUES ('%s', '%s', '%s')""" % (ip, name, date)
    with create_connection("database.db") as conn:
        c = conn.cursor()
        try:
            c.execute(sql)
        except sqlite3.Error as error:
            return Error
        conn.commit()

        
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0].split(".")


def scan_network():

    ip = get_ip_address()
    ip = ".".join(ip[:-1])

    result = subprocess.run(['nmap', '-sn', f"{ip}.0/24"], stdout=subprocess.PIPE)
    return str(result.stdout.decode("utf-8"))


@send_to_db
def give_ips():

    regex = "\((\d+\.\d+.\d+.\d+)\)"
    scan = scan_network()
    regex2 = "for ([\.\-\_\w\d]+) \("
    ips = re.findall(regex, scan)
    names = re.findall(regex2,scan)
    return (ips, names)
