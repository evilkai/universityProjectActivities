from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib import messages

from .models import Task, Account, CreditRequest
from django.contrib.auth.models import User, Group
from .defs import getDate, setDate, isAuth, getCards, cardText, transaction, cardTypeCounter, addPercent

from django.views.generic import DetailView

# Create your views here.
date = getDate



def profile(request):
    StAuth=isAuth(request.user)
    return render(request, 'main/profile.html', {'StAuth': StAuth})


def logout_view(request):
    logout(request)
    return redirect('home')



def index(request):
    StAuth=isAuth(request.user)
    return render(request, 'main/index.html',{'StAuth': StAuth})


def register(request):
    if not(request.user.is_authenticated):
        if request.method == "POST":
                if request.POST.get('password1')==request.POST.get('password2'):
                    userName=request.POST.get('login')
                    firstName=request.POST.get('firstName')
                    lastName=request.POST.get('lastName')
                    #passWord=request.POST.get('password1')
                    newUser=User.objects.create(username=userName, first_name=firstName, last_name=lastName)

                    newUser.set_password(request.POST.get('password1'))

                    
                    group = Group.objects.get(name='Client') 
                    newUser.groups.add(group)
                    newUser.save()

                    return redirect("home")

    return render(request, "registration/register.html")





##### STAFF #####

def tasks(request):
    if isAuth(request.user) == "Staff":
    
        tasks = Task.objects.all()
        for task in tasks:
            if task.dateBool==True and task.status!=True:
                if task.deadlines!=setDate(task.dateBool):
                    task.deadlines=setDate(task.dateBool)
            task.save()
        return render(request, 'main/staff/tasks.html', {'tasks': tasks, 'date':date})
    

def requests(request):
    if isAuth(request.user) == "Staff":
    
        reqs = CreditRequest.objects.all()
        # for req in reqs:
        #     req.status="На рассмотрении"
        #     req.save()
        print(len(reqs))
        return render(request, 'main/staff/requests.html', {'reqs': reqs, 'date':date})





def archive(request):
    if isAuth(request.user) == "Staff":
        tasks = Task.objects.all()
        return render(request, 'main/staff/archive.html', {'tasks': tasks, 'date':date})


def apanel(request):
    
    if isAuth(request.user) == "Staff":
        return render(request, 'main/apanel.html')


def taskpage(request, pk_page):
    if isAuth(request.user) == "Staff":
        page=Task.objects.get(id=pk_page)
        if request.method=="POST":
            comment2=request.POST['com1']
            page.status=True
            page.userComplited=f"{request.user.username} : {request.user.first_name} {request.user.last_name} "
            page.comments=comment2
            page.save()
            redirect('tasks')
        return render(request, 'main/staff/taskpage.html',  {'page':page, 'date':date  })
    

def requestpage(request, pk_page):
    if isAuth(request.user) == "Staff":
        page=CreditRequest.objects.get(id=pk_page)
        if request.method=="POST":
            for card in Account.objects.all():
                if card.cardNumber==page.cardNumber:
                    card.cardStatus=="Active"
            page.status="complited"
            page.save()
        return render(request, 'main/staff/requestpage.html',  {'page':page, 'date':date  })



def savepage(request):
    redirect('home')










###### CLIENT ######

def cards(request):
    if isAuth(request.user) == "Client":
        Ccards = []
        for card in Account.objects.all():
            if card.cardHolder == request.user.username:
                Ccards.append(card)
            addPercent(card)
            
            
            
            card.cardBalance=float('{:.2f}'.format(card.cardBalance))
        return render(request, 'main/client/cards.html', {'cards': Ccards, 'cardText': cardText})
    
    
