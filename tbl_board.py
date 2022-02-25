import sqlite3

def getconn():
    conn = sqlite3.connect("./member.db")
    return conn

# con = getconn()
# print("DB접속", con)

def create_table():
    conn = getconn()
    cur = conn.cursor()
    sql = """
        CREATE TABLE board(
            bno integer PRIMARY KEY AUTOINCREMENT,
            title text NOT NULL,
            content text NOT NULL,
            createDate timestamp date DEFAULT (datetime('now', 'localtime')),
            hit integer,
            mid char(5) NOT NULL,
            FOREIGN KEY(mid) REFERENCES member(mid) ON DELETE CASCADE
        )
    """
    cur.execute(sql)
    conn.commit()
    print("board 테이블 생성")
    conn.close()
def insert_board():
    conn = getconn()
    cur = conn.cursor()
    sql = "INSERT INTO board(title, content, mid) VALUES " \
          "('첫번째 글입니다.', '글 내용입니다.', 'cloud')"
    cur.execute(sql)
    conn.commit()
    conn.close()

def select_board():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board ORDER BY bno DESC"
    cur.execute(sql)
    rs = cur.fetchall()
    #print(rs)
    for i in rs:
        print(i)
    conn.close()

create_table()
#insert_board()
#select_board()