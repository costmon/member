import sqlite3

# db 점속 함수
def getconn():
    conn = sqlite3.connect("./member.db")
    return conn

def select_member():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member ORDER BY regDate DESC"
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return rs