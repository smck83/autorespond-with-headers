import imaplib
import sys
import mailparser
import smtplib
from email.message import EmailMessage
import time
import datetime
import os

if 'IMAP_SERVER' in os.environ:  
    IMAPserver = os.environ['IMAP_SERVER']
if 'IMAP_USERNAME' in os.environ:  
    IMAPuser = os.environ['IMAP_USERNAME']
if 'IMAP_PASSWORD' in os.environ:  
    IMAPpassword = os.environ['IMAP_PASSWORD']
if 'IMAP_FOLDERNAME' in os.environ:  
    IMAPfolderName = os.environ['IMAP_FOLDERNAME']
else:
    IMAPfolderName = 'Inbox'

if 'SMTP_SERVER' in os.environ:  
    SMTPserver = os.environ['SMTP_SERVER']
else:
    SMTPserver = IMAPserver
if 'SMTP_USERNAME' in os.environ:  
    SMTPuser = os.environ['SMTP_USERNAME']
else:
    SMTPuser = IMAPuser
if 'SMTP_PASSWORD' in os.environ:  
    SMTPpassword  = os.environ['SMTP_PASSWORD']
else:
    SMTPpassword = IMAPpassword
if 'SMTP_SENDER' in os.environ:  
    SMTPsender  = os.environ['SMTP_SENDER']
else:
    SMTPsender = f"Autoresponse <{IMAPuser}>"
if 'SCHEDULE' in os.environ:  
    recheckEveryXSeconds  = int(os.environ['SCHEDULE'])
else:
    recheckEveryXSeconds = 30

def sendEmail(receivers,subject,emailbody):
    msg = EmailMessage()
    msg['Subject'] = f"RE: {subject} | ({receivers})"
    msg['From'] = SMTPsender
    msg['To'] = [receivers]
    msg['Bcc'] = ['response@dmarcvalidator.com']
    msg.set_content(emailbody)

    s = smtplib.SMTP(SMTPserver,25)
    try:
        s.connect(SMTPserver,587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(SMTPuser, SMTPpassword)
        s.send_message(msg)

    except Exception as e:
        s.quit()
        print(datetime.datetime.now(),"Something went wrong:",e)
    else:
        print(datetime.datetime.now(),"Success! - E-mail response sent to ",receivers)
        s.quit()



#socket.setdefaulttimeout(3) # Set socket default timeout




# Connect to an IMAP server
def connect(server, user, password):
    try: 
      m = imaplib.IMAP4_SSL(server)
      m.login(user, password)
    except Exception as e:
      print(datetime.datetime.now(),"IMAP Connection Error:",str(e).replace("b'",""))
      sys.exit()
    else:
      print(datetime.datetime.now(),"IMAP Connected sucessfully, checking email")
      m.select(IMAPfolderName) # Look at e-mails in folder URLs
   
    return m

def get_email_headers(con,emailid):
    resp, data = con.fetch(emailid, "(BODY.PEEK[HEADER])")
    email_body = data[0][1]
    mail = mailparser.parse_from_bytes(email_body)
    return mail



def autorespond_to_unread_email(imapserver:str=IMAPserver,username:str=IMAPuser,password:str=IMAPpassword):
    emailResults = None

    con = connect(imapserver,username,password)
    resp, items = con.search(None,'UNSEEN') # Find unread e-mails only
    
    items = items[0].split()
    print(datetime.datetime.now(),"Found e-mail to",len(items),f"in folder \{IMAPfolderName}:")

    if len(items) > 0:
        for emailid in items:
            print(datetime.datetime.now(),"Starting to process e-mails")
            con.store(emailid, '+FLAGS', '(\\Seen)')  # Mark e-mail as read so it won't be picked up next time
            emailResults = get_email_headers(con, emailid)
            messageBody = emailResults.ARC_Authentication_Results + "\r\n\r\n" + "Please see your headers below:\r\n\r\n" + str(emailResults.message_as_string)
            sendEmail(emailResults._from[0][1],emailResults.subject,messageBody)

        
    #con.close
    return emailResults



while 1 != -1:
    autorespond_to_unread_email()
    print(f"{datetime.datetime.now()} Waiting {recheckEveryXSeconds} seconds")
    time.sleep(recheckEveryXSeconds)








