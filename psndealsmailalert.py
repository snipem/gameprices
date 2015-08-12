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

def getContainers(dealContainerAlertsFilename):
	containers = []
	with open(dealContainerAlertsFilename) as csvfile:
		containersReader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in containersReader:
			container = {}
			container['containerId'] = row[0]
			container['store'] = row[1]
			containers.append(container)

	return containers


def checkContainersAndGenerateMailBody(containers):


	body = ""
	bodyElements = []

	for container in containers:
		containerId = container['containerId']
		store = container['store']

		items = psn.getItemsByContainer(containerId, store, {"platform": "ps4"})

		if (items == None):
			utils.print_enc("No items found for Container '"+containerId+"' in store "+store)
		else:

			body = "<div style=\"width: 800px; margin: auto; display: table; border: 1px solid lightgray; padding: 10px;\">\n"
			body = body + ("<p style=\"font-family: sans-serif; font-size: 1.0em; color: #FFFFFF; background-color: #5177B4; padding: 10px; "
						   "text-align: center; font-weight: bold; border-radius: 5px 5px 5px 5px;\">Deals in Store "
						   + store  + " for container " + container["containerId"] + "</p>\n")

			itemNum = 0
			for item in items:

				if itemNum % 3 != 0:
					startNewRow = False
				else:
					startNewRow = True

				bodyElements.append(generateBodyElement(container, item, startNewRow))

				itemNum = itemNum + 1


	body = body + "\n".join(bodyElements) + "</div>"

	return body

def sendMail(body):

	mailConfig = getMailConfig()

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
	mailServer.login(mailConfig["username"],mailConfig["password"])
	mailServer.sendmail(mailConfig["from"], msg['To'], msg.as_string())

	mailServer.quit()


def generateBodyElement(container, item, startNewRow):

	returnBody = []

	startNewRowHtml = ""

	if startNewRow:
		startNewRowHtml = "clear: left;"

	url = psn.getStoreUrl(item, container["store"])

	returnBody.append("<div style=\"float: left; box-sizing: border-box; padding: 10px; font-family: sans-serif; font-size: 0.8em; width: 260px; " + startNewRowHtml + "\">")
	returnBody.append("<div><a href=\"" + url + "\" target=\"_new\"><img src='"+psn.getImage(item)+"'/></a></div>")
	returnBody.append("<div style=\"margin-top: 5px;\"><span style=\"margin-right: 10px; font-weight: bold; font-size: 1.4em; color: #CE1818;\">"
					  + str(psn.getPrice(item)) + "</span><span>"+psn.getName(item)+"</span></div>")
	returnBody.append("</div>")

	return "\n".join(returnBody)

def main():
	dealContainerAlertsFilename = "alert_deal_containers.csv"
	containers = getContainers(dealContainerAlertsFilename)

	body = checkContainersAndGenerateMailBody(containers)
	utils.print_enc("Finished processing")
	
	if (len(body) > 0):
		sendMail(body)
		utils.print_enc("Mail was sent")
	else:
		utils.print_enc("No mail was sent")
	
	exit(0)


if __name__ == "__main__":
    main()