import subprocess
import optparse
import re


def args():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="interface to change its Mac address")
    parser.add_option("-m", "--mac", dest="new_mac", help="new Mac address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error(f"[*] please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error(f"[*] please specify an new mac, use --help for more info.")

    return (options.interface, options.new_mac)


def change_mac(interface, mac):
    print(f"[+] Changing MAC address for {interface}")

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])

    if check_output(interface) and (check_output(interface) != interface):
        print(f"[+] MAC address for {interface} changed {mac}")
    else: 
        print(f"[+] MAC address for {interface} didn\'t change")


def check_output(interface):
    output = subprocess.check_output(['ifconfig', interface])
    output = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(output))

    if output:
        return output.group(0)


args = args()

print(f'current MAC {check_output(args[0])}')

change_mac(args[0], args[1])
