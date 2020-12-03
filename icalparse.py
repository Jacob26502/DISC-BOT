from re import search
from dateutil import parser as parser
import datetime
import time
global time001
global ical03
time001=int(time.time())
global future
future=[]




def sortbystring(ls):
    return int(ls[0])


def parse_ical():
    global time001
    global ical03
    time001=int(time.time())
    ical00 = open("ical01.ics").read().split("\n")
    del ical00[0:6]
    ical01=[]
    ical02=[]
    ical03=[]
    for x0 in ical00:
        if search(("DTEND|DTSTAMP|SEQUENCE|END:VCALENDAR|UID|END:VEVENT|BEGIN:VEVENT"),x0):
            continue
        else:
            ical01.append(x0)

    for v0,y in enumerate(ical01):

        if search("DTSTART",y):
            ical02.append("|".join(ical01[v0:v0+3]))
            ical02[-1]=ical02[-1].split("|")
        else:
            continue

    for z in ical02:    #TODO NEED TO CHANGE NEXT TERM
        if ((z[1] != "LOCATION:Online Delivery") or (search("Weekly Tutorial",z[2])!=None) or (search("ELEC",z[2])!=None)):
            continue
        else:
            ical03.append(z)

    for v2,x1 in enumerate(ical03):
        for v3,y in enumerate(x1):
            ical03[v2][v3]=y[y.find(":")+1:]
        if search("COMP",x1[2]):
            ical03[v2].append(x1[2][0:8])
        elif search("Foundations",x1[2]):
            ical03[v2].append("COMP1215")
        elif search("Programming",x1[2]):
            ical03[v2].append("COMP1202")
        elif search("Professional",x1[2]):
            ical03[v2].append("COMP1205")
        else:
            ical03[v2].append("")
    ##time zone convert
##add a custom event
    ical03.append(open("TESTLECTURE.csv",mode="r").read().split("\n")[1].split(","))
    global future
    future=[]
    ##return all events in the future
    for v4,a in enumerate(ical03):
        a[0]=int(datetime.datetime.timestamp(parser.isoparse(a[0])))
        if int(a[0])-int(time001) > 0:     ##if the time of the meeting - now is > 0 meaning it's in the future and it's the latest event
            next_event=ical03[v4]
            future.append(a)

    future=sorted(future,key = sortbystring)
    future=future[0:5]

    return future    ##returns as [unix,online delivery,course desc, course code] including text or custom lecture
