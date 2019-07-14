'''
some general functions
'''

import datetime


def datumToSeconds(timestr):
    """
    converst a datum string with format %Y-%m-%d
    releative to 1970-01-01 into the corresponding
    second representation.

    Parameters
    ----------
    timestr: str
        date string with format YYYY-MM-DD

    Returns
    -------
    integer
        date in second format
    """
    return (datetime.datetime(int(timestr.split("-")[0]), 
                              int(timestr.split("-")[1]), 
                              int(timestr.split("-")[2])) - datetime.datetime(1970,1,1)).total_seconds()

def secondsToDatum(timeint):
    """
    converst seconds releative to 1970-01-01 into 
    the corresponding Datum string with format
    %Y-%m-%d

    Parameters
    ----------
    timeint: integer
        date in seconds

    Returns
    -------
    string
        date string with format YYYY-MM-DD
    """
    return datetime.datetime.utcfromtimestamp(timeint).strftime('%Y-%m-%d')
