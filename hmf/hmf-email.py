#!/usr/bin/env python3

#
# hmf.py
#
# Command line tool for HMF stuff.  There's gonna be lots, you know.
#
# hmf booths2017.txt
#

import sys
import smtplib
from time import sleep

EMAIL_COL = 5
NAME_COL = 4
BOOTH_COL = 0
ACTIVITY_COL = 1
DAY_COL = 2
SLOT_COL = 3

def main(argv):

    infile = argv[1]
    maildata = {}

    with open(infile, "r") as f:
        next(f)
        for line in f:
            if line.strip() == "":
                continue
            fields = line.split("\t")
            email = fields[EMAIL_COL].strip()
            name = fields[NAME_COL].strip()
            booth = fields[BOOTH_COL].strip()
            activity = fields[ACTIVITY_COL].strip()
            day = fields[DAY_COL].strip()
            slot = fields[SLOT_COL].strip()
            if fields[7].strip() != "":
                slot += " (%s)" % fields[7].strip()

            slot_str = "%s %s" % (day, slot)

            if email != "" and email != "#N/A":
                if email not in maildata:
                    maildata[email] = {}
                if name not in maildata[email]:
                    maildata[email][name] = {}
                if booth not in maildata[email][name]:
                    maildata[email][name][booth] = {}
                if activity not in maildata[email][name][booth]:
                    maildata[email][name][booth][activity] = []
                maildata[email][name][booth][activity].append(slot_str)

    server = smtplib.SMTP_SSL('smtp.gmail.com', '465')
    server.login('aaron.kitzmiller@gmail.com', 'fphlfyeslquijycp')
    for email, data in maildata.items():
        mailto = email
        mailfrom = "aaron.kitzmiller@gmail.com"
        mailsubject = "Fair booth reminder"
        for name, namedata in data.items():
            mailtext = """Hi, %s
This is Aaron Kitzmiller, the Harvest Moon Fair guy from First Parish, and below is what I have down for you at the fair.  I've probably sent you something already, so you don't need to respond unless something is wrong. Also, don't worry about the wide ranges for general Thursday and Friday shifts.  Whenever you can make it is good.

Send me an email (fair@firstparish.info) if this is incorrect.

""" % name
            for booth, boothdata in namedata.items():
                mailtext = mailtext + "    %s\n" % booth
                for activity, slots in boothdata.items():
                    for slot in slots:
                        mailtext = mailtext + "        %s  %s\n" % (activity, slot)
            print("To: %s" % mailto)
            print("From: %s" % mailfrom)
            print("Subject: %s" % mailsubject)
            print(mailtext)
            print("\n\n")
            msg = "To: %s\r\nFrom: %s\r\nSubject: %s\r\n\r\n%s" % ("aaron.kitzmiller@gmail.com", mailfrom, mailsubject, mailtext)
            server.sendmail(mailfrom, [mailto, "fair@firstparish.info"], msg)
            sleep(5)

    server.quit()


if __name__ == "__main__":
    main(sys.argv)
