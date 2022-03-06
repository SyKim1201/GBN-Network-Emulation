#!/bin/bash

#Run script for client distributed as part of 
#Assignment 2
#Computer Networks (CS 456)
#Number of parameters: 5
#Parameter:
#    $1: <emulator_address>
#    $2: <emulator_port>
#    $3: <sender_port>
#    $4: <timeout_interval>
#    $5: <input_file>

#Uncomment exactly one of the following commands depending on your implementation

#For Python implementation
python3 sender.py $1 $2 $3 $4 $5

