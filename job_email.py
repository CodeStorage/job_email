import csv
import sys
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.multipart import MIMEMultipart

#global configuration variables
data_file = sys.argv[1]
gmail_name = 'diemerEE'
gmail_pw = 'XXXXXX' #dummy password for public exposure
resume_filename = "ChrisDiemer_Resume.pdf"

class email_target:
	def __init__(self, name, email, sbc):
		self.name = name
		self.email = email
		self.sbc = sbc

#get data from a csv file
#@param filename is the name of a csv file in the working directory
#returns a list of lists with key-value pair elements
def get_csv_rows(filename):
	with open(filename) as file:
		csvfile = csv.DictReader(file)
		return [row for row in csvfile]		

#get unique email targets from a key-value pair list 
#@param rows is a list of lists with key-value pair elements
#return unique email targets
def get_email_targets(rows):
	email_targets = []
	for row in rows:
		unique = True
		new_target = email_target(*[row['Contact Name'], row['Contact Email'], row['SBC']])
		for target in email_targets:
			if target.email.lower() == new_target.email.lower():
				unique = False
		if(unique):
			email_targets.append(new_target)
	return email_targets
	
#send an email with a predefined subject, body, and attachment.
def send_email(to_addr, from_addr, name, company_name, server):
	message = """
Hello %s,

My name is Chris Diemer and I am interested in pursuing a career with %s as an Electrical Engineer. 
I am a U.S. citizen and have been working the past year as an Electrical Engineering intern at a
small aerial imaging company. I have experience programming complex systems and I deal with hardware 
and circuit schematics on a daily basis. I have attached my resume, please contact me if you have 
any questions or opportunities. 

Thank you for your time,
Chris Diemer
	""" % (name, company_name)
	mime_message = MIMEMultipart(
	From=from_addr,
	To=to_addr,
	Date=formatdate(localtime=True)
	)
	mime_message['Subject'] = 'Looking for career opportunities at %s' % company_name
	mime_message.attach(MIMEText(message))
		
	attach_file=MIMEApplication(open(resume_filename, "rb").read())
	attach_file.add_header('Content-Disposition','attachment', filename=resume_filename)
	mime_message.attach(attach_file)
	
	problems = server.sendmail(from_addr, to_addr, mime_message.as_string())
	

#get the number of lines in a text file using list comprehension	
def num_lines(file):	
	lines = [1 for character in file if character is '\n' or '\r']
	number_lines = reduce(lambda x,y: x+y, lines, 0)
	return number_lines
	
def main():
	#get all the unique emails from the csv file
	csvrows = get_csv_rows(data_file + '.csv')
	email_targets = get_email_targets(csvrows)
	
	#find the number of emails sent from this data set already
	#only 500 emails can be sent through gmail per day without flagging
	#appears to only send about 109 per run before disconnecting
	Past_emails_file = open(data_file + ".txt","a+")
	start = num_lines(Past_emails_file)
	end = start + int(sys.argv[2])
	
	#login to server once
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(gmail_name,gmail_pw)
	
	for i in range(start,end):
		send_email(email_targets[i].email, gmail_name + '@gmail.com', email_targets[i].name, email_targets[i].sbc, server)
		Past_emails_file.write(email_targets[i].email)
		Past_emails_file.write('\n')
		
	#quit the server
	server.quit()
	#close the file
	Past_emails_file.close()

if __name__=='__main__': main()
