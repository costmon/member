import sqlite3

# db 점속 함수
from flask import request


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

def select_one(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s'" % (id)
    cur.execute(sql)
    rs = cur.fetchone()  # 회원 1명
    conn.close()
    return rs

def join_member():
    # 데이터 가져오기
    id = request.form['mid']
    pwd = request.form['passwd']
    name = request.form['name']
    age = request.form['age']

    # db 저장
    conn = getconn()
    cur = conn.cursor()
    sql = "INSERT INTO member(mid, passwd, name, age) " \
          "VALUES ('%s', '%s', '%s', '%s')" % (id, pwd, name, age)
    cur.execute(sql)
    conn.commit()

    # 자동 로그인
    sql = "SELECT * FROM member WHERE mid = '%s' AND passwd = '%s'" % (id, pwd)
    cur.execute(sql)
    rs = cur.fetchone()
    conn.close()
    return rs

def login_member():
    # 입력된 id, 비번을 가져오기
    id = request.form['mid']
    pwd = request.form['passwd']

    # db 연동
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s' AND passwd = '%s'" % (id, pwd)
    cur.execute(sql)
    rs = cur.fetchone()
    conn.close()
    return rs

def delete_member(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "PRAGMA foreign_keys = ON"
    cur.execute(sql)
    sql = "DELETE FROM member WHERE mid = '%s'" % (id)
    cur.execute(sql)
    conn.commit()
    conn.close()

def update_member(id):
    # 데이터 수집
    mid = request.form['mid']
    pwd = request.form['passwd']
    name = request.form['name']
    age = request.form['age']

    # db 연동
    conn = getconn()
    cur = conn.cursor()
    sql = "UPDATE member SET  passwd = '%s', name = '%s', age = '%s' " \
          "WHERE mid = '%s'" % (pwd, name, age, mid)
    cur.execute(sql)
    conn.commit()
    conn.close()