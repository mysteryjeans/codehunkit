"""
Compute ranks base on votes and date or up/down votes
"""

from datetime import datetime
from math import log, sqrt

epoch = datetime(1970, 1, 1)

def epoch_seconds(date):
    """Returns the number of seconds from the epoch to date."""
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


def rank(votes, date):
    """The hot formula. Should match the equivalent function in postgres."""
    s = votes
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(order + sign * seconds / 45000, 7)


def rating(ups, downs):
    """
    Calculate confidence based on votes according to Wilson's score interval 
    """
    n = ups + downs
    if n == 0:
        return 0

    z = 1.96 #1.0 = 85%, 1.96 = 95%
    phat = float(ups) / n
    return (phat + z*z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)
    
    
