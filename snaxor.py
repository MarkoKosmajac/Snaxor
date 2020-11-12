#!/usr/bin/env python

import socket
import threading
import concurrent.futures
import colorama
import sys
from colorama import Fore, Back, Style
from colorama import init
init(strip=not sys.stdout.isatty())
import argparse
from termcolor import cprint 
from pyfiglet import figlet_format
colorama.init()

portparser = argparse.ArgumentParser(prog='Snaxor',
                                    usage='%(prog)s [-h] [--ip] [--startport] [--endport]',
                                    description= Style.BRIGHT + Fore.MAGENTA + '%(prog)s scans a target IP for open ports.' + Fore.RESET,
                                    epilog= Style.BRIGHT + Fore.YELLOW + "Made by https://github.com/MarkoKosmajac/" + Fore.RESET + " with" + Fore.RED + Style.BRIGHT +  " <3")

portparser.add_argument('--ip',
                       metavar='ip',
                       action="store",
                       dest="ip",
                       type=str,
                       help='The target IP to be scanned, can also be an ip.')

portparser.add_argument('--startport',
                       metavar='startport',
                       action="store",
                       dest="startport",
                       type=int,
                       default=1,
                       help='The startport of the target to be scanned.')

portparser.add_argument('--endport',
                       metavar='endport',
                       action="store",
                       dest="endport",
                       type=int,
                       default=1000,
                       help='The endport of the target to be scanned.')

portparser.add_argument('--threads',
                       metavar='threads',
                       action="store",
                       dest="threads",
                       type=int,
                       default=100,
                       help='The amount of spawned threads.')

args = portparser.parse_args()

ip = args.ip
startport = args.startport
endport = args.endport
nrThreads = args.threads

if ip is None:
    portparser.error("Please specify a target ip with '--ip [TARGET]'")

if startport == 0 or startport < 0:
    portparser.error("Ports cannot be 0 or negative...")

if endport > 65535:
    portparser.error("Ports cannot be higher than 65535...")

if nrThreads == 0 or nrThreads < 0:
    portparser.error("Threads cannot be 0 or negative...")

print_lock = threading.Lock()

def scan(ip, port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)
    try:
        scanner.connect((ip, port))
        scanner.close()
        with print_lock:
            print("Port" + Fore.WHITE + f"[{port}]: " + Fore.GREEN + " Opened" + Fore.RESET)
    except:
        pass

with concurrent.futures.ThreadPoolExecutor(max_workers=nrThreads) as executor:
    cprint(figlet_format('Snaxor', font='starwars'),
       'magenta', attrs=['bold'])
    print("Scanning " + Fore.YELLOW + Style.BRIGHT + ip + Fore.RESET + Style.NORMAL + " | Ports: " + Fore.CYAN +Style.BRIGHT + str(startport) + Fore.RESET + "-" + Fore.CYAN + str(endport) + Fore.RESET + Style.NORMAL + " | Threads: " + Fore.RED + Style.BRIGHT + str(nrThreads) + Fore.RESET + Style.NORMAL)
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = =\n")
    print(Fore.LIGHTGREEN_EX + "Results:" + Fore.RESET)
    for port in range(startport, endport+1):
        executor.submit(scan, ip, port)
