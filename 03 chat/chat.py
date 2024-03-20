import openai
import requests
from bs4 import BeautifulSoup
from dotenv import dotenv_values
import time
from email.mime.multipart import MIMEMultipart
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


config = dotenv_values("../.env")
url = "https://g1.globo.com/pr/norte-noroeste/ultimas-noticias/"
response = requests.get(url)
print(response)
sp = BeautifulSoup(response.text, 'html.parser')
div_elements = sp.find_all('a', {'class': 'feed-post-link'})

href_list = [a['href'] for a in div_elements]
title_array = []
for link in href_list:
    response = requests.get(link)
    print(response)
    sp = BeautifulSoup(response.text, 'html.parser')
    title = sp.find_all('h1')
    content = sp.find_all('p')
    title_text = [tag.text for tag in title]
    content_text = [tag.text for tag in content]
    title_array.append([title_text, content_text])
    
print(title_array)

openai.api_key = config.get('API')
def openai_chat_completion(conversation):
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
            {'role': 'system', 'content':
            """Bom dia, estou aqui para te ajudar a encontrar as últimas notícias.
            escreva em portugês, por favor.
              """}
              ,{'role': 'user', 'content': str(conversation)}],
        temperature= 0.7)
    return response.choices[0].message.content.strip()

resposta = openai_chat_completion(title_array)
print(resposta)

def connect():
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login("eronponcepereira@edu.unifil.br", config.get('PASSWORD'))

    msg = MIMEMultipart()
    msg['From'] = "eronponcepereira@edu.unifil.br"
    msg['To'] = "mario.adaniya@unifil.br"
    msg['Subject'] = "[DS101] Chat GPT News letter"

    today = datetime.date.today()
    msg['Date'] = today.strftime("%Y-%m-%d")

    email_content = resposta

    email_body = MIMEText(email_content, 'html')
    msg.attach(email_body)

    try:
        smtp.sendmail("eronponcepereira@edu.unifil.br", "mario.adaniya@unifil.br", msg.as_string())
    except smtplib.SMTPException as e:
        print(f"An error occurred: {e}")
    finally:
        smtp.quit()

connect()