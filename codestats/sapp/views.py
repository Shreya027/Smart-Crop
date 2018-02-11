from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import http.client

from random import randint
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist
from .models import *
import requests
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from textblob import TextBlob
import random
import re

import cv2
import sys
import logging as log
import datetime as dt
from time import sleep 


import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json
from PIL import Image
subscription_key = '5979034bfb134316b72d9625b0c320c5'
uri_base = 'https://westcentralus.api.cognitive.microsoft.com'


# Camera 0 is the integrated web cam on my netbook
camera_port = 0
 
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30
 
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
global camera

def recommend(request):
    return render(request, 'blank.html')


@login_required
def chatbot(request):
    return render(request, 'basic_table.html')

@login_required
def compare(request):
    return render(request, 'responsive_table.html')


@login_required
def charts(request):
    return render(request, 'chartjs.html')


@login_required
def to_do(request):
    return render(request, 'todo_list.html')



def gallery(request):
    return render(request, 'gallery.html')


@login_required
def reminders(request):
    return render(request, 'form_component.html')

def get_image():

    retval, im = camera.read()
    return im

@csrf_exempt
def facedetect(request):


    if request.method == 'POST':
        camera = cv2.VideoCapture(camera_port)       
        for i in range(ramp_frames):
            retval,temp = camera.read()
        print("Taking image...")
        retval2, camera_capture = camera.read()
        file = "photographtest.png"

        cv2.imwrite(file, camera_capture)
        del(camera)

        detect('photographtest.png','photographtest.png')
    
    return render(request,'face.html')




def detect(img_sent, img_store):

    headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
    }

  
    params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    #body1 = {'url': 'https://vignette.wikia.nocookie.net/harrypotter/images/c/c1/Harry%2Bpotter-Harry_Potter_HP4_01.jpg'}
    #body2 = {'url': 'https://images.pottermore.com/bxd3o8b291gf/3SQ3X2km8wkQIsQWa02yOY/25f258f21bdbe5f552a4419bb775f4f0/HarryPotter_WB_F4_HarryPotterMidshot_Promo_080615_Port.jpg'}
   
    try:
        #data1 = open('./img1.png', 'rb').read()
        #data2 = open('./img2.png', 'rb').read()

        #data1= Image.open(img_sent)
        #print(data1)
        #data2= Image.open(img_store)
        data1 = open(str(img_sent), 'rb').read()
        data2 = open(str(img_store), 'rb').read()
        print("Hello1")


        response1 = requests.request('POST', uri_base + '/face/v1.0/detect',  data=img_sent, headers=headers, params=params)
        response2 = requests.request('POST', uri_base + '/face/v1.0/detect', data=img_store, headers=headers, params=params)
        print(response1)

        #print ('Response:')
        parsed1 = json.loads(response1.text)
        parsed2 = json.loads(response2.text)
        print("hello2")
        print(parsed1)
        faceId1=parsed1[0]['faceId']
        faceId2=parsed2[0]['faceId']
        print(faceId1,faceId2)


        verify2(faceId1,faceId2)
        #print (json.dumps(parsed, sort_keys=True, indent=2))

    except Exception as e:
        print('Error:')
        print(e)


def verify2(faceId1,faceId2):
    print("Hello")

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }


    params = urllib.parse.urlencode({
    })

    body = { 
        "faceId1": faceId1,
        "faceId2": faceId2,
    }

    try:
    
        response = requests.request('POST', uri_base + '/face/v1.0/verify', json=body, data=None, headers=headers, params=params)
        print(response)
        print ('Response:')
        parsed = json.loads(response.text)
        print(parsed)
        print (json.dumps(parsed, sort_keys=True, indent=2))
    except Exception as e:
        print('Error:')
        print(str(e.message))
        if(str(e.message)=='0'):
            print('Verified')






