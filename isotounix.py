from dateutil import parser,tz
import sched, time, datetime

def converter(ISO):
    return datetime.datetime.timestamp(parser.isoparse(ISO))
##print(unixdate)
##print(time.time())
scheduler = sched.scheduler(time.time, time.sleep)
time1=1602101920 
def do_thing():
    print("yay")
##scheduler.enterabs(unixdate,1,do_thing)



##def sched_test_01(t1,t2):
##    scheduler.enter(t1,1,do_thing)
##    scheduler.enter(t2,1,do_thing)
##    return scheduler.run()

##print(sched_test_01(2,3))





print("123")
