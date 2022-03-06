#!/bin/bash

#Run script for client distributed as part of 
#Assignment 2
#Computer Networks (CS 456)
#Number of parameters: 5
#Parameter:
#    $1: <emulator_port_forward>
#    $2: <receiver_address>
#    $3: <receiver_port>
#    $4: <emulator_port_backward>
#    $5: <sender_address>
#    $6: <sender_port>
#    $7: <maximum_delay>
#    $8: <discard_probability>
#    $9: <verbose_mode>


#Uncomment exactly one of the following commands depending on your implementation

#For Python implementation
python3 nEmulator.py $1 $2 $3 $4 $5 $6 $7 $8 $9
