import requests
from bs4 import BeautifulSoup
import csv
import smtplib
from email.mime.text import MIMEText
from dotenv import dotenv_values
import datetime
import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
import csv
from dotenv import dotenv_values

config = dotenv_values(".env")


def connect():
    url = "https://pt.ldplayer.net/games/type/108.html?current=1&sortType=2"
    response = requests.get(url)
    print(response)
    sp = BeautifulSoup(response.text, 'html.parser')
    div_elements = sp.find_all('div', {'class': 'game-item-name'})
    img = sp.find_all('img', {'class': 'game-item-icon'})

    # Create a list to store the data
    data = []

    for div, img in zip(div_elements, img):
        game_title = div.text
        image_url = img['src']
        data.append([image_url, game_title])

    # Write the data to a CSV file
    csv_file_path = 'data.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['image', 'game title'])  # Write the header
        csv_writer.writerows(data)  # Write the data rows

    print("CSV file created successfully!")

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()

    smtp.login("eronponcepereira@edu.unifil.br", config.get('PASSWORD'))

    msg = MIMEMultipart()

    # Set the 'From' and 'To' addresses
    msg['From'] = "eronponcepereira@edu.unifil.br"
    msg['To'] = "mario.adaniya@unifil.br"

    # Set the subject (optional)
    msg['Subject'] = "[DS101]"

    # Set the date
    today = datetime.date.today()
    msg['Date'] = today.strftime("%Y-%m-%d")

    # Create the email content
    email_content = ""
    for image_url, game_title in data:
        email_content += f"<img src='{image_url}' alt='{game_title}'><br>{game_title}<br><br>"

    # Set the email content as HTML
    email_body = MIMEText(email_content, 'html')

    # Attach the email body to the message
    msg.attach(email_body)

    try:
        # Use msg.as_string() to get the string representation of the message
        smtp.sendmail("eronponcepereira@edu.unifil.br", "mario.adaniya@unifil.br", msg.as_string())
    except smtplib.SMTPException as e:
        print(f"An error occurred: {e}")
    finally:
        smtp.quit()

connect()