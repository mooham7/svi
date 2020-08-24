from flask import Blueprint,render_template,request,redirect,url_for,session
import pymysql
from config import *
from user import *

con = pymysql.connect(HOST,USER,PASS,DATABASE)
user = Blueprint('user',__name__)

@user.route("/loginpage")
def Loginpage():

    if "username" not in session:
        return render_template("login.html", headername="Login เข้าใช้งานระบบ")
    else:
        return redirect(url_for('member.Showdatamember'))

@user.route("/checklogin",methods = ["POST"])
def Checklogin():

    username = request.form['username']
    password = request.form['password']

    with con:
        cur = con.cursor()
        sql = "SELECT * FROM tb_user WHERE usr_username = %s AND usr_password = %s and usr_status=1"
        cur.execute(sql,(username,password))
        rows = cur.fetchall()
        cur.close()
        if len(rows) > 0:
            session['username'] = username
            session['fname'] = rows[0][1]
            session['lname'] = rows[0][2]
            session.permanent = True
            return redirect(url_for('member.Showdatamember'))

        else:
            return render_template("login.html",headername ="Login เข้าใช้งานระบบ")

@user.route("/logoff")
def Logoff():
    session.clear()
    return redirect(url_for('user.Loginpage'))

@user.route("/checkauth")
def Checkauth():
    auth = request.form['auth']
    status = request.form['status']
    with con:
        cur = con.cursor()
        sql = "SELECT * FROM tb_user WHERE usr_auth = 1 AND usr_status=1"
        cur.execute(sql,(auth,status))
        rows = cur.fetchall()
        cur.close()
        if len(rows) > 0:
            session['username'] = username
            session['auth'] = rows[5][6]

            return redirect(url_for('member.Showdatamember'))
        else:

            return render_template("login.html",headername ="Login เข้าใช้งานระบบ")
