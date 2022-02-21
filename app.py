import sqlite3

from flask import Flask, render_template, request, redirect,url_for, session

from tbl_member import select_member

app = Flask(__name__)

app.secret_key = "#abcde!"   #비밀키 설정 필수

# db 점속 함수
def getconn():
    conn = sqlite3.connect("./member.db")
    return conn

# index 페이지
@app.route('/')
def index():
    return render_template('index.html')
    #return "<h1>Hello~ flask</h1>"

#회원 목록
@app.route('/memberlist/')
def memberlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member ORDER BY regDate DESC"
    cur.execute(sql)
    rs = cur.fetchall()   # 회원 전체
    conn.close()
    return render_template("memberlist.html", rs = rs)

# 회원 상세 페이지
@app.route('/member_view/<string:id>/')
def member_view(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s'" % (id)
    cur.execute(sql)
    rs = cur.fetchone()    # 회원 1명
    conn.close()
    return render_template('member_view.html', rs = rs)

# 회원 가입
@app.route('/register/', methods = ['GET','POST'])
def register():
    if request.method == "POST":
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
        print("회원 추가")
        conn.close()
        return redirect(url_for('memberlist'))   # redirect - 페이지 이동 함수

    else:
        return render_template('register.html')

# 로그인 페이지
@app.route('/login/', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 입력된 id, 비번을 가져오기
        id = request.form['mid']
        pwd = request.form['passwd']
        
        #db 연동
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' AND passwd = '%s'" % (id, pwd)
        cur.execute(sql)
        rs = cur.fetchone()
        if rs:    #rs가 있다면 (일치하면)
            session['userID'] = rs[0]   #아이디로 세션 발급
            return redirect(url_for('index'))  # 로그인후 인덱스페이지로 이동
        else:
            error = "아이디나 비밀번호를 확인해주세요."
            return render_template('login.html', error = error)
        
    else:
        return render_template('login.html')

#로그아웃 페이지
@app.route('/logout/')
def logout():
    session.pop("userID")    #세션 삭제
    return redirect(url_for('index'))

#회원 삭제
@app.route('/member_del/<string:id>/')
def member_del(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM member WHERE mid = '%s'" % (id)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('memberlist'))

app.run(debug=True)