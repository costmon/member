import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

from model.model_board import select_board, select_bo_one, \
    write_board, delete_board, update_board
from model.model_member import getconn, select_member, select_one, \
    join_member, login_member, delete_member, update_member


app = Flask(__name__)

app.secret_key = "#abcde!"  #로그인시 에러발생 - 비밀키 설정 필수

# index 페이지
@app.route('/')
def index():
    return render_template('index.html')
    # return "<h1>Hello~ flask</h1>"

 #회원 목록
@app.route('/memberlist/')
def memberlist():
    rs = select_member()
    return render_template('memberlist.html', rs = rs)

# 회원 상세 페이지
@app.route('/member_view/<string:id>/', methods = ['GET'])
def member_view(id):
    rs = select_one(id)
    return render_template('member_view.html', rs = rs)

# 회원 가입
@app.route('/register/', methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        rs = join_member()
        if rs:
            session['userID'] = rs[0]    # 회원 가입시 세션 발급(아이디)
            session['userName'] = rs[2]  # 회원 가입시 세션 발급(이름)
            return redirect(url_for('memberlist'))
    else:
        return render_template('register.html')

# 로그인 페이지
@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        rs = login_member()
        if rs:  # rs가 있다면 (일치하면)
            session['userID'] = rs[0]  #아이디로 세션 발급
            session['userName'] = rs[2]
            return redirect(url_for('index'))  # 로그인후 인덱스페이지로 이동
        else:
            error = "아이디나 비밀번호를 확인해주세요"
            return render_template('login.html', error = error)
    else:
        return render_template('login.html')

#로그아웃 페이지
@app.route('/logout/')
def logout():
    session.pop("userID")    #세션 삭제
    session.pop("userName")
    # session.clear() # 모든 세션 삭제
    return redirect(url_for('index'))

# 회원 삭제
@app.route('/member_del/<string:id>/')
def member_del(id):
    delete_member(id)
    return redirect(url_for('memberlist'))

# 회원 수정
@app.route('/meber_edit/<string:id>/', methods=['GET', 'POST'])
def member_edit(id):
   if request.method == "POST":
       update_member(id)
       return redirect(url_for('member_view', id=id))  # 해당 id로 경로 설정
   else:
       rs = select_one(id)
       return render_template('member_edit.html', rs = rs)

# 게시글 목록
@app.route('/boardlist/')
def boardlist():
    rs = select_board()
    return render_template('boardlist.html', rs = rs)

# 게시글 상세 페이지
@app.route('/board_view/<int:bno>/', methods = ['GET'])
def board_view(bno):
    rs = select_bo_one(bno)
    return render_template('board_view.html', rs=rs)

# 게시글 쓰기
@app.route('/writing/', methods = ['GET', 'POST'])
def writing():
    if request.method == "POST":
        write_board()
        return redirect(url_for('boardlist'))
    else:
        return render_template('writing.html')

# 게시글 삭제
@app.route('/board_del/<int:bno>/')
def board_del(bno):
    delete_board(bno)
    return redirect(url_for('boardlist'))

# 게시글 수정
@app.route('/board_edit/<int:bno>/', methods = ['GET', 'POST'])
def board_edit(bno):
    if request.method == "POST":
        update_board(bno)
        return redirect(url_for('board_view', bno=bno))
    else:
        rs = select_bo_one(bno)
        return render_template('board_edit.html', rs=rs)

app.run(debug=True)