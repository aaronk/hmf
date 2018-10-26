#!/usr/bin/env python

#
# hmf.py
# 
# Command line tool for HMF stuff.  There's gonna be lots, you know.
# 
# hmf print-booths booths2017.txt
# 

import sys
import smtplib
from time import sleep


def main(argv):

    infile = argv[1]
    maildata = {}

    with open(infile, "r") as f:
        f.next()
        for line in f:
            if line.strip() == "":
                continue
            fields = line.split("\t")
            email = fields[5].strip()
            name = fields[4].strip()
            booth = fields[0].strip()
            activity = fields[1].strip()
            slot = fields[2].strip()
            if fields[7].strip() != "":
                slot += " (%s)" % fields[7].strip()

            if email != "" and email != "#N/A":
                if email not in maildata:
                    maildata[email] = {}
                if name not in maildata[email]:
                    maildata[email][name] = {}
                if booth not in maildata[email][name]:
                    maildata[email][name][booth] = {}
                if activity not in maildata[email][name][booth]:
                    maildata[email][name][booth][activity] = []
                maildata[email][name][booth][activity].append(slot)

    server = smtplib.SMTP_SSL('smtp.gmail.com', '465')
    server.login('aaron.kitzmiller@gmail.com', 'hnzmabbkaucddlhj')
    for email, data in maildata.iteritems():
        mailto = email
        mailfrom = "aaron.kitzmiller@gmail.com"
        mailsubject = "Fair booth reminder"
        for name, namedata in data.iteritems():
            mailtext = """Hi, %s 
This is Aaron Kitzmiller, the Harvest Moon Fair guy from First Parish, and below is what I have down for you at the fair.

Send me an email (fair@firstparish.info) if this is incorrect.

""" % name
            for booth, boothdata in namedata.iteritems():
                mailtext = mailtext + "    %s\n" % booth
                for activity, slots in boothdata.iteritems():
                    for slot in slots:
                        mailtext = mailtext + "        %s  %s\n" % (activity, slot)
            print "To: %s" % mailto
            print "From: %s" % mailfrom
            print "Subject: %s" % mailsubject
            print mailtext
            print "\n\n"
            msg = "To: %s\r\nFrom: %s\r\nSubject: %s\r\n\r\n%s" % ("aaron.kitzmiller@gmail.com", mailfrom, mailsubject, mailtext)
            server.sendmail(mailfrom, [mailto, "fair@firstparish.info"], msg)
            sleep(5)

    server.quit()


if __name__ == "__main__":
    main(sys.argv)
