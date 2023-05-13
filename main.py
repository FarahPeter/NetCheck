from pythonping import ping
import datetime
import time
from statistics import mean
import tkinter as tk
from tkinter import *


def find_between( s, first, last=None):
    try:
        if (last!=None):
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        else:
            start = s.index(first) + len(first)
            return s[start:]
    except ValueError:
        return ""

def TimeNow():
    now = datetime.datetime.now()
    formatted_date = now.strftime("%d/%m/%Y_%H-%M-%S")
    return (formatted_date)

def Ping(Loop=False):
    SessionNumberOfpacketsSentSuccesfully=0
    SessionNumberOfpacketsLost=0
    f = open("ping_results.log", "a")
    counter=600
    while Loop:
        try:
            reply=ping('google.com',count=1,timeout=1)#reply=ping('google.com', verbose=True, out=f,count=1)
        except:
            reply=""
            time.sleep(1)

        replyFormated=find_between(str(reply),"Reply","ms")

        if (len(replyFormated)==0):
            replyFormated="Request timed out 1000ms"
            SessionNumberOfpacketsLost = SessionNumberOfpacketsLost + 1
        else:
            replyFormated="Reply "+replyFormated+"ms"
            SessionNumberOfpacketsSentSuccesfully = SessionNumberOfpacketsSentSuccesfully+1
            time.sleep(1)


        print(str(TimeNow()) +" || "+str(replyFormated)+ " || "+ "Packet Loss this session= "+ str(round(SessionNumberOfpacketsLost/(SessionNumberOfpacketsLost+SessionNumberOfpacketsSentSuccesfully) *100,1))+"%")


        #every 60*10=600s so 10 min print
        '''counter = counter+1
        if (counter>=600):
            counter=1
            print(str(TimeNow()) +" || "+ "Packet Loss this session= "+ str(round(SessionNumberOfpacketsLost/(SessionNumberOfpacketsLost+SessionNumberOfpacketsSentSuccesfully) *100,1))+"%")
        '''
        f.write(str(TimeNow()) +" || "+str(replyFormated)+"\n")
    f.close()



def GenerateStats():
    filepath = "ping_results.log"
    numPacketLoss=0
    numPacketsSuccess=0
    delayArray=[]
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        maxDelay=-1
        minDelay=1001
        while line:
            #print("Line {}: {}".format(cnt, line.strip()))
            curLine=line.strip()
            curLineLength=len(curLine)

            #for packet loss calculations
            if ((curLine[curLineLength-6:])=="1000ms"):
                numPacketLoss=numPacketLoss+1
            else:
                numPacketsSuccess=numPacketsSuccess+1

            #for average max and min delay calculation
            findDelay=find_between(curLine,"in ","ms")
            if (len(findDelay)!=0):
                delay=float(findDelay)
                delayArray.append(delay)
                if (delay>maxDelay):
                    maxDelay=delay
                if(delay<minDelay):
                    minDelay=delay


            line = fp.readline()
            cnt += 1

    #processing stuff
    PacketLossPercentage=numPacketLoss/(numPacketLoss+numPacketsSuccess) *100
    averageDelayWithoutPacketLoss=mean(delayArray)

    print("Packet loss= "+str(round(PacketLossPercentage,4))+"%")
    print("Average delay excluding packet loss= "+str(round(averageDelayWithoutPacketLoss,4))+"ms")
    print("Maximum delay excluding packet loss= "+str(round(maxDelay,4))+"ms")
    print("Minimum delay excluding packet loss= " +str(round(minDelay, 4)) + "ms")