def newcard(request):
    if isAuth(request.user) == "Client":
        cardTypes=cardTypeCounter(request.user)
        if request.method=="POST":
            if request.POST.get('Debit'):
                if cardTypes[0]<1:
                    cId = len(Account.objects.all())+1
                    cardN = 1111222233330000 + cId
                    card = Account.objects.create(cardNumber = cardN,cardHolder = request.user.username,cardType = "Debit",cardBalance = 0,cardStatus = "Active")
            elif request.POST.get('Credit'):
                if cardTypes[1]<1:
                    cId = len(Account.objects.all())+1
                    cardN = 1111222233330000 + cId
                    card = Account.objects.create(cardNumber = cardN,cardHolder = request.user.username,cardType = "Credit",cardBalance = 50000,cardStatus = "Active", percent=2.2, minBalance=50000, startBalance=50000)
            elif request.POST.get('Save'):
                if cardTypes[2]<1:
                    cId = len(Account.objects.all())+1
                    cardN = 1111222233330000 + cId
                    card = Account.objects.create(cardNumber = cardN,cardHolder = request.user.username,cardType = "Save",cardBalance = 0,cardStatus = "Active", percent=0.2)
            
            
        redirect('cards')


        # Удалить все карты
        # card = Account.objects.all().delete()
        return render(request, 'main/client/newcard.html', {'cardPerm': len(getCards(request.user)), 'cDebit':cardTypes[0], 'cCredit':cardTypes[1], 'cSave':cardTypes[2]})



def moneytransfer(request):
    if isAuth(request.user) == "Client":
        done=False
        Ccards = []
        for card in Account.objects.all():
            if card.cardHolder == request.user.username:
                Ccards.append(card)

        if request.method=="POST":
            if request.POST.get('senderCard') != "Выберите карту":
                sender=int(request.POST['senderCard'])
                if request.POST.get('receiverCard') != "":
                    recard=int(request.POST['receiverCard'])
                    receiver=int("1111222233330000")+recard
                    if request.POST.get('amount')!="":
                        amount=int(request.POST.get('amount'))

                        transaction(sender,receiver,amount)
                        done=True
        return render(request, 'main/client/moneytransfer.html', {'cards': Ccards,'done':done})


def credit(request):
    payment=0
    percent=6.6
    amount=0
    period=0
    if request.method=="POST":
        if int(request.POST.get('cAmount'))<250000:
            percent=0.55
        else: percent=0.45

        payment=int(request.POST.get('cAmount'))*((percent/100)/(1-(1+percent/100)**(-int(request.POST.get('cPeriod')))))
        payment=float('{:.2f}'.format(payment))
        percent=float('{:.2f}'.format(percent*12))
        amount=int(request.POST.get('cAmount'))
        period=int(request.POST.get('cPeriod'))
    
    return render(request, 'main/client/credit.html', {'payment': payment, 'percent':percent, 'amount': amount, 'period':period})


def offers(request):
    return render(request, 'main/client/offers.html')



def creditrequest(request):
    if isAuth(request.user) == "Client":
        if request.method=="POST":
            
            cardTypes=cardTypeCounter(request.user)
            # cards=Account.objects.all()
            # for card in cards:
            #     if card.cardType=="CreditSpecial":
            #         card.delete()
            if cardTypes[3]==0:
                name=request.POST.get('lastName')+ " " + request.POST.get('firstName') + " " + request.POST.get('patronymic')
                holder=request.user.username
                date=request.POST.get('date')
                tel=request.POST.get('tel')
                pasport=request.POST.get('pasport')
                money=int(request.POST.get('money'))
                goal=request.POST.get('goal')


                cId = len(Account.objects.all())+1
                cardN = 1111222233330000 + cId
                card = Account.objects.create(cardNumber = cardN,cardHolder = request.user.username,cardType = "CreditSpecial",cardBalance = money,cardStatus = "Request", percent=1.8, startBalance=money)

                Crequest = CreditRequest.objects.create(cardNumber=cardN,cardHolder = holder, fullname=name, birthDate=date, tel = tel, pasport = pasport, amount= money, goal = goal)
                print("DONE")
            else: print("NET")
        return render(request, 'main/client/creditrequest.html')