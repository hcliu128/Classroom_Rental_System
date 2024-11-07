from utils.db import connection
from flask import Flask, render_template
from user import user_bp
from admin import admin_bp
from auth import auth_bp
from flask_mail import Mail
import argparse
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv('./.env')

app.config.update(
    #  gmail
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='swe3onlinegame@gmail.com',
    MAIL_PASSWORD='xybcnshquazoqoux'
)
mail = Mail(app)

app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser(description='Flask server configuration')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host for the Flask server')
    parser.add_argument('--port', type=int, default=8080, help='Port for the Flask server')
    parser.add_argument('--debug', action='store_true', default=False, help='Debug mode for the Flask server')
    args = parser.parse_args()

    # Check Connection
    if connection.is_connected():
        print('[App.py] Connected to MySQL database')

    # Register Blueprints
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Use parsed arguments to configure the Flask server
    app.run(host=args.host, port=args.port, debug=args.debug)