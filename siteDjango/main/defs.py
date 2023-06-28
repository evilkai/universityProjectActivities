import datetime
import calendar
from django.contrib.auth.models import Group, User
from .models import Account




def getDate():
    print((datetime.date(2023, 4, 30)-datetime.date.today()).days)
    return datetime.date.today()

def dateStat(date):
    if date-datetime.date.today()<=0:
        return 0
    else: return 1


def next_month():
    somedate = datetime.date.today()
    months = 1
    month = somedate.month - 1 + months
    year = somedate.year + month // 12
    month = month % 12 + 1
    day = min(somedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

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


def getGroups():
    
    GROUP_CHOICES = []
    GROUP_CHOICES.append(("all","all"))
    for group in Group.objects.all():
        GROUP_CHOICES.append((group.name, group.name))
    return GROUP_CHOICES


groups = []
for group in Group.objects.all():
    groups.append(group.name)

def isAuth(User):
    global groups
    for group in User.groups.all():
        if group.name=="Client":
            return "Client"
        elif group.name in groups:
            return "Staff"

def getCards(User):
    cards=[]
    for card in Account.objects.all():
        if card.cardHolder==User.username:
            cards.append(card)
    return cards

def cardText(num):
    string = str(num)
    res = string[0:4] + " " + string[4:8] + " " + string[8:12] + " " + string[12:16]
    
    print(res)
    return 

def transaction(senderCard,receiverCard,amount):
    if amount>=0:
        sCard=Account.objects.get(cardNumber=senderCard)
        rCard=Account.objects.get(cardNumber=receiverCard)
        # Дать денег
        # sCard.cardBalance+=110000
        if senderCard.cardStatus=="Active" and receiverCard.cardStatus=="Active":
            if sCard.cardBalance>=amount:
                sCard.cardBalance=sCard.cardBalance-amount
                rCard.cardBalance=rCard.cardBalance+amount
                sCard.save()
                rCard.save()

            if sCard.cardBalance<=sCard.minBalance:
                sCard.minBalance=sCard.cardBalance
                sCard.save()


def cardTypeCounter(User):
    counter=[0,0,0,0]
    for card in Account.objects.all():
        if card.cardHolder==User.username:
            if card.cardType=="Debit":
                counter[0]+=1
            elif card.cardType=="Credit":
                counter[1]+=1
            elif card.cardType=="Save":
                counter[2]+=1
            elif card.cardType=="CreditSpecial":
                counter[3]+=1
    
    return counter


def addPercent(card):
    if (getDate()-card.lastDate).days>=30:
        
        if card.cardType=="Credit":
            if card.minBalance<50000:
                card.cardBalance-=(50000-card.minBalance)*card.percent/100
                card.cardBalance=float('{:.2f}'.format(card.cardBalance))
                card.lastDate=getDate()
                card.minBalance=card.cardBalance
                card.save()
        if card.cardType=="Save":
            card.cardBalance+=card.cardBalance*card.percent/100
            card.cardBalance=float('{:.2f}'.format(card.cardBalance))
            card.lastDate=getDate()
            card.save()
        