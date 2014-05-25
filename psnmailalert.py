#!/usr/bin/env python

from psnpricealert.psn import psn
from psnpricealert.utils import utils
import csv
import sys

if (sys.version_info[0] == 2):
	from email.MIMEMultipart import MIMEMultipart
	from email.MIMEBase import MIMEBase
	from email.MIMEText import MIMEText
else:
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
			alert['store'] = row[2]
			alerts.append(alert)

	return alerts

def setAlerts(filename, alerts):
	c = csv.writer(open(filename, "w"))
	for alert in alerts:
		c.writerow([alert['cid'],alert['price'],alert['store']])


def alertIsMatched(alert, item):
	return float(psn.getPrice(item)) <= float(alert['price'])

def checkAlertsAndGenerateMailBody(alerts):
	
	bodyElements = []
	unmatchedAlerts = list(alerts)

	for alert in alerts:
		item = psn.getItemForCid(alert['cid'],alert['store'])
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
	msg['Subject'] = "Playstation Network Price Drop"

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
	mailServer.login(mailConfig["username"],mailConfig["password"])
	mailServer.sendmail(mailConfig["from"], msg['To'], msg.as_string())

	mailServer.quit()


def generateBodyElement(alert, item):

	returnBody = []
	returnBody.append("<p><img src='"+psn.getImage(item)+"'/></p>")
	returnBody.append("<p>"+psn.getName(item)+"</p>")
	returnBody.append("<p>Wished: "+str(alert['price'])+"</p>")
	returnBody.append("<p>Is now: "+str(psn.getPrice(item))+"</p>")

	return "\n".join(returnBody)

def main():
	alertsFilename = "alerts.csv"
	alerts = getAlerts(alertsFilename)

	alertsRemaining, body = checkAlertsAndGenerateMailBody(alerts)

	if (len(body) > 0):
		sendMail(body)
		utils.print_enc("Mail was sent")
		setAlerts(alertsFilename,alertsRemaining)
	
	exit(0)


if __name__ == "__main__":
    main()