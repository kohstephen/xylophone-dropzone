#Use python2

from time import sleep
import serial
import struct
import numpy

def main():

	#Text file into
	fileDir = "C:\Users\Sophia\Desktop\School Work\Senior Design\Code\Arduino"
	fileName = "\MHALL.txt"

	numLSA = 3 #Number of LSAs
	dropSteps = 88*2 #44 steps/drop
	delayTime = 5 #2ms between steps

	prevState = [0]


	#GETTING DATA FROM FILE

	noteTimes = [] #The step that notes are played in ms
	LSAcombos = [] #LSA combo codes, corresponds to noteTimes

	#Converting file into two vectors
	f = open(fileDir+fileName, "rb")
	for line in f:
		out = line.split("	");
		noteTimes += [int(round(float(out[0])/delayTime)) + dropSteps] #Round to nearest delayTime interval
		LSAcombos += [int(out[1])]
	f.close()

	lastTime = noteTimes[-1]

	print "noteTimes: " + repr(noteTimes)
	print "LSAcombos: " + repr(LSAcombos)
	print "Last time: " + repr(lastTime)

	#CREATING STEPARR

	#stepArr[time_step]	
	totalSteps = lastTime + dropSteps * 3
	stepArr = prevState * totalSteps
	print "total steps: " + repr(totalSteps)
	print "drop steps: " + repr(dropSteps)
	print "stepArr: " + repr(stepArr)
	for LSA in range(0, numLSA):
		print "Checking LSA " + repr(LSA)
		t = 1
		while t < len(stepArr):
			if ((t in noteTimes) and checkLSA(LSA, LSAcombos[noteTimes.index(t)])):
				print repr(t) + " is in noteTimes"
				for n in range(0, dropSteps):
					stepArr[t] = nextStepCode(stepArr[t], stepArr[t-1], LSA)
					t = t + 1
			else:
				stepArr[t] = sameStepCode(stepArr[t], stepArr[t-1], LSA)
				t = t + 1
		printBinary(stepArr)


	print repr(stepArr)

	ser = serial.Serial('COM3', 9600, timeout = 5) # Establish the connection on a specific port
	sleep(2)

	print "Connection made!"


	###SENDING DATA TO ARDUINO
	counter = 0
	while counter < len(stepArr):
		print "Sending " + repr(stepArr[counter])
		b = ser.write(str(bytearray([stepArr[counter]]))) # Convert the decimal number to ASCII then send it to the Arduino
		print repr(b) + " bytes sent"
		line = ser.readline()
		print "Recieved " + repr(line)
		counter = counter + 1

	ser.close()

def nextStep(step):
	if(step == 0):
		return 1
	if(step == 1):
		return 3
	if(step == 2):
		return 0
	if(step == 3):
		return 2

def nextStepCode(curCode, prevCode, LSA):
	LSAprevState = (prevCode >> LSA * 2) % 4
	LSAcurrState = (curCode >> LSA * 2) % 4
	LSAnextState = nextStep(LSAprevState)
	return curCode + (LSAnextState - LSAcurrState) * (4**LSA)

def sameStepCode(curCode, prevCode, LSA):
	LSAprevState = (prevCode >> LSA * 2) % 4
	LSAcurrState = (curCode >> LSA * 2) % 4
	return curCode + (LSAprevState - LSAcurrState) * (4**LSA)


def printBinary(arr):
	for elem in arr:
		print bin(elem)

def checkLSA(LSA, combo):
	return (combo >> LSA) % 2

if __name__ == '__main__':
	main()