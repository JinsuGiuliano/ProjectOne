import os
import smtplib
import imghdr
from email.message import EmailMessage
import sqlite3


def SendWelcome():
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	emails = c.execute("SELECT email FROM user;")
	contacts = c.fetchall()
	EMAIL_ADDRESS = os.environ.get('GJ_EMAIL_USER')
	EMAIL_PASSWORD = os.environ.get('GJ_EMAIL_PASS')
	for contact in contacts:
		msg = EmailMessage()
		msg['Subject'] = 'de JINSU - MI 1RA PAGINA WEB "CORONAVIRUS"'
		msg['From'] = EMAIL_ADDRESS
		msg['To'] = contact
		msg.set_content('Bienvenido a la WEB de CoronaVirus. Te estaremos informando de toda la informacion relevante sobre el COVID-19 al rededor del mundo.')

		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
		    smtp.send_message(msg)



SendWelcome()