from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

# Configuration of Flask-Mail with the variables
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# website routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    if request.method == 'POST':
        # Obtener datos del formulario
        name = request.form.get('rname')
        phone = request.form.get('phone')
        date = request.form.get('rdate')
        party_size = request.form.get('rparty-size')
        additional_info = request.form.get('radd-info')

        # Here you create de mail.
        msg = Message(
            subject="New Reservation Request",
            recipients=[os.getenv('MAIL_USERNAME')],
            body=f"""
            Reservation Details:
            Name: {name}
            Phone: {phone}
            Date: {date}
            Party Size: {party_size}
            Additional Information: {additional_info}
            """
        )

        # here you send the mal
        try:
            mail.send(msg)
            flash("Reservation confirmed!", "success")
            return redirect(url_for('reservations'))
        except Exception as e:
            print(f"Error sending email: {e}")
            flash("There was an issue sending your reservation. Please try again later.", "error")
            return redirect(url_for('reservations'))

    return render_template('reservations.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
