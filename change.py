# -*- coding: utf-8 -*-
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import smtplib
from config import *
# import tweepy
from datetime import datetime


# from twilio.rest import Client

def send_email(user, pwd, recipient, subject, body):  # snippet courtesy of david / email sending function
    # SUBJECT = 'SITE UPDATED'  # message subject
    # body = 'CHANGE AT ' + str(url)  # message body
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]

    # Prepare actual message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = FROM
    msg['To'] = ", ".join(TO)
    part1 = MIMEText(subject, 'plain')
    part2 = MIMEText(body, 'html')
    msg.attach(part1)
    msg.attach(part2)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # start smtp server on port 587
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)  # login to gmail server
        server.sendmail(FROM, TO, msg.as_string())  # actually perform sending of mail
        server.close()  # end server
        print('[+] Successfully sent email notification')  # alert user mail was sent
    except Exception as e:  # else tell user it failed and why (exception e)
        print("[-] Failed to send notification email, " + str(e))


# def sendtweet(consumer_key, consumer_secret,access_token, access_token_secret,status_string):
#     try:
#         auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#         auth.set_access_token(access_token, access_token_secret)
#         api = tweepy.API(auth)
#         api.update_status(status_string)
#     except tweepy.error.TweepError:
#         print "[-]Error, invalid or expired twitter tokens, visit http://apps.twitter.com to retrieve or refresh them"

# def sendtext(message):
#     print "[+]Sending text message...."
#     try:
#         twilioCli = Client(accountSID, authToken)
#         twilioCli.messages.create(body=message, from_=twilioNumber, to=myNumber)
#     except Exception, e:
#         print "[-]Error " +e

def main():
    print("[+] Starting up monitor on " + url)
    print("[+] Email on change detect is set to " + str(notify))
    # print("[+] Tweeting is set to " + str(tweet))
    # print("[+] Text notifications set to " + str(text))

    latest = 106
    with requests.Session() as c:
        try:
            page1 = c.get(url, headers=HEADERS)  # base page that will be compared against
            latest = page1.json()["Items"][0]['ID']
            print("current latest id: %d" % latest)
            # latest = 0  # debug use
        except Exception as e:
            print("[-] Error Encountered during initial page retrieval: " + e)

        while 1:
            time.sleep(wait_time)  # wait between comparisons
            get_success = False
            while not get_success:
                try:
                    page2 = c.get(url, headers=HEADERS)  # page to be compared against page1 / the base page
                    current = page2.json()["Items"][0]['ID']
                    get_success = True
                except Exception as e:
                    print("[+] Error Encountered during comparison page retrieval: " + e)
                    time.sleep(wait_time)  # retry after sleep for a while

            # if page1.content == page2.content:  # if else statement to check if content of page remained same
            if latest == current:  # if else statement to check if content of page remained same
                print('[-] No Change Detected on ' + str(url) + "\n" + str(datetime.now()))
            else:
                status_string = 'Change Detected at ' + str(url) + "\n" + str(datetime.now())
                subject = page2.json()["Items"][0]["Title"]
                body = page2.json()["Items"][0]["Email"]["Body"]

                print("[+] " + status_string)
                latest = current
                if notify:
                    send_email(user, pwd, recipient, subject, body)  # send notification email
                else:
                    pass
                # if tweet:
                #     sendtweet(consumer_key, consumer_secret, access_token, access_token_secret, status_string)
                # else:
                #     pass
                # if text:
                #     sendtext(message)
                print('\n[+] Retrieving new base page and restarting\n')
                main()


if __name__ == '__main__':
    main()
