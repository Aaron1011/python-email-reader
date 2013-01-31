import imaplib
import time
import getpass
import email
import socket
import pyttsx
from email.parser import HeaderParser


def setup():
    global TTS
    global PARSER
    global IMAP_SERVER
    global MAIL_SERVERS

    IMAP_SERVER = None

    PARSER = HeaderParser()

    TTS = pyttsx.init()
    TTS.say(' ')
    TTS.runAndWait()

    MAIL_SERVERS = {'gmail.com': {'Server': str(socket.gethostbyname('imap.gmail.com'))},
                    'yahoo.com': {'Server': str(socket.gethostbyname('imap.mail.yahoo.com'))},
                    'aol.com': {'Server': str(socket.gethostbyname('imap.aol.com'))}}


def getLogin():
    username = raw_input("Email address: ")
    password = getpass.getpass()
    return username, password

def getMessages(server):
    server.select()
    _, data = server.search(None, 'All')
    return data[0].split()


def main():

    setup()
    global TTS
    global PARSER
    global IMAP_SERVER
    global MAIL_SERVERS

    print("Please enter in your email account details.")
    username, password = getLogin()
    username2 = username.split("@")
    while len(username2) != 2:
        print("Please enter a valid email address.")
        username, password = getLogin()
        username2 = username.split("@")

    if username2[1] not in MAIL_SERVERS:
        raise NotImplementedError("Support for your email provider has not been implemented yet")

    IMAP_SERVER = imaplib.IMAP4_SSL(MAIL_SERVERS[username2[1]]["Server"], MAIL_SERVERS[username2[1]].get("Port", 993))
    IMAP_SERVER.login(username, password)

    read = set()

    while True:
        ids = getMessages(IMAP_SERVER)
        for email_id in ids:
            resp, data = IMAP_SERVER.fetch(email_id, '(RFC822)')
            mail = email.message_from_string(data[0][1])
            for part in mail.walk():
                if part.get_content_maintype() == 'multipart':
                    continue

                if part.get_content_subtype() != 'plain':
                    continue

                payload = part.get_payload()
                if not payload in read:
                    print "New message"
                    read.add(payload)
                    msg = PARSER.parsestr(data[0][1])
                    TTS.say("New message from " + msg['From'])
                    TTS.say("Subject: " + msg['Subject'])
                    TTS.say(payload)
                    TTS.runAndWait()
                time.sleep(2)

        time.sleep(1)

if __name__ == "__main__":
    main()
