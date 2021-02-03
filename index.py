# 導入相對應的套件
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import FlaskSeeder
from flask_migrate import Migrate 

# 創建了一個flask的實例
app = Flask(__name__)

'''
在Flask項目中，我們會用到很多配置（Config） 像是以下的密鑰以及資料庫
Session, Cookies以及一些第三方擴展都會用到SECRET_KEY值
這是一個比較重要的配置值，如未使用，會出現以下錯誤
the session is unavailable because no secret key was set.
Set the secret_key on the application to something unique and secret
'''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:redd00r@172.20.10.2:3306/crud'
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db) 
seeder = FlaskSeeder()
seeder.init_app(app, db)

#定義模型(model)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    messages = db.relationship('Message', backref='user')
    def __repr__(self):
        return 'id=%r, User_name=%r' % (self.id, self.name)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return 'id=%r, title=%r,content=%r' % (self.id, self.title,self.content)

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    users = db.relationship('User', backref='city')
    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return 'id=%r, city_name=%r' % (self.id, self.name)

@app.route('/', methods=["POST", "GET"])
def Index():
    if request.method == "POST":
        id_data = request.form['id']
        content = request.form['current_content']
        title = request.form['current_title']
        select_message = Message.query.filter_by(id=int(id_data)).first()
        select_message.title = title
        select_message.content = content
        db.session.commit()
    ms=Message.query.all()
    return render_template('index3.html', messages=ms)

@app.route('/add',methods=["GET","POST"])
def Add():
    if request.method == "POST":
        content = request.form['content']
        title = request.form['title']
        add_name = request.form['add_name']
        select_user = User.query.filter_by(name=add_name)  # 先取得在user當中naem='Eric'的User_id
        #在Message()這張表單新增資料
        create_Eric_Messags = Message(user_id=select_user[0].id, title=title,content=content)
        db.session.add(create_Eric_Messags)  # 建立資料暫存
        db.session.commit()  # 傳送至資料庫
        return 'ok'
    return  render_template('add.html')

@app.route('/update_db/<message_id>', methods=["POST", "GET"])  # 小心同名子不行
def update_db(message_id):
    if request.method == "POST":
        content = request.form['content']
        title = request.form['title']
        select_message = Message.query.filter_by(id=int(message_id)).first()
        select_message.title = title
        select_message.content = content
        db.session.commit()
        return redirect(url_for('index3.html'))
    return render_template('update.html')

@app.route('/delete/<message_id>', methods=['GET', 'POST'])
def delete(message_id):
    # if request.method == "POST":
    select_message = Message.query.filter_by(id=int(message_id)).first()
    # 利用 delete 的方法即可刪除單筆資料
    db.session.delete(select_message)
    # 將之前的操作變更至資料庫中
    db.session.commit()
    return redirect(url_for('Index'))
    # return render_template('delete.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form["user_name"]
        user_city = request.form["city_select"]  # 寫入城市再說
        create_user = User(city_id=user_city,name=user_name)  # User()為要加入入的表單  # 必要條件為id(非必要),city_id(必要),name(必要)
        db.session.add(create_user)  # 建立資料暫存
        db.session.commit()  # 傳送至資料庫
        return render_template('index3.html')
    return render_template('register.html')

if __name__ == "__main__":
    # 由於在開發階段，將debug設為True
    app.run(debug=True)

