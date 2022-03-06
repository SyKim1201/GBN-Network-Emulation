from socket import *
from struct import *
import argparse
import sys
import time

#Parse command line arguments
s_parser = argparse.ArgumentParser(description='GBN Sender')

s_parser.add_argument('emu_addr', help='network emulator host address', type=str)
s_parser.add_argument('emu_port', help='emulator port number', type=int)
s_parser.add_argument('s_port', help='sender port number', type=int)
s_parser.add_argument('to', help='timeout interval', type=int)
s_parser.add_argument('fname', help='file name', type=str)

args = s_parser.parse_args()


basenum = 0
seqnum = 0
t = 0
timer = 0
tonum = 0
eot = False
n = 10

#Open input file, process into packets and store into array
packets = []
f = open(args.fname, 'r')

dat = f.read(500)
sn = seqnum
while dat != '':
    pkt = pack('III{0}s'.format(len(dat.encode())),
               1, sn, len(dat.encode()), dat.encode())
    packets.append(pkt)
    sn += 1
    dat = f.read(500)

pkt = pack('III', 2, sn, 0)
packets.append(pkt)

#Open log files to write
s_log = open('seqnum.log', 'w+')
a_log = open('ack.log', 'w+')
n_log = open('N.log', 'w+')

#Create UDP socket and bind to given port number
s_sock = socket(AF_INET, SOCK_DGRAM)
s_sock.bind(('', args.s_port))
s_sock.setblocking(0)

while not eot:

    #Send a packet while window is not full
    if (seqnum < basenum + n) and (seqnum < len(packets)):
        s_sock.sendto(packets[seqnum], (args.emu_addr, args.emu_port))
        s_log.write('t={0} {1}\n'.format(t, seqnum))
        seqnum += 1
        t += 1

        #Start a timer if one has not been started
        if timer == 0:
            timer = time.perf_counter()

    #Receive ACKs
    try:
        rec_ack, emuaddr = s_sock.recvfrom(12)
        rec_dat = unpack('III', rec_ack)
        ack_n = rec_dat[1]
        a_log.write('t={0} {1}\n'.format(t, ack_n))

        #Received EOT
        if rec_dat[0] == 2:
            eot = True

        #Cumulative ACK update if non-duplicate ACK received 
        if ack_n > basenum:
      
            basenum = ack_n + 1

            #Increment window
            if n < 10:
                n += 1
                n_log.write('t={0} {1}\n'.format(t, n))

            #Timer stopped if no outstanding packets, otherwise restart timer
            if basenum == seqnum:
                timer = 0
            else:
                timer = time.perf_counter()

        t += 1
        
    except:
        pass

    #Retransmit timed out packet and set window size to 1
    if timer != 0:
        if (time.perf_counter() - timer) > (0.001 * args.to):
            s_sock.sendto(packets[ack_n + 1], (args.emu_addr, args.emu_port))

            n = 1
            seqnum = basenum
            
            s_log.write('t={0} {1}\n'.format(t, ack_n+1))
            n_log.write('t={0} {1}\n'.format(t, n))
            t += 1
            
            timer = time.perf_counter()
            
            
