from socket import *
from struct import *
import argparse
import sys
import os
import random
import time

#Parse command line arguments
e_parser = argparse.ArgumentParser(description='GBN Network Emulator')

e_parser.add_argument('es_port', help='emulator port number in sender direction', type=int)
e_parser.add_argument('r_addr', help='receiver address', type=str)
e_parser.add_argument('r_port', help='receiver port number', type=int)
e_parser.add_argument('er_port', help='emulator port number in receiver direction', type=int)
e_parser.add_argument('s_addr', help='sender address', type=str)
e_parser.add_argument('s_port', help='sender port number', type=int)
e_parser.add_argument('md', help='max delay', type=int)
e_parser.add_argument('dp', help='discard probability', type=float)
e_parser.add_argument('verb', help='verbose mode', type=bool)

args = e_parser.parse_args()

#Create UDP sockets and bind to given port numbers
es_sock = socket(AF_INET, SOCK_DGRAM)
es_sock.bind(('', args.es_port))

er_sock = socket(AF_INET, SOCK_DGRAM)
er_sock.bind(('', args.er_port))


pid = os.fork()

#Receive and forward packets
if pid > 0:
    
    while True:
        s_drop = False

        #Receive and process packet
        s_pkt, saddr = es_sock.recvfrom(512)


        spkttype = unpack('I', s_pkt[:4])
        spktnum = unpack('I', s_pkt[4:8])

        if args.verb == 1:
            print('receiving Packet {0}\n'.format(spktnum[0]))

        #Don't drop EOT
        if spkttype[0] != 2:
            #Randomly drop packet based on given probability
            s_dropn = random.random()
            if s_dropn < args.dp:
                s_drop = True
        
        if not s_drop:
            #If packet is not dropped, send after random delay 
            
            s_delay_t = random.randint(0, args.md)
            time.sleep(0.001 * s_delay_t)
            
            if args.verb == 1:
                print('forwarding Packet {0}\n'.format(spktnum[0]))
                
            es_sock.sendto(s_pkt, (args.r_addr, args.r_port))
        else:
            if args.verb == 1:
                print('discarding Packet {0}\n'.format(spktnum[0]))
            

#Receive and forward ACKs
else:
    
    while True:
        r_drop = False

        #Receive and process ACK
        r_pkt, raddr = er_sock.recvfrom(12)

        rpkttype = unpack('I', r_pkt[:4])
        rpktnum = unpack('I', r_pkt[4:8])

        if args.verb == 1:
            print('receiving ACK {0}\n'.format(rpktnum[0]))

        #Don't drop EOT
        if rpkttype[0] != 2:
            #Randomly drop ACK based on given probability
            r_dropn = random.random()
            if r_dropn < args.dp:
                r_drop = True        

        if not r_drop:
            #If ACK is not dropped, send after random delay 
            
            r_delay_t = random.randint(0, args.md)
            time.sleep(0.001 * r_delay_t)

            if args.verb == 1:
                print('forwarding ACK {0}\n'.format(rpktnum[0]))
            
            er_sock.sendto(r_pkt, (args.s_addr, args.s_port))
        else:
            if args.verb == 1:
                print('discarding ACK {0}\n'.format(rpktnum[0]))

        
