from flask import Flask,render_template
#import pymysql
from member import *
from user import *

from datetime import timedelta
app = Flask(__name__)
app.secret_key = "Jefree"
app.permanent_session_lifetime = timedelta(minutes=5)

app.register_blueprint(member)
app.register_blueprint(user)

@app.route("/")
def Index():
    return render_template('login.html',headername="Login เข้าใช้งานระบบ")

@app.route("/member")
def member():
        return "This is member Page"

if __name__ == '__main__':
    app.run(debug = True,host="ec2-184-73-249-9.compute-1.amazonaws.com",port=5432)
