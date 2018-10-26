#!/usr/bin/env python

#
# hmf.py
# 
# Command line tool for HMF stuff.  There's gonna be lots, you know.
# 
# hmf print-booths booths2017.txt
# 

import sys


def boothize(fields):
    booth = fields[0].strip()
    return "            <h1>%s</h1>" % booth


def slotize(fields):
    booth = fields[0].strip()
    activity = fields[1].strip()
    slot = fields[2].strip()

    requested = fields[3].strip()
    return "            <h2>%s (%s)</h2><h2>%s (%s needed)</h2>" % (activity, booth, slot, requested)


def volunteerize(fields):
    volunteer = ""
    if len(fields) > 4:
        volunteer = fields[4]
    if volunteer == "":
        volunteer = "&nbsp;" * 80
    return '            <div class="volunteer">%s</div>' % volunteer


def main(argv):

    infile = argv[1]

    print "<html>"

    print """    <head>
    <style type="text/css">
        body {
            font-family: Arial, sans serif;
            width: 800px;
            text-align: center;
            border: 1px solid #bbb;
            font-size: 20px;
        }
        h1 {
            width: 100%;
            font-weight: bold;
            font-size: 32px;
            margin-top: 2em;
            margin-bottom: 1em;
        }
        h2 {
            width: 100%;
            font-weight: bold;
            font-size: 20px;
            font-color: #bbb;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }
        .volunteer {
            width: 50%;
            text-decoration: underline;
            margin: auto;
            min-height: 50px;
            padding: 4px;
        }
        @media print {
            .booth {page-break-before: always;}
        }
    </style>
    </head>
    <body>"""

    boothopentag = '        <div class="booth">'
    boothclosetag = ""  # Close is set later

    with open(infile, "r") as f:
        booth = ""
        slot = ""
        f.next()
        for line in f:
            if line.strip() == "":
                continue
            fields = line.split("\t")
            if fields[0].strip() != booth:

                # It's a new booth, so close the old and open a new
                print boothclosetag
                boothclosetag = "        </div>"
                print boothopentag

                booth = fields[0].strip()
                slot = '%s %s' % (fields[2].strip(), fields[1].strip())

                print boothize(fields)
                print slotize(fields)
                print volunteerize(fields)

            elif "%s %s" % (fields[2].strip(), fields[1].strip()) != slot:

                slot = '%s %s' % (fields[2].strip(), fields[1].strip())
                print slotize(fields)
                print volunteerize(fields)

            else:

                print volunteerize(fields)

    print boothclosetag
    print "    </body>\n</html>"

if __name__ == "__main__":
    main(sys.argv)
