#!/usr/bin/env python3
# Copyright (c) 2019, Gouasmia Zakaria
# All rights reserved.


import smtplib
import sys


def load_emails(filename):
    """
    Load the target email addresses from a file.
    """
    emails = []
    print('[*] Loading email addresses.')
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('#'):
                continue
            if line == '':
                continue

            emails.append(line)

    return emails


def usage():
    """
    Print usage statement and exit.
    """
    print('Usage: smtp_enum.py mx_server port email_file')
    sys.exit()


if __name__ == '__main__':
    """
    Enumerate the target email addresses.

    Use the EXPN, VRFY, or RCPT TO method to enumerate email addresses.
    """ 
    if len(sys.argv) != 4:
        usage()

    debug = False
    helo = 'mail.example.com'
    mail_from = 'user@example.com'
    mx = sys.argv[1]
    port = int(sys.argv[2])
    emails = load_emails(sys.argv[3])

    try:
        smtp = smtplib.SMTP()
        smtp.set_debuglevel(debug)

        smtp.connect(mx, port)
        smtp.ehlo(helo)

        if smtp.has_extn('vrfy') is True:
            print('[*] Using VRFY to enumerate email addresses.')
            check = smtp.vrfy
        elif smtp.has_extn('expn') is True:
            print('[*] Using EXPN to enumerate email addresses.')
            check = smtp.expn
        else:
            print('[*] Using RCPT to enumerate email addresses.')
            smtp.mail(mail_from)
            check = smtp.rcpt

        for email in emails:
            code, _ = check(email)
            if code == 250:
                print('[+] {0}'.format(email))
            else:
                print('[-] {0}'.format(email))

        smtp.quit()

    except smtplib.SMTPDataError as e:
        print('[-] {0}'.format(str(e[1])))

    except smtplib.SMTPServerDisconnected as e:
        print('[-] {0}'.format(str(e)))

    except smtplib.SMTPConnectError as e:
        print('[-] {0}'.format(str(e[1])))

    except smtplib.SMTPSenderRefused as e:
        print('[-] {0}'.format(str(e)))
