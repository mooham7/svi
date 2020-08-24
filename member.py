from flask import Blueprint,render_template,request,redirect,url_for,session
import pymysql
from config import *
from user import *

con = pymysql.connect(HOST,USER,PASS,DATABASE)
member = Blueprint('member',__name__)

@member.route("/showmember")
def Showdatamember():
    if "username" not in session:
        return render_template('login.html',headername="Login เข้าใช้งานระบบ")

    with con:
        cur = con.cursor()
        sql = "SELECT * FROM tb_leakboard"
        cur.execute(sql)
        rows = cur.fetchall()
        return render_template("showdatamember.html",headername = "ข้อมูลบอร์ด",datas = rows)

@member.route("/showsearch",methods=["POST"])
def Showsearch():
    if "username" not in session:
        return render_template('login.html',headername="Login เข้าใช้งานระบบ")
    with con:
        if request.method == "POST":
            KeySearch = request.form['searchname']
            likeString = "%" + KeySearch +"%"
            cur = con.cursor()
            sql = "SELECT * FROM tb_leakboard where leak_serial like %s or leak_wo like %s"
            cur.execute(sql,(likeString,likeString))
            rows = cur.fetchall()
            cur.close()
            return render_template("showdatamember.html",headername="ข้อมูลสมาชิก",datas=rows)


@member.route("/showwithdate",methods=["POST"])
def Showwithdate():
    if "username" not in session:
        return render_template('login.html',headername="Login เข้าใช้งานระบบ")
    if request.method == "POST":
        dstart = request.form['dtstart']
        dtend = request.form['dtend']
        with con:
            cur = con.cursor()
            sql = "SELECT * FROM tb_leakboard where leak_datetime between %s and %s"
            cur.execute(sql,(dstart,dtend))
            rows = cur.fetchall()
            cur.close()
            return render_template("showdatamember.html",headername="ข้อมูลบอร์ด",datas=rows)

@member.route("/editmember",methods = ["POST"])
def Editmember():
        if request.method == "POST":
            id = request.form["id"]
            en = request.form["en"]
            serial = request.form["serial"]
            wo = request.form["wo"]
            location = request.form["location"]
            rootcause = request.form["rootcause"]
            result = request.form["result"]
        with con:
                #update with nopic
                cur = con.cursor()
                sql = "update tb_leakboard set leak_en = %s,leak_serial = %s,leak_wo = %s,leak_location = %s,leak_rootcause = %s,leak_result= %s where leak_id = %s"
                cur.execute(sql,(en,serial,wo,location,rootcause,result,id))
                con.commit()

                return redirect(url_for('member.Showdatamember'))


@member.route("/delmember",methods=["POST"])
def Delmember():

    if request.method == "POST":
        id = request.form['id']

        with con:
                    cur = con.cursor()
                    sql = "delete from tb_leakboard where leak_id = %s"
                    cur.execute(sql,(id))
                    con.commit()
                    cur.close()
                    return redirect(url_for('member.Showdatamember'))

    else:
            return render_template("login.html",headername ="Login เข้าใช้งานระบบ")

@member.route("/adddatamember")
def Adddatamember():

     return render_template("adddatamember.html",headername="เพิ่มข้อมูลบอร์ด")

@member.route("/adddata",methods=["POST"])
def Adddata():
    if request.method == "POST":
        en = request.form["en"]
        serial = request.form["serial"]
        wo = request.form["wo"]
        location = request.form["location"]
        rootcause = request.form["rootcause"]
        result = request.form["result"]

        with con:
            cur = con.cursor()
            sql = "SELECT * FROM tb_leakboard where leak_serial = %s"
            cur.execute(sql,(serial))
            rows = cur.fetchall()
            cur.close()

            if len(rows)>0:
                return "SERIAL NUMBER ซ้ำ"

            else:

                with con:
                    cur = con.cursor()
                    sql = "insert into tb_leakboard (leak_en,leak_serial,leak_wo,leak_location,leak_rootcause,leak_result) VALUES (%s,%s,%s,%s,%s,%s)"
                    cur.execute(sql,(en,serial,wo,location,rootcause,result))
                    con.commit()
                    cur.close()
                    return redirect(url_for('member.Showdatamember'))
