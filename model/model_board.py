from flask import request, session

from model.model_member import getconn


def select_board():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board ORDER BY bno DESC"
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return rs


def select_bo_one(bno):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board WHERE bno = '%s' " % (bno)
    cur.execute(sql)
    rs = cur.fetchone()

    #hit 1증가 시켜서 - update set
    hit = rs[4]       # 이전 조회수
    hit = hit + 1
    sql = "UPDATE board SET hit = '%s' WHERE bno = '%s' " % (hit, bno)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return rs

def write_board():
    # 데이터를 넘겨 받음
    title = request.form['title']
    content = request.form['content']
    hit = 0
    mid = session.get('userID')  # 로그인한 mid(글쓴이)

    # db 연동 처리
    conn = getconn()
    cur = conn.cursor()
    sql = "INSERT INTO board(title, content, hit, mid) " \
          "VALUES ('%s', '%s', '%s', '%s')" % (title, content, hit, mid)
    cur.execute(sql)
    conn.commit()
    conn.close()

def delete_board(bno):
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM board WHERE bno = '%s'" % (bno)
    cur.execute(sql)
    conn.commit()
    conn.close()

def update_board(bno):
    # 데이터 전달 받기
    title = request.form["title"]
    content = request.form['content']
    mid = session.get('userName')

    # db 연동
    conn = getconn()
    cur = conn.cursor()
    sql = "UPDATE board SET  title = '%s', content = '%s', mid = '%s' " \
          "WHERE bno = '%s'" % (title, content, mid, bno)
    cur.execute(sql)
    conn.commit()
    conn.close()