def send_sms(request):
    message = request.POST.get('message')
    conn = http.client.HTTPConnection("api.msg91.com")
    payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": message, \"to\": [ \"9819515144\"] }] }"
    headers = {
        'authkey': "197517AZ3pT96i9Ef05a7e37ef",
        'content-type': "application/json"
    }

    conn.request("POST", "/api/v2/sendsms", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

    return render(request, 'blank.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        #user_type = request.POST.get('user_type')
        mobile = request.POST.get('mobile')
        aadhar = request.POST.get('aadhar')
        password = randint(1000, 9999)
        # print(user_type)
        #message = "Your OTP for login is: "
        #requests.get('https://control.msg91.com/api/sendhttp.php?authkey=132727AshR9z6QU9Dg58416307&mobiles='+mob+'&message='+a+'&sender=DLFIND&route=4', None)
        if MyUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error1': 'Email already taken by another user', 'first_name': first_name, 'last_name': last_name, 'email': email})
        elif MyUser.objects.filter(mobile_no=mobile).exists():
            return render(
                request,
                'register.html',
                {
                    'error': 'Mobile already registered by another user',
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username,
                    'email': email
                }
            )
        else:
            user = MyUser.objects.create(
                first_name=first_name, last_name=last_name, email=email, username=email, mobile_no=mobile, user_type=user_type)
            user.set_password(password)
            user.save()
            return redirect('/login/')
    else:
        return render(request, 'register.html')


@csrf_exempt
def login_app(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        otp = request.POST.get('otp', None)
        #print(mobile + ' ' + otp)
        if 'mobile' in request.POST and otp is not None:
            try:
                user = MyUser.objects.get(mobile_no=mobile)
            except MyUser.DoesNotExist:
                return redirect('../register')
            email = user.email
            user = None
            user = auth.authenticate(
                username=email, password=str(otp))
            # print(user)
            if user:
                login(request, user)
                return redirect('../')
            else:
                return render(request, 'login.html', {'mobile': mobile, 'error': 'Incorrect OTP'})
        elif 'mobile' in request.POST and otp is None:
            mobile = request.POST.get('mobile')
            otp = str(randint(1000, 9999))
            try:
                user = MyUser.objects.get(mobile_no=mobile)
            except MyUser.DoesNotExist:
                print(mobile)
                return redirect('../register')
            user.set_password(otp)
            user.save()
            message = "Your OTP for login is: " + otp
            requests.get('https://control.msg91.com/api/sendhttp.php?authkey=197517AZ3pT96i9Ef05a7e37ef&mobiles=' +
                         mobile + '&message=' + message + '&sender=CROPPY&route=4', None)
            return HttpResponse()
    else:
        return render(request, 'login.html')



def index(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return redirect('/login/')
#def index(request):
    #if request.user.is_authenticated():
        #return render(request,'index.html')
    #else:
        #return redirect('/login/')

def logout_app(request):
    if request.user.is_authenticated():
        logout(request)
        return redirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


def feedback(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            aadhar = request.POST.get('aadharNumber')
            phoneNo = request.POST.get('phoneNo')
            text_feedback = request.POST.get('text_feedback')
            feedback = Support()
            feedback.user = request.user
            #feedback.aadhar = aadhar
            feedback.support_text = text_feedback
            feedback.is_read = False
            feedback.save()
    return render(request,'feedback.html')



def check_for_energy(sentence):

    resp = "Check out some sites for green energy :"
    link1 ="http://www.iea.org/"
    link2="http://www.renewable-living.com/blog/"
    link3="https://www.cleanenergyresourceteams.org/blog"
    return resp,link1,link2,link3


def check_for_farming(sentence):
    resp = "Check out farming techniques on the following sites : "
    link1 ="https://www.csiro.au/en/Research/Farming-food/Improving-farming-techniques"
    link2 ="http://www.fwi.co.uk/"

    return resp,link1,link2,link3

def check_for_crop(sentence):
    resp = "Check out crop requirements on the following sites : "
    link1 ="http://ucanr.edu/sites/Nutrient_Management_Solutions/stateofscience/Meet_Crop_Nutrient_Requirements/"
    link2 ="https://www1.agric.gov.ab.ca/$department/deptdocs.nsf/all/agdex3791"
    link3="https://www.sswm.info/category/implementation-tools/water-sources/hardware/conservation-soil-moisture/crop-selection"
    return resp,link1,link2,link3



def check_for_soil(sentence):
    resp = "Check out soil requirements and  remedies on the following sites : "
    link1 ="https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/soil-remediation"
    link2 ="https://www.deme-group.com/expertises/soil-remediation-and-treatment"
    link3="http://www.lusern.org/index.php?option=com_content&view=article&id=159&Itemid=234"
    return resp,link1,link2,link3



def check_for_water(sentence):
    resp = "Check out water requirements and remedies on the following sites : "
    link2 ="http://www.fao.org/nr/water/aquastat/water_use_agr/index.stm"
    link1 ="http://agritech.tnau.ac.in/agriculture/agri_irrigationmgt_waterrequirements.html"
    link3="http://againstwaterpollution.blogspot.in/2010/12/remedies-for-water-pollution.html"
    return resp,link1,link2,link3



def check_for_air(sentence):
    resp = "Check out air requirements and remedies on the following sites :"
    link1 ="http://green.wikia.com/wiki/How_to_Reduce_Air_Pollution"
    link2 ="http://www.monitor.co.ug/Magazines/Farming/How-air-pollution-affects-agriculture/689860-2656434-133lf48z/index.html"

    return resp,link1,link2,link3


def check_for_fertility(sentence):
    resp = "Check out fertility requirements on the following sites : "
    link1 ="https://www1.agric.gov.ab.ca/$department/deptdocs.nsf/all/agdex3791"
    link2="http://www.smart-fertilizer.com/nutrient-requirements"
    return resp,link1,link2,link3


energy_pattern = re.compile("^energy|^green|^power|^hydro|^solar|^clean")
farming_pattern = re.compile("^farm|^farming|^agriculture|^methods|^techniques|^agro")
crop_pattern = re.compile("^crop|^rice|^maize|^wheat|^cotton|^sugarcane|^potato|^soybean")
soil_pattern = re.compile("^soil")
water_pattern = re.compile("^water")
air_pattern = re.compile("^air")
fertility_pattern = re.compile("^fertile|^fertility|^manure")


def check_for_keywords(sentence):
    link1=None
    link2=None
    link3=None
    resp=None
    for word in sentence.words:
        
        if energy_pattern.match(word.lower()):
            resp,link1,link2,link3 =check_for_energy(sentence)
            
            break
            
        elif farming_pattern.match(word.lower()): 
            
            resp,link1,link2,link3 =check_for_farming(sentence)
            break
          

        elif crop_pattern.match(word.lower()):
            resp,link1,link2,link3=check_for_crop(sentence)
            break
           

        elif soil_pattern.match(word.lower()):
            resp,link1,link2,link3 =check_for_soil(sentence)
            break

        elif water_pattern.match(word.lower()): 
            resp,link1,link2,link3 =check_for_water(sentence)
            break

        elif air_pattern.match(word.lower()): 
            resp,link1,link2,link3 =check_for_air(sentence)
            break

        elif fertility_pattern.match(word.lower()): 
            resp,link1,link2,link3 =check_for_fertility(sentence)
            break

    return resp,link1,link2,link3




greeting_pattern = re.compile("^hello|^hi|^greeting|^sup|^what's up|^hey")

GREETING_RESPONSES = ["Hey, you seem hungry..", "Oh hi there :p ", "Hey food lover :D " , "Hey, what's up ?"]



NONE_RESPONSES = [
    "I didn't get what you said...",
    "I didn't understand. You could ask questions related to climate, green energy, farming techniques, air / water / soil quality",
    "Umm, could you please elaborate ? ",

]

def check_for_greeting(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    for word in sentence.words:
        if greeting_pattern.match(word.lower()) :
            return random.choice(GREETING_RESPONSES)



def request(sentence):
    #cleaned = preprocess_text(sentence)
    parsed = TextBlob(sentence)

    resp= None
    link1=None
    link2=None
    link3=None

    resp,link1,link2,link3 = check_for_keywords(parsed)


    if not resp:
        resp = check_for_greeting(parsed)

    if not resp:
        resp = random.choice(NONE_RESPONSES)

    return resp,link1,link2,link3



def reply(sentence):
    resp,link1,link2,link3  = request(sentence)
    return resp,link1,link2,link3

def chatbot(request):

    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a valid chat')
        
        else:
            resp,link1,link2,link3=reply(q)
            return render(request, 'basic_table.html',
                          {'resp':resp,'link1':link1,'link2':link2,'link3':link3})
        
    return render(request, 'basic_table.html',
              {'errors': errors})
