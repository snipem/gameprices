from psnpricealert.psn import psn
from psnpricealert.utils import utils
from mailer import Mailer
from mailer import Message
import csv

def getMailConfig():
	mailConfig = {}
	mailConfig = utils.getJsonFile("mailconfig.json")
	return mailConfig

def getAlerts(alertsFilename):
	alerts = []
	with open(alertsFilename, 'rb') as csvfile:
		alertsreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in alertsreader:
			alert = {}
			alert['cid'] = row[0]
			alert['price'] = row[1]
			alert['store'] = row[2]
			alerts.append(alert)

	return alerts

def setAlerts(filename, alerts):
	c = csv.writer(open(filename, "wb"))
	for alert in alerts:
		c.writerow([alert['cid'],alert['price'],alert['store']])


def alertIsMatched(alert, item):
	return float(psn.getPrice(item)) <= float(alert['price'])

def checkAlertsAndGenerateMailBody(alerts):
	
	bodyElements = []
	returnAlerts = alerts

	for alert in alerts:
		item = psn.getItemForCid(alert['cid'],alert['store'])
		if (alertIsMatched(alert, item)):
			bodyElements.append(generateBodyElement(alert, item))
			
			#TODO remove matched alerts
			#returnAlerts.remove(alert)

	body = "\n".join(bodyElements)

	return returnAlerts, body

def sendMail(body):

	mailConfig = getMailConfig()
	message = Message(From=mailConfig["from"],
	                  To=mailConfig["to"],
	                  charset="UTF-8")

	message.Subject = "PlaystationNetwork Price Drop"
	message.Html = body

	sender = Mailer(mailConfig["server"])
	sender.login(mailConfig["username"],mailConfig["password"])
	sender.send(message)


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