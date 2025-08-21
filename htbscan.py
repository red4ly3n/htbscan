#!/usr/bin/env python3

import argparse
import subprocess
import os
import shutil
import sys
import time
import re
from pathlib import Path

# Colores
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    ENDC = "\033[0m"

def printc(msg, color=Colors.OKGREEN):
    print(f"{color}{msg}{Colors.ENDC}")

def check_dependencies():
    for cmd in ["nmap", "openvpn"]:
        if not shutil.which(cmd):
            printc(f"[-] Error: El comando '{cmd}' no está instalado.", Colors.FAIL)
            sys.exit(1)

def create_machine_folder(name):
    base_folder = Path.cwd() / name
    base_folder.mkdir(exist_ok=True)
    printc(f"[+] Carpeta principal: {base_folder}")

    for sub in ["enum", "ex", "cont"]:
        sub_path = base_folder / sub
        sub_path.mkdir(exist_ok=True)
        printc(f"    - {sub}/", Colors.OKBLUE)

    return base_folder

def connect_vpn_background(ovpn_path):
    printc("[+] Conectando a la VPN (modo silencioso)...", Colors.OKBLUE)
    process = subprocess.Popen(
        ["sudo", "openvpn", "--config", ovpn_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setpgrp
    )
    printc("[*] Esperando 10 segundos para establecer la VPN...", Colors.WARNING)
    time.sleep(10)
    return process

def run_nmap_scan(ip, machine_name, folder_path):
    scan_file = folder_path / "enum" / f"scan_{machine_name.replace(' ', '_')}"
    cmd = f"sudo nmap -sC -sS --min-rate 5000 --open -Pn -oN {scan_file} {ip}"
    printc(f"[+] Ejecutando escaneo Nmap inicial:\n    {cmd}", Colors.OKGREEN)
    os.system(cmd)
    printc(f"[+] Escaneo guardado en: {scan_file}", Colors.OKBLUE)
    return scan_file

def extract_open_ports(scan_file):
    printc("[*] Extrayendo puertos abiertos del escaneo...", Colors.OKBLUE)
    ports = []
    with open(scan_file, "r") as file:
        for line in file:
            match = re.match(r"^(\d+)/tcp\s+open", line)
            if match:
                ports.append(match.group(1))
    port_list = ",".join(ports)
    printc(f"[+] Puertos abiertos detectados: {port_list}", Colors.OKGREEN)
    return port_list

def run_deep_nmap(ip, ports, machine_name, folder_path):
    if not ports:
        printc("[-] No se detectaron puertos abiertos para el escaneo profundo.", Colors.FAIL)
        return
    scan_file = folder_path / "enum" / f"deep_scan_{machine_name.replace(' ', '_')}"
    cmd = f"sudo nmap -sV -p {ports} -Pn -oN {scan_file} {ip}"
    printc(f"[+] Ejecutando escaneo profundo:\n    {cmd}", Colors.OKGREEN)
    os.system(cmd)
    printc(f"[+] Escaneo profundo guardado en: {scan_file}", Colors.OKBLUE)

def main():
    parser = argparse.ArgumentParser(description="HTB VPN + Nmap Automation Script")
    parser.add_argument("-n", "--name", required=True, help="Nombre de la máquina HTB")
    parser.add_argument("-i", "--ip", required=True, help="Dirección IP de la máquina")
    parser.add_argument("-v", "--vpn", required=True, help="Ruta al archivo .ovpn")
    args = parser.parse_args()

    check_dependencies()
    folder = create_machine_folder(args.name)
    connect_vpn_background(args.vpn)
    scan_file = run_nmap_scan(args.ip, args.name, folder)
    ports = extract_open_ports(scan_file)
    run_deep_nmap(args.ip, ports, args.name, folder)

    printc("\n[+] Script finalizado. La VPN sigue activa.", Colors.HEADER)
    printc("    Cuando quieras cerrarla, usá: `sudo pkill openvpn`", Colors.WARNING)

if __name__ == "__main__":
    main()