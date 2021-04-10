import requests
from bs4 import BeautifulSoup
import smtplib
import config
from time import *



data = requests.get('https://www.brawlhalla.com/rankings/1v1/')
soup = BeautifulSoup(data.text, 'html.parser')

data=[]
for tr in soup.find_all('tr', {'class':['odd','even']}):
    values=[td.text for td in tr.find_all('td')]
    data.append(values)
stored=[]
for elem in data:
    if len(elem)==8:
        wrlist=elem[5].split("-")
        wr=round(int(wrlist[0])/(int(wrlist[0])+int(wrlist[1]))*100,1)
        stored.append("{:3s} {:17s} {:4s} elo      wr:{:4}% ({} games)".format(elem[1]+".",elem[3][:17],elem[6],wr, int(wrlist[0])+int(wrlist[1])))
formatted=('\n'.join(stored).encode('ascii', 'ignore').decode('ascii')) #enfin

def send_email(subject,msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject,msg)
        server.sendmail(config.EMAIL_ADDRESS, config.DEST, message)
        server.quit()
        print("Success: Email sent to {}".format(config.DEST))
    except:
        print("Email failed to send.")

subject = "Classement 1V1 Brawlhalla - {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
msg = formatted
send_email(subject,msg)
print(msg)

