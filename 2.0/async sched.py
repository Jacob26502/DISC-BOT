import sched, time, datetime, asyncio
print(time.time())
scheduler = sched.scheduler(time.time, time.sleep)
count = 0

def ticker():
    print("code")

def sched_test():
     scheduler.enter(1,1,ticker)
     scheduler.enter(3,1,ticker)
     count = 0
     return scheduler.run()
print(sched_test())
