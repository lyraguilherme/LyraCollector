#!/usr/bin/env python3
import getpass
import sys
import csv
from netmiko import ConnectHandler
from argparse import ArgumentParser

def collector(device_ip, device_port, ssh_user, ssh_pass):

    params = { 
        'device_type': 'cisco_ios',
        'ip': device_ip,
        'port': device_port,
        'username': ssh_user,
        'password': ssh_pass
    }

    with ConnectHandler(**params) as ch:

        print(f"\n[!] Conexao estabelecida com {device_ip}")
        # seta terminal length para evitar erros com outputs extensos     
        ch.send_command('terminal length 0')

        # identifica hostname
        hostnameraw = ch.send_command('show running-config | include hostname')
        hostname = hostnameraw.split()
        hostname = hostname[1]

        # define nome do arquivo que sera criado com base no hostname do equipamento
        filename = f"{hostname}.txt"
        print(f"--> Hostname: {hostname}")

        # coleta informacoes   
        print("--> Coletando informacoes...")
        output = "#show version\n" + ch.send_command('show version') + "\n\n\n"
        output += "#show inventory\n" + ch.send_command('show inventory') + "\n\n\n"
        output += "#show modules\n" + ch.send_command('show modules') + "\n\n\n"
        output += "#show ip protocols\n" + ch.send_command('show ip protocols') + "\n\n\n"
        output += "#show cdp neighbors\n" + ch.send_command('show cdp neighbors') + "\n\n\n"        
        output += "#show interfaces status\n" + ch.send_command('show interfaces status') + "\n\n\n"        
        output += "#show interfaces description\n" + ch.send_command('show interfaces description') + "\n\n\n"
        output += "#show spanning-tree\n" + ch.send_command('show spanning-tree') + "\n\n\n"
        output += "#show ip route\n" + ch.send_command('show ip route') + "\n\n\n"
        output += "#show vrf\n" + ch.send_command('show vrf') + "\n\n\n"        

        # grava outputs em arquivo
        print("--> Gravando informacoes...")
        f = open(filename, "w")
        f.write("-" * 30 + "\n" + hostname + "\n" + "-" * 30 + "\n\n")
        f.write(output)
        print("--> Criado arquivo " + filename)

        # encerra conexao
        ch.disconnect()
        print("[!] Conexao encerrada.\n")

def main():
    parser = ArgumentParser(description='')
    parser.add_argument('-c', '--csv', required=True, help='arquivo CSV')    

    # credenciais
    #ssh_user = input('\nSSH Username: ')
    #ssh_pass = getpass.getpass('SSH Password: ')
    #device_port = "22"

    # csv
    csv_file = parser.parse_args().csv
    with open(csv_file, mode='r') as devices_list:
        csv_reader = csv.DictReader(devices_list, delimiter=',')
        for device in csv_reader:
            collector(device['device_ip'], device['device_port'], device['ssh_user'], device['ssh_pass'])

if __name__ == "__main__":
    main()
