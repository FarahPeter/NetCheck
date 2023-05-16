import threading
import webbrowser
from pythonping import ping
import datetime
import time
from statistics import mean
import tkinter as tk


#TODO Look into delaArray memory taking


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
    CurrentInternetState=[False,False,False]
    f = open("Ping_results_V2.log", "a")
    f.write("================================================================\n")
    f.write("                       New Process Started\n")
    f.write("================================================================\n")
    counter=600
    writeEvery5s=0
    arrayOfOutput=[""]*10
    InternetDownFor3s = 0
    InternetDownFor2s = 0
    InternetDownFor1s = 0
    while Loop:
        CurrentInternetState[2]=CurrentInternetState[1]
        CurrentInternetState[1]=CurrentInternetState[0]
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
            CurrentInternetState[0]=True
        else:
            CurrentInternetState[0]=False
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
        PacketLossPercentage = SessionNumberOfpacketsLost / (SessionNumberOfpacketsLost + SessionNumberOfpacketsSentSuccesfully) * 100
        packetLoss["text"] = str(round(PacketLossPercentage, 2)) + "%"
        try:
            averageDelayWithoutPacketLoss = mean(delayArray)

            averageDelay["text"] = str(round(averageDelayWithoutPacketLoss, 2)) + "ms"
            maxDelayglob["text"] = str(round(maxDelay, 2)) + "ms"
            minDelayglob["text"] = str(round(minDelay, 2)) + "ms"
        except Exception as e:
            averageDelay["text"] = "Wait!"
            maxDelayglob["text"] = "Wait!"
            minDelayglob["text"] = "Wait!"



        if (CurrentInternetState[0]==True and CurrentInternetState[1]==True and CurrentInternetState[2]==True):
            internetSate["text"]="Down"
            InternetDownFor3s=InternetDownFor3s+1
        elif(CurrentInternetState[0]==True and CurrentInternetState[1]==True):
            internetSate["text"] = "Down 2s"
            InternetDownFor2s=InternetDownFor2s+1
        elif(CurrentInternetState[0]==True ):
            internetSate["text"] = "Inconsistent"
            InternetDownFor1s=InternetDownFor1s+1
        else:
            internetSate["text"]="UP"



        cut1s["text"] = str(InternetDownFor1s)
        cut2s["text"] = str(InternetDownFor2s)
        cut3s["text"] = str(InternetDownFor3s)

        f.write(str(TimeNow()) + " || " + str(replyFormated)+ " || Packet Loss: "+ str(round(PacketLossPercentage,2))+"%" +"\n")

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
    global internetSate
    global cut1s
    global cut2s
    global cut3s
    #UI
    master = tk.Tk()
    master.wm_title("NetCheck")
    master.geometry("580x220")
    #master.resizable(width=0, height=0)


    ping0 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=500)
    ping0.grid(row=0,column=0,columnspan = 2)
    ping1 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=500)
    ping1.grid(row=1,column=0,columnspan = 2)
    ping2 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=500)
    ping2.grid(row=2,column=0,columnspan = 2)
    ping3 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=500)
    ping3.grid(row=3,column=0,columnspan = 2)
    ping4 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=500)
    ping4.grid(row=4,column=0,columnspan = 2)
    ping5 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=500)
    ping5.grid(row=5,column=0,columnspan = 2)
    ping6 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=500)
    ping6.grid(row=6,column=0,columnspan = 2)
    ping7 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=500)
    ping7.grid(row=7,column=0,columnspan = 2)
    ping8 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=500)
    ping8.grid(row=8,column=0,columnspan = 2)
    ping9 =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,wraplength=500)
    ping9.grid(row=9,column=0,columnspan = 2)


    pingProcess=threading.Thread(target=Ping)
    pingProcess.start()


    internetSateLabel = tk.Label(master, text="Status:", fg="black", pady=0, padx=10, font=10)
    internetSateLabel.grid(row=0, column=2, columnspan=1)
    packetLossLabel =tk.Label(master,text="Pcts loss:",fg="black",pady=0, padx=10, font=10)
    packetLossLabel.grid(row=1,column=2,columnspan = 1)
    averageDelayLabel =tk.Label(master,text="Avg delay:",fg="black",pady=0, padx=10, font=10)
    averageDelayLabel.grid(row=2,column=2,columnspan = 1)
    maxDelayLabel =tk.Label(master,text="Max delay:",fg="black",pady=0, padx=10, font=10)
    maxDelayLabel.grid(row=3,column=2,columnspan = 1)
    minDelayLabel =tk.Label(master,text="Min delay:",fg="black",pady=0, padx=10, font=10)
    minDelayLabel.grid(row=4,column=2,columnspan = 1)
    cut1sLabel = tk.Label(master, text="1s cuts:", fg="black", pady=0, padx=10, font=10)
    cut1sLabel.grid(row=5, column=2, columnspan=1)
    cut2sLabel = tk.Label(master, text="2s cuts:", fg="black", pady=0, padx=10, font=10)
    cut2sLabel.grid(row=6, column=2, columnspan=1)
    cut3sLabel = tk.Label(master, text="3s cuts:", fg="black", pady=0, padx=10, font=10)
    cut3sLabel.grid(row=7, column=2, columnspan=1)


    internetSate = tk.Label(master, text="", fg="black", pady=0, padx=10, font=10)
    internetSate.grid(row=0, column=3, columnspan=1)
    packetLoss =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10)
    packetLoss.grid(row=1,column=3,columnspan = 1)
    averageDelay =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10)
    averageDelay.grid(row=2,column=3,columnspan = 1)
    maxDelayglob =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10)
    maxDelayglob.grid(row=3,column=3,columnspan = 1)
    minDelayglob =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10)
    minDelayglob.grid(row=4,column=3,columnspan = 1)
    cut1s =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,width=6)
    cut1s.grid(row=5,column=3,columnspan = 1)
    cut2s =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,width=6)
    cut2s.grid(row=6,column=3,columnspan = 1)
    cut3s =tk.Label(master,text="",fg="black",pady=0, padx=10, font=10,width=6)
    cut3s.grid(row=7,column=3,columnspan = 1)

    menubar = tk.Menu(master)


    contact = tk.Menu(menubar, tearoff=0)
    contact.add_command(label="GitHub",command=lambda: webbrowser.open('https://github.com/FarahPeter?tab=repositories'))
    menubar.add_cascade(label="Contact", menu=contact)

    master.config(menu=menubar)



    master.mainloop()