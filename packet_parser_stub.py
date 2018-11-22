#!/usr/bin/python
import sys
import argparse
import subprocess

# Variables
clearScreen = subprocess.call('clear',shell=True)

# Lists
allBits = []
packetList = []
decodedPacketList = []
packetListBytes = []
byteList = []

def get_args():
    # get Manchester encoded file from the user
    parser = argparse.ArgumentParser(description="Script to help decode Manchester encoding.")
    parser.add_argument("-f", "--fileName", help="Payload Text File")
    parser.add_argument("-d", "--dataBytes", help="Number of Data byes", type=int)
    args = parser.parse_args()

    if args.fileName is None:
        clearScreen
        print "*************************************************"
        print "*                                               *"
        print "* ERROR: Please supply a binary file to decode. *"
        print "* Ex: -f /path/to/filename                      *"
        print "*                                               *"
        print "*************************************************"
        exit()
    elif args.dataBytes is None:
        clearScreen
        print "****************************************************"
        print "*                                                  *"
        print "* ERROR: Please supply a the number of data bytes. *"
        print "* Ex: -d 14                                        *"
        print "*                                                  *"
        print "****************************************************"
        exit()
    fileName = args.fileName
    numDataBytes = args.dataBytes
    return fileName, numDataBytes

def checkStoreBits(rawList):
    for rawBit in rawList:
        if rawBit == b'\x00':
            allBits.append(0)
        elif rawBit == b'\x01':
            allBits.append(1)
        else:
            print "***************************************"
            print "*                                     *"
            print "* ERROR: non-binary value encountered *"
            print "*                                     *"
            print "***************************************"
            exit(1)

def createPacketList(numDataBytes):
    manchesterDecodeErrors = 0
    packetSize = numDataBytes*2*8
    numPackets = len(allBits)/packetSize
    for i in xrange(numPackets):
        packet = allBits[i*packetSize:(i+1)*packetSize]
        packetList.append(packet)
    for packet in packetList:
        decodedPacket = []
        for i in xrange(0, packetSize, 2):
            if packet[i] == packet[i+1]:
                manchesterDecodeErrors = manchesterDecodeErrors + 1        
            else:
                decodedPacket.append(packet[i+1])
        decodedPacketList.append(decodedPacket)
    return manchesterDecodeErrors

def bitsToDec(bitList, invert = False, reverse = False):
    # invert bits if necessary
    bitList2 = []
    if invert:
        for bit in bitList:
            if bit == 0:
                bitList2.append(1)
            else:
                bitList2.append(0)
    else:
        bitList2 = bitList[:]
    # reverse bits if necessary
    if reverse:
        bitList3 = reversed(bitList2)
    else:
        bitList3 = bitList2[:]    
    value = 0
    for bit in bitList3:
        if isinstance(bit, int):
            value = (value << 1) | bit
        else:
            # if we don't have an integer, then we ended up with a
            # logic error at some point
            value = -1
            break
    return int(value)

def bytesDec():
    incompleteByte = 0
    for packet in decodedPacketList:
        if len(packet) % 8 != 0:
            incompleteByte = incompleteByte + 1
        for i in xrange(0, len(packet), 8):
            bitsInByte = packet[i:i+8]
            byte = bitsToDec(bitsInByte)
            byteList.append(byte)
    return incompleteByte
    
def printDecoded():
    for packetBytes in byteList:
        sys.stdout.write(chr(packetBytes))


if __name__ == "__main__":
    fileName, numDataBytes = get_args()
    # Read file into a list
    with open(fileName, 'rb') as f:
        rawList = list(f.read())
    
    checkStoreBits(rawList)
    manchesterDecodeErrors =createPacketList(numDataBytes)
    incompleteByte = bytesDec()

    clearScreen
    print "---------------------------------"
    print "-                               -"
    print "- Your results are as followed: -"
    print "-                               -"
    print "---------------------------------"
    print " "
    print "Manchester decode errors = %s" %manchesterDecodeErrors 
    print " "
    print "Incomplete bytes captured =  %s" %incompleteByte
    print " "
    print "Decoded Message: "
    print " "
    printDecoded()
    print " "
    print " "