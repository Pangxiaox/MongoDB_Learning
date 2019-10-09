from django.shortcuts import render, HttpResponse
from TestingApp.models import Person
# Create your views here.


def createInfo(request):
    Person.objects.create(name="Ann", age=24)
    Person.objects.create(name="Tom", age=26)
    return HttpResponse("create_success")


def findInfo(request):
    res = Person.objects.filter(name="Ann")
    return render(request, "findinfo.html", {"res": res})


def updateInfo(request):
    Person.objects.filter(name="Ann").first().update(name="Bob")
    return HttpResponse('update_success')


def deleteInfo(request):
    Person.objects.filter(name="Bob").first().delete()
    return HttpResponse('delete_success')
