from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Domain

from Sublist3rMaster import sublist3r
import subprocess,re,time,socket


# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    if request.method=='POST':
        
        try:
            print(socket.gethostbyname(request.POST.get('domain')))
            return redirect('details')
        except:
            return HttpResponse("Invalid Doamin!!!")
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def DetailsPage(request):
    if request.method=='POST':
        try:
            socket.gethostbyname(request.POST.get('domain'))
            domain=request.POST.get('domain')
            sublist3r.main(domain, 40, 'subdomains.txt', ports= None, silent=False, verbose= False, enable_bruteforce= False, engines=None)
            subprocess.Popen(['httpx.exe','-list','subdomains.txt','-o','httpx_data.txt','-sc','-cl','-nc','-rt','-title','-ip','-cname','-cdn','-td'])
            subprocess.Popen(['naabu.exe','-list','subdomains.txt','-o','naabu_data.txt','-nc'])
            subprocess.Popen(['gowitness.exe','file','--file','subdomains.txt','--screenshot-path','screenshots'])

            time.sleep(110)

            with open('subdomains.txt','r') as f:
                sub_domains = [line.rstrip() for line in f.readlines() if line!='\n']
            ports={}
            with open('naabu_data.txt','r') as f:
                for line in f.readlines():
                    subdomain,port=line.split(':')
                    if ports.get(subdomain):
                        ports[subdomain].append(port.rstrip())
                    else:
                        ports[subdomain]=[port.rstrip()]
            details={}
            with open('httpx_data.txt','r') as f:
                for line in f.readlines():
                    individual_details={}
                    subdomain,data=line.split(" ",1)
                    subdomain=subdomain.split('//')[1]
                    data_split=re.compile('\[[^]]*\]').findall(data)
                    if len(data_split)==7:
                        individual_details['status_code']=data_split[0].strip('[]')
                        individual_details['content_length']=data_split[1].strip('[]')
                        individual_details['title']=data_split[2].strip('[]')
                        individual_details['ip']=data_split[3].strip('[]')
                        individual_details['cname']=data_split[4].strip('[]')                    
                        individual_details['response_time']=data_split[5].strip('[]')
                        individual_details['technologies']=[t for t in data_split[6].strip('[]').split(',')]
                    elif len(data_split)==6:
                        individual_details['status_code']=data_split[0].strip('[]')
                        individual_details['content_length']=data_split[1].strip('[]')
                        individual_details['title']=data_split[2].strip('[]')
                        individual_details['ip']=data_split[3].strip('[]')
                        individual_details['cname']=None
                        individual_details['response_time']=data_split[4].strip('[]')
                        individual_details['technologies']=[t for t in data_split[5].strip('[]').split(',')]
                    details[subdomain]=individual_details
            Domain.objects.create(
                user=request.user,
                details=details,
                ports=ports,
                subdomains=sub_domains,
            )
            return render(request,'details.html',{'sub_domains':sub_domains,'details':details,'ports':ports})
        except:
            return HttpResponse("Network error or Invalid Doamin!!!")
    else:
        return HttpResponse("Incorrect request!!!")