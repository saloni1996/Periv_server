# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from .models import Pollutants

from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions

import unirest
import json
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
import pandas as pd
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

so= []
no= []
pm25=[]
co=[]
o3=[]
hum11=[]
# Create your views here.
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def data_save(request):
    noOfhours=48;
    DEVICE_ID = request.data['d_id']
    #DEVICE_ID = 'CPCB_64'

    #print DEVICE_ID
    response= unirest.get("https://openenvironment.p.mashape.com/all/public/data/hours/"+str(noOfhours)+"/"+DEVICE_ID,
      headers={
        "X-Mashape-Key": "G2v9SeAYZDmshOQcIodXHnaRjpChp1CqdwLjsnMURaezdTxudI",
        "Accept": "application/json"
      })

    raw_response = response.raw_body

    jsonResponse = json.loads(response.raw_body);
    #print raw_response



    sumso2=0
    sumno2=0
    sumo3=0
    sumhum=0
    sumco=0
    sumpm25=0



    global so
    global no
    global o3
    global co
    global pm25
    global hum11




    for i in range(0,48):

        if 'aqi' in jsonResponse[i]:
            aqi1=jsonResponse[i]['aqi']
        else:
            aqi1=hackr.generator.digits(150,1)

        if 'no2' in jsonResponse[i]['payload']['d']:
            #print jsonResponse[i]['payload']['d']['no2']
            f=jsonResponse[i]['payload']['d']['no2'];
            no21=f
            no.append(no21)
        else:
            no21=0.
            no.append(no21)

        if 'co' in jsonResponse[i]['payload']['d']:
            #print jsonResponse[i]['payload']['d']['co']
            f=jsonResponse[i]['payload']['d']['co'];
            co1=f
            co.append(co1)
        else:
            co1=0.
            co.append(co1)

        if 'so2' in jsonResponse[i]['payload']['d']:
            #print jsonResponse[i]['payload']['d']['so2']
            f=jsonResponse[i]['payload']['d']['so2'];
            so21=f
            so.append(so21)
        else:
            so21=0.
            so.append(so21)

        if 'o3' in jsonResponse[i]['payload']['d']:
            #print jsonResponse[i]['payload']['d']['o3']
            f=jsonResponse[i]['payload']['d']['o3'];
            o31=f
            o3.append(o31)
        else:
            o31=0.
            o3.append(o31)

        if 'pm25' in jsonResponse[i]['payload']['d']:
            #print jsonResponse[i]['payload']['d']['pm25']
            f=jsonResponse[i]['payload']['d']['pm25'];
            pm251=f
            pm25.append(pm251)
        else:
            pm251=0.
            pm25.append(pm251)

        if 'temp' in jsonResponse[i]['payload']['d']:
            #print jsonResponse[i]['payload']['d']['temp']
            f=jsonResponse[i]['payload']['d']['temp'];
            temp1=f
        else:
            temp1=0.

        if 'hum' in jsonResponse[i]['payload']['d']:
            #print jsonResponse[i]['payload']['d']['so2']
            hum1=jsonResponse[i]['payload']['d']['hum']
            hum11.append(hum1)
        else:
            hum1=0.
            hum11.append(hum1)

        P = Pollutants( device_id=DEVICE_ID,
						aqi=jsonResponse[i]['aqi'],
                        so2=so21,
                        no2=no21,
                        o3=o31,
                        hum=hum1,
                        temp=temp1,
                        co=co1,
                        pm25=pm251
                        )


        '''if i<24:
            if so21=='NaN':
                so21=2.13
            if no21=='None':
                no21=22.19
            if co1=='NaN':
                co1=1.24
            if o31=='NaN':
                o31=7.31
            if pm251=='NaN':
                pm251=12.14
            if hum1=='NaN':
                hum11=100

            print no21
            sumso2=sumso2+float(so21)

            sumno2=sumno2+float(no21)
            sumo3=sumo3+float(o31)
            sumhum=sumhum+float(hum1)
            sumco=sumco+float(co1)
            sumpm25=sumpm25+float(pm251)'''

        #print so
        #so = [5,4,2,6,27,89,21,98,65,17]
        #print jsonResponse[i]['aqi']
        P.save()

    sumso2 = sum(so[0:24])
    sumno2 = sum(no[0:24])
    sumo3 = sum(o3[0:24])
    sumhum = sum(hum11[0:24])
    sumpm25 = sum(pm25[0:24])
    sumco = sum(co[0:24])

    avgso2=float(sumso2/24);
    avgno2=float(sumno2/24);
    avgo3=float(sumo3/24);
    avghum=float(sumhum/24);
    avgco=float(sumco/24);
    avgpm25=float(sumpm25/24);

    response_android = str(avgno2) + 'RESPIRATORY AND CARDIOVASCULAR ILLNESS' + str(avgso2) + 'RESPIRATORY AND CARDIOVASCULAR ILLNESS' +str(avgco)+'HEADACHE AND FATIGUE'+str(avgpm25)+'LUNG DAMAGE'+str(avgo3)+'RESPIRATORY ILLNESS'


    return HttpResponse(response_android)

#so = [5,4,2,6,27,89,21,98,65,17]
def graph_so2(request):
    #print so

    so_list=so[0:10]
    print so_list
    fig=plt.figure() #Plots in matplotlib reside within a figure object, use plt.figure to create new figure
    #Create one or more subplots using add_subplot, because you can't create blank figure
    ax = fig.add_subplot(1,1,1)
    #Variable
    x = [0,1,2,3,4,5,6,7,8,9]
    ax.plot(x,so_list,'b--') # Here you can play with number of bins Labels and Tit

    start_time= datetime.datetime.now()
    title_so2 = 'SO2 LEVELS FOR PAST 10 HOURS '+str(start_time)
    plt.title(title_so2)
    plt.xlabel('Time')
    plt.ylabel('Value microgram/m3')
    plt.savefig("/home/mmps/hack_data/so2.png")
    image_data = open("/home/mmps/hack_data/so2.png", "rb").read()
    return HttpResponse(image_data)



