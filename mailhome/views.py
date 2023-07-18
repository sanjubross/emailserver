from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
import requests
import datetime
import pandas as pd
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from .forms import PageForm

# mail send funtion view
@api_view(['GET', 'POST'])
def mail_send(request):

    url = "https://emailapi.netcorecloud.net/v5.1/mail/send"
    
    if request.method == "POST":
        if request.FILES.get("upload_csv"):

            upload_csv = request.FILES.get("upload_csv")
            df = pd.read_csv(upload_csv)
            text_series = df.iloc[:,0].astype(str)

            # Join the text Series into a single string
            text_string = ', '.join(text_series)

            # bcc = request.POST.get("bcc")
            # data = str(bcc)
            for email_id in text_string.split(', '):
                print(f"(email: {email_id}),")
                payload = {
                    "from": {
                        "email": "info@kpclasses.co.in",
                        "name": "KP Classes"
                    },
                    "subject": request.POST.get("subject"),
                    # "template_id": 0,
                    "tags": ["Pawnee"],
                    "content": [
                        {
                            "type": "html",
                            "value": request.POST.get("content")
                        }
                    ],
                    "personalizations": [
                        {
                            "attributes": {
                                "LEAD": "Andy Dwyer",
                                "BAND": "Mouse Rat"
                            },
                            "to": [
                                {
                                    "email": "info@kpclasses.co.in",
                                    "name": "KP Classes"
                                }
                            ],
                            "bcc": [{ "email": email_id },],
                            "token_to": "noble-land-mermaid",
                            "token_cc": "MSGID657243",
                            "token_bcc": "MSGID657244",
                            # "attachments": [
                            #     {
                            #         "name": request.POST.get("attach"),
                            #         "content": "base64 encoded file content"
                            #     }
                            # ]
                        }
                    ],
                    "settings": {
                        "open_track": True,
                        "click_track": True,
                        "unsubscribe_track": True,
                        "ip_pool": "shared"
                    },
                }
        elif request.POST.get("to"):
            payload = {
                    "from": {
                        "email": "info@kpclasses.co.in",
                        "name": "KP Classes"
                    },
                    "subject": request.POST.get("subject"),
                    # "template_id": 0,
                    "tags": ["Pawnee"],
                    "content": [
                        {
                            "type": "html",
                            "value": request.POST.get("content")
                        }
                    ],
                    "personalizations": [
                        {
                            "attributes": {
                                "LEAD": "Andy Dwyer",
                                "BAND": "Mouse Rat"
                            },
                            "to": [
                                {
                                    "email": request.POST.get("to"),
                                }
                            ],
                            "token_to": "noble-land-mermaid",
                            "token_cc": "MSGID657243",
                            "token_bcc": "MSGID657244",
                            # "attachments": [
                            #     {
                            #         "name": request.POST.get("attach"),
                            #         "content": "base64 encoded file content"
                            #     }
                            # ]
                        }
                    ],
                    "settings": {
                        "open_track": True,
                        "click_track": True,
                        "unsubscribe_track": True,
                        "ip_pool": "shared"
                    },
                }
    headers = {
        "api_key": "7e4927ff91726d2495ed2cf0c4719c67",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # print(request.FILES["attach"])

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    return Response(data, status=status.HTTP_200_OK)

# home function view
@login_required(login_url='/s/login')
def mail_home(request):
    context = {
       'form': PageForm
    }    
    return render(request, template_name="mail/home.html", context=context)

@login_required(login_url='/s/login')
def sent_mail(request):
    
    url = "https://emailapi.netcorecloud.net/v5.1/stats"
    
    headers = {
        "api_key": "7e4927ff91726d2495ed2cf0c4719c67",
        "Accept": "application/json"
    }

    querystring = {"startdate":datetime.datetime.now().date() - datetime.timedelta(days=6),"enddate":datetime.datetime.now().date(),"aggregated_by":"day"}

    response = requests.get(url, headers=headers, params=querystring)

    dateWise = response.json()

    print(dateWise)

    date = dateWise['data']['datewise']
            
    dates = []
    for i in date.keys():
        dates.append(i)

    totalMail = 0
    sent = []
    for j in date.values():
        totalMail += j['sent']
        sent.append(j['sent'])
    
    print("total mails: ", totalMail)

    context = {
        'dates':dates,
        'sent': sent,
        'totalMail': totalMail
    }

    return render(request, template_name="mail/mail_sent.html", context=context)

# login function view
def login_attempt(request):
    if request.user.is_authenticated:
        return redirect(reverse('mailhome'))
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(username=email)
        
        if not user_obj.exists():
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username=email, password=password)
        
        if user_obj:
            login(request, user_obj)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('/')
        
        messages.warning(request, 'Invalid Credentials!')
        return HttpResponseRedirect(request.path_info)

    return render(request, template_name="credentials/login.html")

@login_required(login_url='/s/login')
def signout(request):
    logout(request)
    return redirect("/")