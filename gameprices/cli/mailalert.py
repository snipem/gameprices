#!/usr/bin/env python

import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from gameprices.shops import psn
from gameprices.shops.eshop import Eshop
from gameprices.shops.psn import Psn
from gameprices.utils import utils


def get_mail_config():
    mail_config = utils.get_json_file("mailconfig.json")
    return mail_config


def get_alerts(alerts_filename):
    alerts = []
    with open(alerts_filename) as csv_file:
        alerts_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
        for row in alerts_reader:
            alert = {"cid": row[0], "price": row[1]}
            if len(row) >= 3:
                alert["store"] = row[2]
            # TODO wild hack and duplication of code
            elif "###" not in alert["cid"]:
                alert["store"] = psn._determine_store(alert["cid"])
            alerts.append(alert)

    return alerts


def set_alerts(filename, alerts):
    c = csv.writer(open(filename, "w"))
    for alert in alerts:
        c.writerow([alert["cid"], alert["price"], alert["store"]])


def alert_is_matched(alert, item):
    return item and float(item.prices[0].value) <= float(alert["price"])


def check_alerts_and_generate_mail_body(alerts):

    body_elements = []
    unmatched_alerts = list(alerts)

    for alert in alerts:
        cid = alert["cid"]
        store = alert["store"]

        if "###" in cid:
            shop = Eshop(store)
        else:
            shop = Psn(store)

        try:
            item = shop.get_item_by(item_id=cid)
        except Exception as e:
            print(
                "Did not find an item for id %s in store %s with exception '%s'"
                % (cid, store, e)
            )
            continue

        if alert_is_matched(alert, item):
            body_elements.append(generate_body_element(alert, item))

            unmatched_alerts.remove(alert)

    body = "\n".join(body_elements)

    return unmatched_alerts, body


def send_mail(body):

    mail_config = get_mail_config()

    msg = MIMEMultipart("alternative")
    msg["From"] = mail_config["from"]
    msg["To"] = mail_config["to"]
    msg["Subject"] = "PlayStation Network Price Drop"

    send_body = body

    html_mail = MIMEText(send_body, "html")
    msg.attach(html_mail)

    mail_server = smtplib.SMTP(mail_config["server"])
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login(mail_config["username"], mail_config["password"])
    mail_server.sendmail(mail_config["from"], msg["To"], msg.as_string())

    mail_server.quit()


def generate_body_element(alert, item):

    return_body = [
        "<p><img src='" + item.get_full_image() + "'/></p>",
        "<p>" + item.name + "</p>",
        "<p>Wished: " + str(alert["price"]) + "</p>",
        "<p>Is now: " + str(item.prices[0].value) + "</p>"
    ]

    return "\n".join(return_body)


def main():
    alerts_filename = "alerts.csv"
    alerts = get_alerts(alerts_filename)

    alerts_remaining, body = check_alerts_and_generate_mail_body(alerts)
    utils.print_enc("Finished processing")

    if len(body) > 0:
        send_mail(body)
        utils.print_enc("Mail was sent")
        set_alerts(alerts_filename, alerts_remaining)
    else:
        utils.print_enc("No mail was sent")

    exit(0)