def graph_no2(request):
    no_list=no[0:10]
    fig=plt.figure() #Plots in matplotlib reside within a figure object, use plt.figure to create new figure
    #Create one or more subplots using add_subplot, because you can't create blank figure
    ax = fig.add_subplot(1,1,1)
    #Variable
    x = [0,1,2,3,4,5,6,7,8,9]
    ax.plot(x,no_list,'r--') # Here you can play with number of bins Labels and Tit

    start_time= datetime.datetime.now()
    title_no2 = 'NO2 LEVELS FOR PAST 10 HOURS '+str(start_time)
    plt.title(title_no2)
    plt.xlabel('Time')
    plt.ylabel('Value microgram/m3')
    plt.savefig("/home/mmps/hack_data/no2.png")
    image_data = open("/home/mmps/hack_data/no2.png", "rb").read()
    return HttpResponse(image_data)


def graph_o3(request):
    o3_list=o3[0:10]
    fig=plt.figure() #Plots in matplotlib reside within a figure object, use plt.figure to create new figure
    #Create one or more subplots using add_subplot, because you can't create blank figure
    ax = fig.add_subplot(1,1,1)
    #Variable
    x = [0,1,2,3,4,5,6,7,8,9]
    ax.plot(x,o3_list,'g--') # Here you can play with number of bins Labels and Tit

    start_time= datetime.datetime.now()
    title_03 = 'Ozone LEVELS FOR PAST 10 HOURS '+str(start_time)
    plt.title(title_03)
    plt.xlabel('Time')
    plt.ylabel('Value microgram/m3')
    plt.savefig("/home/mmps/hack_data/o3.png")
    image_data = open("/home/mmps/hack_data/o3.png", "rb").read()
    return HttpResponse(image_data)


def graph_co(request):
    co_list=co[0:10]
    fig=plt.figure() #Plots in matplotlib reside within a figure object, use plt.figure to create new figure
    #Create one or more subplots using add_subplot, because you can't create blank figure
    ax = fig.add_subplot(1,1,1)
    #Variable
    x = [0,1,2,3,4,5,6,7,8,9]
    ax.plot(x,co_list,'c--') # Here you can play with number of bins Labels and Tit

    start_time= datetime.datetime.now()
    title_co = 'CO LEVELS FOR PAST 10 HOURS '+str(start_time)
    plt.title(title_co)
    plt.xlabel('Time')
    plt.ylabel('Value milligram/m3')
    plt.savefig("/home/mmps/hack_data/co.png")
    image_data = open("/home/mmps/hack_data/co.png", "rb").read()
    return HttpResponse(image_data)


def graph_pm25(request):
    pm25_list=pm25[0:10]
    fig=plt.figure() #Plots in matplotlib reside within a figure object, use plt.figure to create new figure
    #Create one or more subplots using add_subplot, because you can't create blank figure
    ax = fig.add_subplot(1,1,1)
    #Variable
    x = [0,1,2,3,4,5,6,7,8,9]
    ax.plot(x,pm25_list,'m--') # Here you can play with number of bins Labels and Tit

    start_time= datetime.datetime.now()
    title_pm25 = 'PM25 LEVELS FOR PAST 10 HOURS '+str(start_time)
    plt.title(title_pm25)
    plt.xlabel('Time')
    plt.ylabel('Value microgram/m3')
    plt.savefig("/home/mmps/hack_data/pm25.png")
    image_data = open("/home/mmps/hack_data/pm25.png", "rb").read()
    return HttpResponse(image_data)

def pie_chart(request):
    labels= 'so2', 'no2', 'o3', 'hum', 'pm25',

    if(so[0]=='NaN'):
        so[0]=2.13
    if(no[0]=='NaN'):
        no[0]=22.19
    if(co[0]=='NaN'):
        co[0]=1.24
    if(o3[0]=='NaN'):
        o3[0]=7.31
    if(pm25[0]=='NaN'):
        pm25[0]=12.14
    if(hum11[0]=='NaN'):
        hum11[0]=100
    sizes = [so[0],no[0],o3[0],hum11[0],pm25[0]]
    fig1, ax1 = plt.subplots()
    explode = (0.1, 0.1, 0.1, 0.1,0.1)
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.savefig("/home/mmps/hack_data/pie_chart.png")
    image_data = open("/home/mmps/hack_data/pie_chart.png", "rb").read()
    return HttpResponse(image_data)

#@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def predictive_analytics(request):
    #dev_id='CPCB_64'
    pollutant_data= pd.DataFrame(list(Pollutants.objects.all()[0:450].values()))


    features=['so2','no2','o3','co','pm25']
    data_X = pollutant_data.filter(['so2','no2','o3','co','pm25'], axis=1)
    target=['aqi']
    data_Y=pollutant_data[['aqi']].copy()

    train_X = data_X[:-40]
    test_X = data_X[-40:]

    train_Y = data_Y[:-40]
    test_Y = data_Y[-40:]

    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(train_X,train_Y)

    predicted_Y=clf.predict(test_X)
    res=accuracy_score(test_Y, predicted_Y)
    print "Test Accuracy  :: ", res
    #for i in range(0,50):
    #    print pollutant_data[i]
    return HttpResponse(str(res))
''''
    train_data,test_data = pollutant_data.random_split(.8,seed=0)
    my_features=['so2','no2','o3','co','pm25']
    my_features_model = graphlab.linear_regression.create(train_data,target='aqi',features=my_features,validation_set=None)
'''
