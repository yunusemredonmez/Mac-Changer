#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[+] PLease specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[+] PLease specify a MAC, use --help for more info")
    return options

def change_mac(interface,new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Couldn't read MAC address")

options = get_arguments()
first_mac = get_current_mac(options.interface)
print("Current MAC = " + str(first_mac))
change_mac(options.interface, options.new_mac)
new_mac = get_current_mac(options.interface)
print(new_mac)
if new_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + new_mac)
else:
    print("[-] MAC address didn't change")
