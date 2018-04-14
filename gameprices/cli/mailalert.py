#!/usr/bin/env python

from gameprices.utils import utils
from gameprices.shops.psn import Psn
from gameprices.shops.eshop import Eshop
from gameprices.shops import psn
import csv

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

import smtplib


def get_mail_config():
    mailConfig = {}
    mailConfig = utils.get_json_file("mailconfig.json")
    return mailConfig


def get_alerts(alertsFilename):
    alerts = []
    with open(alertsFilename) as csvfile:
        alertsreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in alertsreader:
            alert = {}
            alert['cid'] = row[0]
            alert['price'] = row[1]
            if len(row) >= 3:
                alert['store'] = row[2]
            # TODO wild hack and duplication of code
            elif "###" not in alert['cid']:
                alert['store'] = psn._determine_store(alert["cid"])
            alerts.append(alert)

    return alerts


def set_alerts(filename, alerts):
    c = csv.writer(open(filename, "w"))
    for alert in alerts:
        c.writerow([alert['cid'], alert['price'], alert['store']])


def alert_is_matched(alert, item):
    return item and float(item.prices[0].value) <= float(alert['price'])


def check_alerts_and_generate_mail_body(alerts):

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
            print(
                "Did not find an item for id %s in store %s with exception '%s'" %
                (cid, store, e))
            continue

        if (alert_is_matched(alert, item)):
            bodyElements.append(generate_body_element(alert, item))

            unmatchedAlerts.remove(alert)

    body = "\n".join(bodyElements)

    return unmatchedAlerts, body


def send_mail(body):

    mailConfig = get_mail_config()

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


def generate_body_element(alert, item):

    returnBody = []
    # store = alert['store']
    returnBody.append("<p><img src='" + item.get_full_image() + "'/></p>")
    returnBody.append("<p>" + item.name + "</p>")
    returnBody.append("<p>Wished: " + str(alert['price']) + "</p>")
    returnBody.append("<p>Is now: " + str(item.prices[0].value) + "</p>")

    return "\n".join(returnBody)


def main():
    alertsFilename = "alerts.csv"
    alerts = get_alerts(alertsFilename)

    alertsRemaining, body = check_alerts_and_generate_mail_body(alerts)
    utils.print_enc("Finished processing")

    if (len(body) > 0):
        send_mail(body)
        utils.print_enc("Mail was sent")
        set_alerts(alertsFilename, alertsRemaining)
    else:
        utils.print_enc("No mail was sent")

    exit(0)
