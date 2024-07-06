from flask import Flask, request, render_template
from email.message import EmailMessage
import ssl
import smtplib
import mimetypes
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

def add_attachment(email_message, file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    mime_type, mime_subtype = mime_type.split('/')

    with open(file_path, 'rb') as file:
        email_message.add_attachment(file.read(), maintype=mime_type, subtype=mime_subtype, filename=file_path.name)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email_sender = os.getenv('EMAIL_SENDER')
        email_password = os.getenv('EMAIL_PASSWORD')
        email_receiver = request.form['email_receiver']
        subject = request.form['subject']
        body = request.form['body']

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        files = request.files.getlist('attachments')
        for file in files:
            file_path = Path(file.filename)
            file.save(file_path)
            add_attachment(em, file_path)
            os.remove(file_path)  # Clean up the saved file

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(em)
        
        return 'Email sent successfully!'

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
