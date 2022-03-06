#!/bin/bash

#Run script for client distributed as part of 
#Assignment 2
#Computer Networks (CS 456)
#Number of parameters: 5
#Parameter:
#    $1: <emulator_address>
#    $2: <emulator_port>
#    $3: <receiver_port>
#    $4: <output_file>

#Uncomment exactly one of the following commands depending on your implementation

#For Python implementation
python3 receiver.py $1 $2 $3 $4 
