from datetime import datetime
from flask_mail import Mail, Message
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

sender = os.getenv("SENDER")
password = os.getenv("PASSWORD")

app = Flask(__name__)
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = sender
app.config['MAIL_PASSWORD'] = password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def sendMail(mailList):
    current_time = datetime.now().strftime("%H:%M:%S")

    msg = Message(
        subject='Movement Detected at your doorstep!!!',
        sender = 'alarm@notifier.com',
        recipients = mailList, 
        body=f"Movement detected at your doorstep. Exact time was : {current_time}"
    )
    mail.send(msg)