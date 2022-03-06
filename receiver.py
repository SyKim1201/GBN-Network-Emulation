from socket import *
from struct import *
import argparse
import sys

#Parse command line arguments
r_parser = argparse.ArgumentParser(description='GBN Receiver')

r_parser.add_argument('emu_addr', help='network emulator host address', type=str)
r_parser.add_argument('emu_port', help='emulator port number', type=int)
r_parser.add_argument('r_port', help='receiver port number', type=int)
r_parser.add_argument('fname', help='file name', type=str)

args = r_parser.parse_args()

seqnum = 0
eot = False

#Open output file to write
f = open(args.fname, 'w+')

#Open log file to write
a_log = open('arrival.log', 'w+')

#Create UDP socket and bind to given port number
r_sock = socket(AF_INET, SOCK_DGRAM)
r_sock.bind(('', args.r_port))

while not eot:

    #Receive and process packet
    pkt, emuaddr = r_sock.recvfrom(512)
    pktheader = unpack('III', pkt[:12])
    pktdat = unpack('{0}s'.format(pktheader[2]), pkt[12:])
    dat = pktdat[0].decode()

    a_log.write('{0}\n'.format(pktheader[1]))

    
    if pktheader[1] == seqnum:
        #Write to file if in order data packet received
        if pktheader[0] == 1:
            f.write(dat)
        #Send EOT back if EOT received
        elif pktheader[0] == 2:
            eot = True

        if eot:
            ack_pkt = pack('III', 2, seqnum, 0)
        else:
            ack_pkt = pack('III', 0, seqnum, 0)

        #Send ACK of in order packet    
        r_sock.sendto(ack_pkt, (args.emu_addr, args.emu_port))

        seqnum += 1

    else:
        if seqnum > 0:
            #Out of order packet, resend ACK of most recent in order packet
            ack_pkt = pack('III', 0, seqnum - 1, 0)
            r_sock.sendto(ack_pkt, (args.emu_addr, args.emu_port))
        
