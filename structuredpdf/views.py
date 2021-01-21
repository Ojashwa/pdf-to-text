from typing import KeysView
from django.contrib.messages import api
from django.contrib.messages.api import error
from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from invoice2data.input import pdftotext
from .models import Userregistration,Userpdfdata
from .serializer import UserpdfdataSeralizer
from rest_framework import serializers, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
from django.conf import settings
import os
import json
# Create your views here.

def home(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        query = Userregistration(name=request.POST['name'],email=request.POST['email'],password=request.POST['password'])
        query.save(force_insert=True)
        messages.success(request,"Registered sccuessfully!!\n Kindly login..")
    return redirect(home)

def login(request):
    if request.method=='post':
        Userregistration.objects.filter(email=request.POST['email'],password=request.POST['password']).exists()
        messages.success(request,"welcome "+request.POST['email'])
        request.session['email']=request.POST['email']
    return render(request,'user.html')

@api_view(['GET'])
def apiOverview(request):
    '''overview of urls'''
    api_urls={
        'List':'/digi-list/',
    }
    return Response(api_urls)

@api_view(['GET'])
def digitizedList(request):
    d_list = Userpdfdata.objects.all()
    serializer = UserpdfdataSeralizer(d_list,many=True)
    return Response(serializer.data)

def fileUpload(request):
    '''get pdf file form the user-end'''
    if request.is_ajax:
        files = request.FILES.get('myfile')
        print(request.session.get('_auth_user_id',None))
        if files is not None:
            if os.path.exists(str(settings.MEDIA_ROOT+files.name)):
                return JsonResponse({'message': 'File exists'})
            else:
                fs = FileSystemStorage(location=str(settings.MEDIA_ROOT))
                fs.save(files.name,files)
                if "Amazon" in files.name:
                    digital_data = amazonInvoice(files.name,request)
                    # if(digital_data):
                    return JsonResponse({'message':digital_data})
                elif "Flipkart" in files.name:
                    digital_data = flipkartInvoice(files.name,request)
                    # if(digital_data):
                    return JsonResponse({'message':digital_data})
        else:
            return JsonResponse({'error':True,'errors':"invalid response"})

def amazonInvoice(path,request):
    ''' Extract amazoninvoice data'''
    a_invoice = extract_data(str(settings.MEDIA_ROOT+path),input_module=pdftotext)
    desc=""
    for key in a_invoice['lines']:
        for val in key:
            if val=='description':
                desc+=key[val]+","
    insert = Userpdfdata(buyer=a_invoice['issuer'],invoice_number=a_invoice['invoice_number'],seller=a_invoice['partner_name'],invoice_date=a_invoice['date'],items=desc,digitalized="digitized")
    insert.save(force_insert=True)
    digital_data=list(Userpdfdata.objects.all().values_list())
    return digital_data

def flipkartInvoice(path,request):
    '''Extract flipkartinvoice data'''
    f_invoice = extract_data(str(settings.MEDIA_ROOT+path),input_module=pdftotext)
    insert = Userpdfdata(buyer=f_invoice['issuer'],invoice_number=f_invoice['invoice_number'],seller=f_invoice['issuer'],invoice_date=f_invoice['date'],items=f_invoice['desc'],digitalized="digitized")
    insert.save(force_insert=True)
    digital_data=list(Userpdfdata.objects.all().values_list())
    return digital_data
