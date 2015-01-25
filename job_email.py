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

def get_csv_rows():
	with open(data_file + '.csv') as file:
		csvfile = csv.DictReader(file)
		return [row for row in csvfile]		

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
	
		
def num_lines(file):	
	lines = [1 for character in file if character is '\r' or '\n']
	number_lines = reduce(lambda x,y: x+y, lines, 0)
	return number_lines
	
def main():
	#get all the unique emails from the csv file
	csvrows = get_csv_rows()
	email_targets = get_email_targets(csvrows)
	
	Past_emails_file = open(data_file + ".txt","a+")
	start = num_lines(Past_emails_file)
	end = start + 300
	
	print start
	
	#login to server once
	# server = smtplib.SMTP('smtp.gmail.com', 587)
	# server.starttls()
	# server.login(gmail_name,gmail_pw)
	
	# for i in range(start,end):
		# to_addr = email_targets[i].email
		# name = email_targets[i].name
		# company_name = email_targets[i].sbc
		# # send_email(to_addr, gmail_name + '@gmail.com', name, company_name, server)
		# Past_emails_file.write(to_addr)
		# Past_emails_file.write('\n')
		# print company_name
		
	#quit the server
	# server.quit()
	#close the file
	Past_emails_file.close()

if __name__=='__main__': main()
