import threading
import webbrowser
from pythonping import ping
import datetime
import time
from statistics import mean
import tkinter as tk



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


def Ping(Loop=True):
    maxDelay = -1
    minDelay = 1001
    SessionNumberOfpacketsSentSuccesfully=0
    SessionNumberOfpacketsLost=0
    delayArray = []
    f = open("ping_results_perSession.log", "w")
    counter=600
    writeEvery5s=0
    arrayOfOutput=[""]*10
    while Loop:
        writeEvery5s=writeEvery5s+1
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

            findDelay = find_between(replyFormated, "in ", "ms")
            if (len(findDelay) != 0):
                delay = float(findDelay)
                delayArray.append(delay)
                if (delay > maxDelay):
                    maxDelay = delay
                if (delay < minDelay):
                    minDelay = delay
            time.sleep(1)


        arrayOfOutput[9] = arrayOfOutput[8]
        arrayOfOutput[8] = arrayOfOutput[7]
        arrayOfOutput[7] = arrayOfOutput[6]
        arrayOfOutput[6] = arrayOfOutput[5]
        arrayOfOutput[5] = arrayOfOutput[4]
        arrayOfOutput[4]=arrayOfOutput[3]
        arrayOfOutput[3]=arrayOfOutput[2]
        arrayOfOutput[2]=arrayOfOutput[1]
        arrayOfOutput[1]=arrayOfOutput[0]
        arrayOfOutput[0]=replyFormated


        ping9["text"] = arrayOfOutput[0]
        ping8["text"] = arrayOfOutput[1]
        ping7["text"] = arrayOfOutput[2]
        ping6["text"] = arrayOfOutput[3]
        ping5["text"] = arrayOfOutput[4]
        ping4["text"]=arrayOfOutput[5]
        ping3["text"]=arrayOfOutput[6]
        ping2["text"] = arrayOfOutput[7]
        ping1["text"] = arrayOfOutput[8]
        ping0["text"] = arrayOfOutput[9]
        #print(str(TimeNow()) +" || "+str(replyFormated)+ " || "+ "Packet Loss this session= "+ str(round(SessionNumberOfpacketsLost/(SessionNumberOfpacketsLost+SessionNumberOfpacketsSentSuccesfully) *100,1))+"%")

        # processing stuff
        try:
            PacketLossPercentage = SessionNumberOfpacketsLost / (SessionNumberOfpacketsLost + SessionNumberOfpacketsSentSuccesfully) * 100
            averageDelayWithoutPacketLoss = mean(delayArray)

            packetLoss["text"] = str(round(PacketLossPercentage, 4)) + "%"
            averageDelay["text"] = str(round(averageDelayWithoutPacketLoss, 4)) + "ms"
            maxDelayglob["text"] = str(round(maxDelay, 4)) + "ms"
            minDelayglob["text"] = str(round(minDelay, 4)) + "ms"
        except:
            packetLoss["text"] = "Wait!"
            averageDelay["text"] = "Wait!"
            maxDelayglob["text"] = "Wait!"
            minDelayglob["text"] = "Wait!"

    f.close()


if __name__ == '__main__':
    global ping0
    global ping1
    global ping2
    global ping3
    global ping4
    global ping5
    global ping6
    global ping7
    global ping8
    global ping9
    global packetLoss
    global averageDelay
    global maxDelayglob
    global minDelayglob
    #UI
    master = tk.Tk()
    master.wm_title("NetCheck")
    master.geometry("580x220")
    master.resizable(width=0, height=0)


    ping0 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=400)
    ping0.grid(row=0,column=0,columnspan = 2)
    ping1 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=400)
    ping1.grid(row=1,column=0,columnspan = 2)
    ping2 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=400)
    ping2.grid(row=2,column=0,columnspan = 2)
    ping3 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=400)
    ping3.grid(row=3,column=0,columnspan = 2)
    ping4 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=400)
    ping4.grid(row=4,column=0,columnspan = 2)
    ping5 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=400)
    ping5.grid(row=5,column=0,columnspan = 2)
    ping6 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=400)
    ping6.grid(row=6,column=0,columnspan = 2)
    ping7 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=400)
    ping7.grid(row=7,column=0,columnspan = 2)
    ping8 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=400)
    ping8.grid(row=8,column=0,columnspan = 2)
    ping9 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=400)
    ping9.grid(row=9,column=0,columnspan = 2)


    pingProcess=threading.Thread(target=Ping)
    pingProcess.start()


    packetLossLabel =tk.Label(master,text="Pcts loss:",fg="black",pady=0, padx=10, font=10)
    packetLossLabel.grid(row=0,column=2,columnspan = 1)
    averageDelayLabel =tk.Label(master,text="Avg delay:",fg="black",pady=0, padx=10, font=10)
    averageDelayLabel.grid(row=1,column=2,columnspan = 1)
    maxDelayLabel =tk.Label(master,text="Max delay:",fg="black",pady=0, padx=10, font=10)
    maxDelayLabel.grid(row=2,column=2,columnspan = 1)
    minDelayLabel =tk.Label(master,text="Min delay:",fg="black",pady=0, padx=10, font=10)
    minDelayLabel.grid(row=3,column=2,columnspan = 1)



    packetLoss =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10)
    packetLoss.grid(row=0,column=3,columnspan = 1)
    averageDelay =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10)
    averageDelay.grid(row=1,column=3,columnspan = 1)
    maxDelayglob =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10)
    maxDelayglob.grid(row=2,column=3,columnspan = 1)
    minDelayglob =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10)
    minDelayglob.grid(row=3,column=3,columnspan = 1)

    menubar = tk.Menu(master)


    contact = tk.Menu(menubar, tearoff=0)
    contact.add_command(label="GitHub",command=lambda: webbrowser.open('https://github.com/FarahPeter?tab=repositories'))
    menubar.add_cascade(label="Contact", menu=contact)

    master.config(menu=menubar)



    master.mainloop()