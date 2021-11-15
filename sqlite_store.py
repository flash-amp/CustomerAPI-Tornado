import sqlite3
from sqlite3.dbapi2 import Error

keys = ('id','firstName','lastName','emailId','mobileNo','city','address')

def create_conn(db_file = 'customer.db'):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    sql = '''CREATE TABLE IF NOT EXISTS CUSTOMER(
            id integer,
            firstname text,
            lastname text, 
            emailid text, 
            mobileno INTEGER, 
            city text,
            address text
    );'''
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def insert_customer(conn, cust):
    sql = '''INSERT into customer(id,firstname, lastname, emailid, mobileno, city, address) 
            values(?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    try:
        cur.execute(sql,cust)
    except Error as e:
        return "Invalid parameter values"
    conn.commit()
    return dict(keys,cust)

def select_all_customers(conn):
    c = conn.cursor()
    try:
        c.execute("select * from customer")
    except Error as e:
        return "Invalid customer"
    rows = c.fetchall()
    # return row
    json_dict = {}
    for row in rows:
        json_dict[row[0]] = dict(zip(keys,row))
    return json_dict
        

def select_customer_by_id(conn,id):
    c = conn.cursor()
    try:
        c.execute("select * from customer where id =?",(id,))
    except Error as e:
        return "Invalid customer"
    rows = c.fetchone()
    return dict(zip(keys,rows))

def update_customer(conn,val):
    sql = '''UPDATE customer set firstname = ?,
            lastname=?,
            emailid=?,
            mobileno=?,
            city=?,
            address=?
            where id=?
            '''
    cur = conn.cursor()
    try:
        cur.execute(sql,val)
    except Error as e:
        return "Invalid parameter values"
    conn.commit()
    return f"Updated {val[6]} successfully"

def delete_customer(conn,id):
    c = conn.cursor()
    try:
        c.execute("delete from customer where id =?",(id,))
    except Error as e:
        return e
    conn.commit()
    return f'Deleted {id} successfully'

# c.execute("""CREATE TABLE customer(
#     id integer PRIMARY KEY,
#     firstname text,
#     lastname text,
#     mobileno integer,
#     city text,
#     address text
# )""")

# c.execute("""INSERT INTO customer VALUES(
#     1,'flash','amp',1234567890,'Central city','ccpd'
# )""")

# c.execute("""delete table customer""")

# print(c.fetchone())

# conn.commit()

# conn.close()