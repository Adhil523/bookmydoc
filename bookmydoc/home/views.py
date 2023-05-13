from django.shortcuts import render
from .models import Bookings,Clinic
from datetime import datetime, timedelta
import openai,os
from dotenv import load_dotenv
import re
load_dotenv()
api_key=os.getenv("OPENAI_KEY", None)

# Create your views here.
def homes(request):
    if request.method=='POST':
        pname=request.POST["pname"]
        print(pname)
        loc=request.POST["loc"]
        landmark=request.POST["landmark"]
        dis=request.POST["dis"]
        list1=[pname,loc,landmark,dis]
        request.session['list1']=list1
        return render(request,'slot.html')
    return render(request,'home.html')
def slot(request):
    if request.method=='POST':
        bdate=request.POST["bdate"]
        btime=request.POST["btime"]
        start=btime[0:8]
        end=btime[12:]
        start_time = datetime.strptime(start, '%I:%M %p')
        end_time = datetime.strptime(end, '%I:%M %p')
        interval = timedelta(minutes=20)

        current_time = start_time
        l2=[]
        while current_time < end_time:
            l2.append(current_time.strftime('%I:%M %p'))
            current_time += interval
        obj=Clinic.objects.all()
        list2=request.session.get('list1')
        dict_dis={}
        for i in obj:
            loc1=i.loc
            landmark1=i.landmark
            dis1=i.dis
            openai.api_key=api_key
            prompt="What is the distance between "+landmark1+" "+loc1+ " and "+list2[2]+" "+list2[1]+" ,both in "+dis1+",India.Give the answer in numerical form only without showing km" 
            response=openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                max_tokens=256,
                temperature=0.7

            )
            print(response)
            str1=response['choices'][0]['text']

            print(str1)
            #str1=str1[2:]
            #st=str1.split(' ')
            #dict_dis[i.cname]=float(st[0])
            st=int(re.search(r'\d+', str1).group())
            dict_dis[i.cname]=st
        print(dict_dis)
        m=10
        st=""
        for i in dict_dis:
            if dict_dis[i]<=m:
                m=dict_dis[i]
                st=i
        print(st)
        obj=Clinic.objects.get(cname=st)
        s=obj.workhour_b
        start=s[0:8]
        end=s[12:]
        start_time = datetime.strptime(start, '%I:%M %p')
        end_time = datetime.strptime(end, '%I:%M %p')
        interval = timedelta(minutes=20)

        current_time = start_time
        l=[]
        while current_time < end_time:
            l.append(current_time.strftime('%I:%M %p'))
            current_time += interval
        s=obj.workhour_a
        start=s[0:8]
        end=s[12:]
        start_time = datetime.strptime(start, '%I:%M %p')
        end_time = datetime.strptime(end, '%I:%M %p')
        interval = timedelta(minutes=20)

        current_time = start_time
        while current_time < end_time:
            l.append(current_time.strftime('%I:%M %p'))
            current_time += interval
        obj=Bookings.objects.all()
        for i in obj:
            if i.slot in l and i.cname==st:
                l.remove(i.slot)
        
        stnew=""
        for i in l2:
            if i in l:
                c=1
                stnew=i
                break
        
        dict_res={"pname":list2[0],"cname":st,"slot":stnew,"d":bdate} 
        request.session['dict_res']=dict_res
        return render(request,'result.html',dict_res)
       
        
def dummy(request):
    return render(request,'home.html')

def book(request):
    dict_res=request.session.get('dict_res')
    Bookings.objects.create(**dict_res)
    return render(request,'success.html',dict_res)
def medigo(request):
    if request.method=='POST':
        pres=request.POST['pres']
        dis=request.POST['dis']
        age=request.POST['age']
        allergy=request.POST['allergy']
        openai.api_key=api_key
        prompt="A person is prescribed "+ pres+" for the diagonosis of "+dis+" .List out the main medicines and extra supplements from the prescription."
        response=openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=prompt,
                    max_tokens=256,
                    temperature=0.7

                )
        str1=response['choices'][0]['text']
        print(str1)
        st=str1.split("upplements:")
        print(st)
        stnew=st[1]
        print(stnew)
        prompt="Find  names of cheaper drugs if any for the supplements"+stnew+" for a person of age "+age +" and "+allergy+" allergies."
        response=openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=prompt,
                    max_tokens=256,
                    temperature=0.7

                )
        str1=response['choices'][0]['text']
        print(str1)
        st=str1.split('\n')
        dict_med={
            'cheap':st
        }
        return render(request,'med.html',dict_med)
    return render(request,'medigo.html')

def em(request):
    if request.method=='POST':
        return render(request,"emesuccess.html")
    return render(request,"eme.html")

