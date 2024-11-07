from flask import render_template, request, redirect, url_for, flash, session
from utils.db import connection
from . import auth_bp
import uuid
import random
import string
from flask_mail import Message
from flask import current_app
from app import mail

from utils.constant import goto_admin, goto_user

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        cur = connection.cursor(buffered=True)
        cur.execute("SELECT password, type FROM user WHERE user_name=%s", [username])
        r = cur.fetchone()
        if r:
            user_password, user_type = r
        cur.close()


        if r and user_password == password:
            session['username'] = username
            flash('成功登入', 'success')
            if user_type in goto_admin:
                session['user_type'] = user_type
                return redirect(url_for('admin.home'))
            elif user_type in goto_user:
                session['user_type'] = user_type
                return redirect(url_for('user.index'))
            else:
                flash(f'不正確的用戶類型: {user_type}', 'danger')
        else:
            flash('帳號或密碼錯誤', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('您已成功登出', 'success')
    return redirect(url_for('auth.login'))




@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        realname = request.form['realname']
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        email = request.form['email']

        # Validate phone number and password length
        if len(phone) != 10:
            flash('請輸入正確的十位數手機號碼', 'danger')
            return render_template('register.html')

        if len(password) < 6 or len(password) > 20:
            flash('請輸入 6 到 20 位數的密碼', 'danger')
            return render_template('register.html')

        # Generate a unique user ID
        user_id = generate_unique_user_id()

        cur = connection.cursor()
        try:
            cur.execute("INSERT INTO user (User_ID, Name, User_Name, Password, Phone, Email, Type) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (user_id, realname, username, password, phone, email, 'Student'))
            connection.commit()
            flash('註冊成功! 請輸入帳號密碼登入', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            connection.rollback()
            flash('註冊失敗:使用者名稱已被使用', 'danger')
        finally:
            cur.close()

    return render_template('register.html')



@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        cur = connection.cursor()
        cur.execute("SELECT 1 FROM user WHERE User_Name=%s AND Email=%s", (username, email))
        user = cur.fetchone()
        cur.close()

        if user:
            reset_token = generate_reset_token()
            cur = connection.cursor()
            cur.execute("UPDATE user SET reset_token=%s WHERE User_Name=%s", (reset_token, username))
            connection.commit()
            cur.close()
            send_reset_code(username, email, reset_token)
            flash('驗證碼已傳送到您的email', 'success')
            return redirect(url_for('auth.reset_password'))
        else:
            flash('用戶或Email錯誤', 'danger')

    return render_template('forgot_password.html')

@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        token = request.form.get('token')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        cur = connection.cursor()
        cur.execute("SELECT * FROM user WHERE reset_token=%s", [token])
        user = cur.fetchone()

        if not user:
            flash('驗證碼無效', 'danger')
            return redirect(url_for('auth.reset_password'))

        if new_password != confirm_new_password:
            flash('密碼不匹配', 'danger')
            return redirect(url_for('auth.reset_password'))

        cur.execute("UPDATE user SET Password=%s, reset_token=NULL WHERE reset_token=%s", ((new_password), token))
        connection.commit()
        cur.close()

        flash('您已成功修改密碼，請重新登入', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')

@auth_bp.route('/tutorial', methods=['GET', 'POST'])
def tutorial():

    return render_template('tutorial.html')



def generate_unique_user_id():
    while True:
        user_id = str(uuid.uuid4())
        cur = connection.cursor()
        cur.execute("SELECT 1 FROM user WHERE User_ID = %s", (user_id,))
        if not cur.fetchone():
            cur.close()
            return user_id
        cur.close()

def send_reset_code(username, email, reset_token):
    msg_title = 'SWEGame 重設Email驗證信'
    msg_sender = current_app.config['MAIL_USERNAME']
    msg_recipients = [email]

    email_content = f"""
    <html>
        <head>
            <style>
                body {{
                    background-color: #ff8c00;  /* 上下橘色背景 */
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    margin: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .orange-bg {{
                    background-color: #ff8c00;  /* 橘色背景 */
                    color: #ffffff;  /* 文字顏色 */
                    padding: 10px;
                    text-align: center;
                }}
                .white-bg {{
                    background-color: #ffffff;  /* 白色背景 */
                    color: #000000;  /* 文字顏色 */
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    margin-top: 20px;
                    margin-bottom: 20px;
                }}
                .random-code {{
                    font-size: 36px;
                    color: #ff8c00;  /* 橘色文字 */
                    text-align: center;
                    margin-bottom: 10px;
                }}
                .greeting {{
                    margin-top: 2px;
                    text-align: left;
                }}
                .instruction {{
                    text-align: left;
                    margin-top: -10px;
                    margin-bottom: 5px;
                }}
                .contact {{
                    text-align: center;
                    margin-top: -10px;
                    margin-bottom: 20px;
                }}
                .btn-confirm-email {{
                    padding: 10px 20px;
                    background-color: #ff8c00;  /* 修改為橘色 */
                    color: #ffffff;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    display: block;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="orange-bg">
                    <p>修改玩家密碼驗證信</p>
                </div>
                <div class="white-bg">
                    <p class="greeting">Dear {username},</p>
                    <p class="instruction">我們收到了您的忘記密碼請求，</p>
                    <p class="instruction">請使用以下驗證碼重置您的密碼：</p>
                    <p class="random-code">{reset_token}</p>
                    <p>如果您沒有送出請求，請忽略這封信件。</p>
                    <p>謝謝您，祝您有個美好的一天。</p>
                </div>
                <div class="orange-bg">
                    <p>如有其他問題，請直接回信聯繫我們！</p>
                </div>
            </div>
        </body>
    </html>
    """

    msg = Message(msg_title,
                  sender=msg_sender,
                  recipients=msg_recipients,
                  html=email_content)
    mail.send(msg)

def generate_reset_token():
    return ''.join(random.choices(string.digits, k=6))