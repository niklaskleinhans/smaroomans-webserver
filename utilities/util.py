import datetime

def datumToSeconds(timestr):
    return (datetime.datetime(int(timestr.split("-")[0]), 
                              int(timestr.split("-")[1]), 
                              int(timestr.split("-")[2])) - datetime.datetime(1970,1,1)).total_seconds()

def secondsToDatum(timeint):
    return datetime.datetime.utcfromtimestamp(timeint).strftime('%Y-%m-%d')
