#!/usr/bin/env python
import smtplib
import os
import getpass
import sys
import thread
import subprocess
import re
import glob
import random
import time
import base64
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

message_flag="plain"

from src.core.setcore import *

definepath = os.getcwd()

# DEFINE SENDMAIL CONFIG and WEB ATTACK
sendmail=0

# need to do this if we aren't in the SET root
if "program_junk" in definepath:
	definepath = definepath.replace("src/program_junk/web_clone", "")

sendmail_file=file("%s/config/set_config" % (definepath),"r").readlines()
for line in sendmail_file:
        # strip carriage returns
        line=line.rstrip()
        match=re.search("SENDMAIL=",line)
        if match: 
                # if match and if line is flipped on continue on
                if line == ("SENDMAIL=ON"):
                        print_info("Sendmail is a Linux based SMTP Server, this can be used to spoof email addresses.")
                        print_info("Sendmail can take up to three minutes to start")
                        print_status("Sendmail is set to ON")
                        sendmail_choice = yesno_prompt(["1"], "Start Sendmail? [yes|no]")
                        # if yes, then do some good stuff
                        if sendmail_choice == "YES":
                                print_info("Sendmail can take up to 3-5 minutes to start")
                                if os.path.isfile("/etc/init.d/sendmail"):
                                        subprocess.Popen("/etc/init.d/sendmail start", shell=True).wait()
                                if not os.path.isfile("/etc/init.d/sendmail"):
                                        pause = raw_input("[!] Sendmail was not found. Try again and restart.")
                                        sys.exit()
                                smtp = ("localhost")
                                port = ("25")
                                # Flip sendmail switch to get rid of some questions             
                                sendmail=1 
                                # just throw user and password to blank, needed for defining below
                                user=''
                                pwd=''

        # Search for SMTP provider we will be using
        match1=re.search("EMAIL_PROVIDER=", line)
        if match1:

                # if we hit on EMAIL PROVIDER
                email_provider=line.replace("EMAIL_PROVIDER=", "").lower()

                # support smtp for gmail
                if email_provider == "gmail":
                        if sendmail == 0:
                                smtp = ("smtp.gmail.com")
                                port = ("587")

                # support smtp for yahoo
                if email_provider == "yahoo":
                        if sendmail == 0:
                                smtp = ("smtp.mail.yahoo.com")
                                port = ("25")

                # support smtp for hotmail
                if email_provider == "hotmail":
                        if sendmail == 0:
                                smtp = ("smtp.hotmail.com")
                                port = ("25")

            
print ("""
   Social Engineer Toolkit Mass E-Mailer

   There are two options on the mass e-mailer, the first would
   be to send an email to one individual person. The second option
   will allow you to import a list and send it to as many people as
   you want within that list.

   What do you want to do:

    1.  E-Mail Attack Single Email Address
    2.  E-Mail Attack Mass Mailer
    
    99. Return to main menu.
   """)

option1=raw_input(setprompt(["5"], ""))

if option1 == 'exit':
        exit_set()

# single email
if option1 == '1':
   to = raw_input(setprompt(["1"], "Send email to"))

# mass emailer
if option1 == '2':
   print ("""
 The mass emailer will allow you to send emails to multiple 
 individuals in a list. The format is simple, it will email
 based off of a line. So it should look like the following:

 john.doe@ihazemail.com
 jane.doe@ihazemail.com
 wayne.doe@ihazemail.com

 This will continue through until it reaches the end of the
 file. You will need to specify where the file is, for example
 if its in the SET folder, just specify filename.txt (or whatever
 it is). If its somewhere on the filesystem, enter the full path, 
 for example /home/relik/ihazemails.txt
""")
   filepath = raw_input(setprompt(["1"], "Path to the file to import into SET"))

# exit mass mailer menu
if option1 == '99': 
        print "Returning to main menu..."
        sys.exit(1)
print ("""\n  1. Use a %s Account for your email attack.\n  2. Use your own server or open relay\n""" % (email_provider)) 
relay = raw_input(setprompt(["1"], ""))

counter=0
# Specify mail Option Here
if relay == '1':
   user = raw_input(setprompt(["1"], "Your %s email address" % (email_provider)))
   user1 = user
   pwd = getpass.getpass("Email password: ")
   #smtp = ("smtp.gmail.com")
   #port = ("587")

# Specify Open-Relay Option Here
if relay == '2':
   user1 = raw_input(setprompt(["1"], "From address (ex: moo@example.com)"))

   if sendmail==0:
      user = raw_input(setprompt(["1"], "Username for open-relay [blank]"))
      pwd =  getpass.getpass("Password for open-relay [blank]: ")
      #if user == '':
       #  counter=1
   if sendmail==0:
      smtp = raw_input(setprompt(["1"], "SMTP email server address (ex. smtp.youremailserveryouown.com)"))
      port = raw_input(setprompt(["1"], "Port number for the SMTP server [25]"))
      if port == "":
         port = ("25")

# specify if its a high priority or not
highpri=yesno_prompt(["1"], "Flag this message/s as high priority? [yes|no]")
if not "YES" in highpri:
        prioflag1 = ""
        prioflag2 = ""
else:
        prioflag1 = ' 1 (Highest)'
        prioflag2 = ' High'

subject=raw_input(setprompt(["1"], "Email subject"))
try:
    html_flag=raw_input(setprompt(["1"], "Send the message as html or plain? 'h' or 'p' [p]"))

    if html_flag == "" or html_flag == "p":
        message_flag="plain"
    if html_flag == "h":
        message_flag="html"
    body = ""
    body=raw_input(setprompt(["1"], "Enter the body of the message, hit return for a new line. Control+c when finished"))
    while body != 'exit':
       try:
          body+=("\n")
          body+=raw_input("Next line of the body: ")
       except KeyboardInterrupt:
               break
except KeyboardInterrupt:
    pass

def mail(to, subject, prioflag1, prioflag2, text):

      msg = MIMEMultipart()
      msg['From'] = user1
      msg['To'] = to
      msg['X-Priority'] = prioflag1
      msg['X-MSMail-Priority'] = prioflag2
      msg['Subject'] = subject

      body_type=MIMEText(text, "%s" % (message_flag))
      msg.attach(body_type)

      mailServer = smtplib.SMTP(smtp, port)
      #mailServer.ehlo()

      if sendmail == 0:
         if email_provider == "gmail":
                 try:
                         mailServer.starttls()
                 except: pass
                 mailServer.ehlo()
         else: mailServer.ehlo()

         if counter == 0:

            try:

               mailServer.login(user, pwd)
               thread.start_new_thread(mailServer.sendmail,(user, to, msg.as_string()))

            except:

               import base64

               try:

                  mailServer.docmd("AUTH LOGIN", base64.b64encode(user))
                  mailServer.docmd(base64.b64encode(pwd), "")

               except Exception, e: 

                   print_warning("It appears your password was incorrect.\nPrinting response: "+(str(e)))
                   return_continue()

      if sendmail == 1: 
                thread.start_new_thread(mailServer.sendmail,(user, to, msg.as_string()))    

if option1 == '1':
   mail("%s" % (to),
   subject,
   prioflag1,
   prioflag2,
   body)

if option1 == '2':
      email_num=0
      fileopen=file(filepath, "r").readlines()
      for line in fileopen:
          to = line.rstrip()
          mail("%s" % (to),
          subject,
          prioflag1,
          prioflag2,
          body)
          email_num=email_num+1
          print "Sent e-mail number: " + (str(email_num))

print_status("SET has finished sending the emails")
return_continue()
