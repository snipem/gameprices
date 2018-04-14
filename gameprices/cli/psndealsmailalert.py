#!/usr/bin/env python

from gameprices.shops import psn
from gameprices.utils import utils
from xml.sax.saxutils import escape
import csv
import sys
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

import smtplib


def get_mail_config():
    mailConfig = {}
    mailConfig = utils.get_json_file("mailconfig.json")
    return mailConfig


def get_containers(dealContainerAlertsFilename):
    containers = []
    with open(dealContainerAlertsFilename) as csvfile:
        containersReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in containersReader:
            container = {}
            container['containerId'] = row[0]
            container['store'] = row[1]
            containers.append(container)

    return containers


def check_containers_and_generate_mail_body(containers):

    body = ""
    bodyElements = []

    for container in containers:
        containerId = container['containerId']
        store = container['store']

        items = psn._get_items_by_container(
            containerId, store, {"platform": "ps4"})

        if (items is None):
            utils.print_enc(
                "No items found for Container '" +
                containerId +
                "' in store " +
                store)
        else:

            body = "<table style=\"width: 100%; border-spacing: 0px;\" cellspacing=\"0\" cellpadding=\"0\" border=\"0\"><tbody><tr><td align=\"center\">"
            body = body + "<table width=\"620\" style=\"width: 620px;\" align=\"center\" cellspacing=\"0\" cellpadding=\"0\"><tbody>"
            body = body + ("<tr><td><p style=\"font-family: sans-serif; font-size: 1.0em; color: #FFFFFF; background-color: #5177B4; padding: 10px; "
                           "text-align: center; font-weight: bold; border-radius: 5px 5px 5px 5px;\">Deals in Store "
                           + store + " for container " + container["containerId"] + "</p></td></tr>")

            for subsetStartIdx in range(0, len(items), 3):
                itemsSubset = items[subsetStartIdx: subsetStartIdx + 3]

                bodyElements.append(
                    generate_body_itemsRow(
                        container, itemsSubset))

    body = body + "\n".join(bodyElements) + \
        "</tbody></table></td></tr></tbody></table>"

    return body


def send_mail(body):

    mailConfig = get_mail_config()

    msg = MIMEMultipart('alternative')
    msg['From'] = mailConfig["from"]
    msg['To'] = mailConfig["to"]
    msg['Subject'] = "Playstation Network Deals"

    if (sys.version_info[0] == 2):
        sendBody = body.encode('utf-8')
    else:
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


def generate_body_itemsRow(container, items):

    returnBody = []

    returnBody.append("<tr><td>")

    for item in items:
        returnBody.append(generate_body_item(container, item))

    returnBody.append("</td></tr>")

    return "\n".join(returnBody)


def generate_body_item(container, item):

    returnBody = []

    url = psn._get_store_url(item, container["store"])
    offerEndDate = psn._get_offer_end_date(item)
    itemName = escape(psn._get_name(item))

    returnBody.append(
        "<div style=\"float: left; padding: 10px; font-family: sans-serif; font-size: 0.8em; width: 180px;\">")
    returnBody.append(
        "<div style=\"height: 180px; min-height: 180px; max-height: 180px\"><a href=\"" +
        url +
        "\" target=\"_blank\"><img src='" +
        psn._get_image(item) +
        "' alt=\"" +
        itemName +
        "\" style=\"width: 180px; height:180px;\"/></a></div>")

    if offerEndDate is not None:
        returnBody.append(
            "<div style=\"background-color: #000000; color: white; font-size: 1.0em; padding: 5px; border-radius: 0px 0px 10px 0px; padding-left: 10px;\">Ends " +
            datetime.datetime.strftime(
                offerEndDate,
                "%d/%m/%Y") +
            "</div>")

    returnBody.append(
        "<div style=\"margin-top: 5px;\"><span style=\"margin-right: 10px; font-weight: bold; font-size: 1.4em; color: #CE1818;\">" +
        psn._get_display_price(
            item,
            container["store"]) +
        "</span><span>" +
        itemName +
        "</span></div>")
    returnBody.append("</div>")

    return "\n".join(returnBody)


def main():
    dealContainerAlertsFilename = "alert_deal_containers.csv"
    containers = get_containers(dealContainerAlertsFilename)

    body = check_containers_and_generate_mail_body(containers)
    utils.print_enc("Finished processing")

    if (len(body) > 0):
        send_mail(body)
        utils.print_enc("Mail was sent")
    else:
        utils.print_enc("No mail was sent")

    exit(0)


if __name__ == "__main__":
    main()
