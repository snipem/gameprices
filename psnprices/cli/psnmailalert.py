#!/usr/bin/env python

from psnprices.utils import utils
from psnprices.shops.psn import Psn
from psnprices.shops.eshop import Eshop
from psnprices.shops import psn
import csv
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

import smtplib


def getMailConfig():
    mailConfig = {}
    mailConfig = utils.getJsonFile("mailconfig.json")
    return mailConfig


def getAlerts(alertsFilename):
    alerts = []
    with open(alertsFilename) as csvfile:
        alertsreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in alertsreader:
            alert = {}
            alert['cid'] = row[0]
            alert['price'] = row[1]
            if len(row) >= 3:
                alert['store'] = row[2]
            #TODO wild hack and duplication of code
            elif "###" not in alert['cid']:
                alert['store'] = psn._determineStore(alert["cid"])
            alerts.append(alert)

    return alerts


def setAlerts(filename, alerts):
    c = csv.writer(open(filename, "w"))
    for alert in alerts:
        c.writerow([alert['cid'], alert['price'], alert['store']])


def alertIsMatched(alert, item):
    return item and float(item.prices[0].value) <= float(alert['price'])


def checkAlertsAndGenerateMailBody(alerts):

    bodyElements = []
    unmatchedAlerts = list(alerts)

    for alert in alerts:
        cid = alert['cid']
        store = alert['store']

        if "###" in cid:
            shop = Eshop(store)
        else:
            shop = Psn(store)

        try:
            item = shop.get_item_by(id=cid)
        except Exception as e:
            print("Did not find an item for id %s in store %s with exception '%s'" % (cid, store, e)) 
            continue

        if (alertIsMatched(alert, item)):
            bodyElements.append(generateBodyElement(alert, item))

            unmatchedAlerts.remove(alert)

    body = "\n".join(bodyElements)

    return unmatchedAlerts, body


def sendMail(body):

    mailConfig = getMailConfig()

    msg = MIMEMultipart('alternative')
    msg['From'] = mailConfig["from"]
    msg['To'] = mailConfig["to"]
    msg['Subject'] = "PlayStation Network Price Drop"

    sendBody = body

    htmlMail = MIMEText(sendBody, 'html')
    msg.attach(htmlMail)

    mailServer = smtplib.SMTP(mailConfig["server"])
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(mailConfig["username"], mailConfig["password"])
    mailServer.sendmail(mailConfig["from"], msg['To'], msg.as_string())

    mailServer.quit()


def generateBodyElement(alert, item):

    returnBody = []
    store = alert['store']
    returnBody.append("<p><img src='"+item.get_full_image()+"'/></p>")
    returnBody.append("<p>"+item.name+"</p>")
    returnBody.append("<p>Wished: "+str(alert['price'])+"</p>")
    returnBody.append("<p>Is now: "+str(item.prices[0].value)+"</p>")

    return "\n".join(returnBody)


def main():
    alertsFilename = "alerts.csv"
    alerts = getAlerts(alertsFilename)

    alertsRemaining, body = checkAlertsAndGenerateMailBody(alerts)
    utils.print_enc("Finished processing")

    if (len(body) > 0):
        sendMail(body)
        utils.print_enc("Mail was sent")
        setAlerts(alertsFilename, alertsRemaining)
    else:
        utils.print_enc("No mail was sent")

    exit(0)
