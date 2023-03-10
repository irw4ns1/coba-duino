#!/usr/bin/env python

# Minimal version of Duino-Coin PC Miner, useful for developing own apps

# revox 2020-2022

import socket

import hashlib

import urllib.request

import json

import time

from colorama import Fore, Back, Style

username = "Irw4ns12" # Replace this with your username

minerId = "None" # Custom miner identifier

print("\n " + Fore.WHITE + Back.BLUE + " ‖ Minimal DUCO-S1 Python Miner " + Style.RESET_ALL)

print(" " + Fore.YELLOW + Back.BLUE + " ‖ Duino-Coin community 2020-2022 " + Style.RESET_ALL)

print(" " + Fore.YELLOW + Back.BLUE + " ‖ https://github.com/revoxhere/duino-coin " + Style.RESET_ALL + "\n")

# Server IP file url

url = 'https://raw.githubusercontent.com/revoxhere/duino-coin/gh-pages/serverip.txt'

response = urllib.request.urlopen(url)

response = response.read().decode().split('\n')

serverip = response[0]

serverport = response[1]

sharecount = 0

# Connect to the server

s = socket.socket()

s.connect((serverip, int(serverport)))

# Read server version

SERVER_VER = s.recv(3).decode()

print(Fore.WHITE + Back.BLUE + " net " + Style.RESET_ALL + Fore.YELLOW + " Connected " + Style.RESET_ALL + "to the master Duino-Coin server ("+ SERVER_VER+ ")")

# Mining loop

print(Fore.WHITE + Back.YELLOW + " cpu " + Style.RESET_ALL + Fore.YELLOW + " Mining thread is starting " + Style.RESET_ALL + "using DUCO-S1 algorithm")

while True:

    # Send job request

    s.send(bytes("JOB,"+str(username)+",MEDIUM,", encoding='utf-8'))

    # Read job

    job = s.recv(87).decode()

    # Split into previous block hash, result hash and difficulty

    job = job.split(',')

    difficulty = job[2]

    # Measure starting time

    timeStart = time.monotonic()

    for result in range(100 * int(difficulty) + 1):

        # DUCO-S1 loop - find the numeric result

        # By checking if last block hash + n is result hash

        sha1 = hashlib.sha1(str(str(job[0])+str(result)).encode()).hexdigest()

        # If result is found

        if sha1 == str(job[1]):

            # Measure ending time

            timeStop = time.monotonic()

            timeDiff = timeStop - timeStart

            # Calculate hashrate

            hashrate = result / timeDiff

            # Send numeric result to the server

            s.send(bytes(str(result) + "," + str(hashrate) + ",Minimal Python Miner (DUCO-S1)," + str(minerId), encoding='utf-8'))

            # Receive result feedback

            SHAREFEED = s.recv(4).decode()

            sharecount += 1

            # Check whether it was accepted or not

            if SHAREFEED == "GOOD" or SHAREFEED == "BLOCK":

                print(Fore.WHITE + Back.YELLOW + " cpu " + Style.RESET_ALL + Fore.GREEN + " Accepted " + Style.RESET_ALL + "share #" + str(sharecount) + ", speed: " + str(int(hashrate / 1000)) + "kH/s @ diff " + str(difficulty))

                break

            if SHAREFEED == "INVU":

                print("Invalid username") 

