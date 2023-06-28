import datetime
import calendar




def getDate():
    print((datetime.date(2023, 4, 30)-datetime.date.today()).days)
    return datetime.date.today()


def setDate(k):
    somedate=getDate()
    q1=datetime.date(somedate.year, 3, 31)
    q2=datetime.date(somedate.year, 6, 30)
    q3=datetime.date(somedate.year, 9, 30)
    q4=datetime.date(somedate.year, 12, 31)
    quarter=(q1,q2,q3,q4)
    if k==True:
        for el in quarter:
            if el > q1:
                return el
    else:
        return datetime.date(somedate.year, somedate.month, calendar.monthrange(somedate.year,somedate.month)[1])
