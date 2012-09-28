'''
Created on 2012-9-4

@author: jizhishu
'''
import MySQLdb

def select(conn):
    cursor = conn.cursor()
    n = cursor.execute("select * from test")
    print "select",n
    rows = cursor.fetchall()

    for (idtest, col1, col2, col3) in rows:
        print "idtest={0}, col1={1}, col2={2}, col3={3}".format(idtest, col1, col2, col3)

def insert(conn):
    cursor = conn.cursor()
    n = cursor.execute("insert into test values (3, 4, 5, 6)");
    print "insert", n

def update(conn):
    cursor = conn.cursor()
    n = cursor.execute("update users set age = age + 10, sex = %s where name like %s", (1, "a%"));
    print "update", n

def delete(conn):
    cursor = conn.cursor()
    n = cursor.execute("delete from users where name like %s", "a%");
    print "delete", n

def main():
    conn = MySQLdb.connect(host = "localhost", user = "jizhishu", passwd = "jzs030547", db = "django")

    try:
        insert(conn)
        #update(conn)
        select(conn)
        #delete(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()