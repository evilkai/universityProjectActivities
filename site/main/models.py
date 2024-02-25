from django.db import models
from .datedefs import setDate, getDate
from django.contrib.auth.models import Group
# Create your models here.


GROUP_CHOICES = []
GROUP_CHOICES.append(("All","All"))
for group in Group.objects.all():
    if group.name!="Client":
        GROUP_CHOICES.append((group.name, group.name))



class Task(models.Model):
    global GROUP_CHOICES 
    title = models.CharField('Название', max_length=50, default="Задание ")
    task = models.TextField('Описание')
    group = models.CharField('Отдел', max_length=10, choices=GROUP_CHOICES, default="All")
    
    forHeads = models.BooleanField('Задание для нач. отделов', default=False)
    dateBool = models.BooleanField('Задание на квартал', default=False)
    
    id = models.AutoField(primary_key=True)

    status = models.BooleanField('Выполнено', default=False, editable = False)
    userComplited = models.CharField('Кто выполнил', max_length=50,blank=True, editable = False)
    comments = models.TextField('Комментарии', default="", max_length=200,blank=True, editable = False)
    deadlines = models.DateField('Сроки', default=setDate(dateBool),blank=True, editable = False)

    

    def __str__(self):
        return self.title
    





class Account(models.Model):
    
    cardNumber = models.IntegerField('Номер счёта', editable = False)
    cardHolder = models.CharField('Владелец счёта', max_length=40, editable = False)
    cardType = models.CharField('Тип карты', max_length=32, default="Debit", editable = False)
    cardBalance = models.FloatField('Баланс карты', default=0, editable = False)
    cardStatus = models.CharField('Статус активности', max_length=20, default="Active", editable=False)
    lastDate = models.DateField('Ежемесячный процент', default=getDate, editable=False)
    percent = models.FloatField('Ставка', default=0, editable=False)
    minBalance = models.FloatField('Минимальный баланс', default=0, editable=False)
    startBalance = models.IntegerField('Кредитный баланс', default=0, editable=False)

    
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title
    


class CreditRequest(models.Model):
    
    cardNumber = models.IntegerField('Номер счёта', editable = False)
    
    cardHolder = models.CharField('Владелец счёта', max_length=40, editable = False)
    fullname = models.CharField('Полное имя',default="" , max_length=40, editable = False)
    cardType = models.CharField('Тип карты', max_length=32, default="CreditSpecial", editable = False)
    birthDate = models.CharField('Дата рождения', max_length=16, editable=False)
    tel = models.IntegerField('Телефон', editable=False)
    pasport = models.CharField('Паспорт', max_length=16, editable=False)
    amount = models.IntegerField('Сумма', editable=False)
    goal = models.CharField('Цель кредита', max_length=32, editable=False)
    status=models.CharField('Статус заявки', max_length=30, editable=False, default="На рассмотрении")

    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title