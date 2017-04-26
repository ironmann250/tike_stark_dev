from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from tickapp.models import profile,ticket,tickettype,Show
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
# Create a pin code
import random
import string
import smtplib
import json
from smsapi.client import SmsAPI
from smsapi.responses import ApiError


api = SmsAPI()

api.set_username('tike')
api.set_password('869579e0598bd70a216261a80507efed')
api.auth_token = 'q6QWErR7qkI9MNzA4bJJ86fltC5KfselYYiO2DUi'
    #sending SMS

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


#creating an email
me='tikerwanda@gmail.com'
  


@login_required
def sell(request):
    if request.user.is_authenticated():
        username = request.user.username
        objs = profile.objects.get(seller__username=username)
        event = objs.event
        tickobjs=list()
        tickobjs = tickettype.objects.filter(event= event)
        ticket_types=list()
        ticketdict = {}
        for tickobj in tickobjs:
            ticket_types.append(tickobj.tike_types)
            element = ticket_types[-1]
            ticketdict[element]=(tickobj.amount)
        show = Show.objects.get(title = event)
        total = show.tickets_no 
        soldobj = list()
        stobj = list()
        sumofsalesobj=list()
        sumofsalesobjs = ticket.objects.filter(seller__seller__username =username)
        sum = 0
        for sumofsalesobj in sumofsalesobjs:
            sum= sum + sumofsalesobj.ticket_type.amount
        soldobj = ticket.objects.filter(event= show)
        sold= len(soldobj)
        stobj = ticket.objects.filter(event = event, seller= objs)
        st= len(stobj)
        perc =  (sold/total)* 100
    if request.method == 'POST':
        event= request.POST['event']
        ticket_type = request.POST['ticket_type']
        name= request.POST['name']
        email= list()
        email.append(request.POST['email'])
        tel= request.POST['tel']
        usage = request.POST['usage'] 
        pin = id_generator()
        eventobj= Show.objects.get(title = event)
        sellerobj= profile.objects.get(seller__username = username)
        tobj= tickettype.objects.get(tike_types = ticket_type)
        fee = tobj.amount
        datetime= eventobj.date 
        
        try:
            pinobj=ticket.objects.get(Q(pin__exact = pin))
            if pinobj:
                pin = id_generator()
        except ticket.DoesNotExist:
            pass
        if usage == '0':
            try:
                sold1 = sold +1
                htmlmsg = render_to_string('html/essay/email.html',{'event':event,'names': name,'ticket_type':ticket_type,'fee': fee,'date':datetime,'pin':pin,'sold':sold1})
                send_mail('Your ticket to attend the event','',me,email,html_message= htmlmsg, fail_silently= False)
                newticket= ticket.objects.create()
                newticket= ticket(phone_number = tel, email= email, Name= name, pin = pin, event = eventobj, seller= sellerobj,ticket_type= tobj)
                newticket.save()
            except smtplib.SMTPException:
                return render(request,'html/essay/sell.html',{'view' : 'Sell', 'event': event, 'ticket_types' : ticket_types, 'action': True,'username':username,'st': st, 'income': sum,'ticketdict': ticketdict , 'total': total,'sold': sold,'perc': perc,'email':email,'pin':pin})
            
            total = total
            st = st + 1
            sold = sold + 1
            perc = (sold/total)* 120
            return render(request,'html/essay/sell.html',{'view' : 'Sell', 'event': event, 'ticket_types' : ticket_types, 'action': False,'username':username,'st':st,'income': 0,'ticketdict': ticketdict,'total': total,'sold': sold,'perc': perc,'email':email })
        if usage == '1':
            
            try:
                sold1= sold +1
                api.service('sms').action('send')
                msg = "Owner:"+name+"\nEvent:"+event +"\nCode:"+str(pin)+'\nvenue:'+str(ticket_type) +"\nTicket:"+str(fee)+'\nDate:'+str(datetime)
                api.set_content('  Ticket [%3%] \n  [%1%] \n Issued by Tike ltd\nplease keep this ticket safe.\n Any question call [%2%]. ')
                Phone = '250789267775'
                api.set_params(msg,Phone,sold1)
                api.set_to(tel)
                api.set_from('Tike') #Requested sender name
                result = api.execute()
                for r in result:
                    print (r.id, r.points, r.status)
                sum = sum + fee
                st = st + 1
                sold = sold + 1
                perc = (sold/total)* 120
                newticket= ticket.objects.create()
                newticket= ticket(phone_number = tel, email= email, Name= name, pin = pin, event = eventobj, seller= sellerobj,ticket_type= tobj)
                newticket.save()
                print(pin)
                return render(request,'html/essay/sell.html',{'view' : 'Sell', 'event': event, 'ticket_types' : ticket_types, 'action': False,'username':username,'st':st,'income': sum,'ticketdict': ticketdict,'total': total,'sold': sold,'perc': perc,'tel': tel })
            except ApiError as e:
                print(tel)
                print ('%s - %s' % (e.code, e.message))
                return render(request,'html/essay/sell.html',{'view' : 'Sell', 'event': event, 'ticket_types' : ticket_types, 'action': True,'username':username,'st': st, 'income': 0,'ticketdict': ticketdict , 'total': total,'sold': sold,'perc': perc,'tel':tel})
            
        
        
    else:
        print(sum)
        return render(request,'html/essay/sell.html',{'view' : 'Sell', 'event': event,'ticket_types': ticket_types,'username': username,'st':st,'income': sum,'ticketdict': ticketdict,'total': total,'sold': sold,'perc': perc,})
   

    
   
 
            #events=list()
'''
            for obj in objs :
                events.append(obj.event)
                tickets_types=list()
'''
'''
            for event in events:
                global ticket_type
                tickobjs= ticket_type.objects.filter(event = event)
                tickets_types.append('nothing')
                tickets_types[:] = []
                for tickobj in tickobjs:
                    ticket_types.append(tickobj.tike_type)
                    if event not in eventdict:
                        eventdict[event] = list()
                        eventdict[event].append(tickets_types)
'''
   
@login_required
def restore(request):
    
    
    return render(request,'html/essay/restore.html',{'view' : 'Restore'})
@login_required
def check(request):
    if request.method == 'POST':
        pin = request.POST['pin']
        try:
            tickobj=ticket.objects.get(Q(pin__exact = pin))
            owner= tickobj. Name
            ticket_type = tickobj.ticket_type
            status = tickobj.status
            if(status == False):
                tickobj.status = True
                status = True
                tickobj.save()
                return render(request,'html/essay/check.html',{'view' : 'Check','status':status,'owner':owner,'ticket_type': ticket_type,'pin':pin})
            else:
                status = False
                return render(request,'html/essay/check.html',{'view' : 'Check','status':status,'owner':owner,'ticket_type': ticket_type})
        except ticket.DoesNotExist:
            status = False
            return render(request,'html/essay/check.html',{'view' : 'Check','status': status,'pin':pin})

   

    else:
        return render(request,'html/essay/check.html',{'view' : 'Check'})
@login_required
def transfer(request):
    if request.method == 'POST':
        tel1 = request.POST['tel1']
        tel2 = request.POST['tel2']
        pin = request.POST['pin']
        try:
            tickobj=ticket.objects.get(Q(phone_number__exact = tel1, pin__exact = pin ))
            try:
                pinobj=ticket.objects.get(Q(pin__exact = pin))
                if pinobj:
                    pin = id_generator()
            except ticket.DoesNotExist:
                pass
            try:
                api.service('sms').action('send')
                api.set_content('  valid ticket(250)  \nOwner:[%1%]\nEvent: [%2%]\nTicket: [%4%]\nCode:[%3%]\nIssued by Tike ltd\nplease keep this ticket safe. ')
                api.set_params(name, event , pin, ticket_type)
                api.set_to(tel2)
                api.set_from('Tike') #Requested sender name
                result = api.execute()
                for r in result:
                    print (r.id, r.points, r.status)
                total = total
                st = st + 1
                sold = sold + 1
                perc = (sold/total)* 120
                newticket= ticket.objects.create()
                newticket= ticket(phone_number = tel2, email= email, Name= name, pin = pin, event = eventobj, seller= sellerobj,ticket_type= tobj)
                newticket.save()
                print(pin)
                return render(request,'html/essay/transfer.html',{'view' : 'Transfer','status':1})
            except ApiError as e:
                print(tel)
                print ('%s - %s' % (e.code, e.message))
                return render(request,'html/essay/transfer.html',{'view' : 'Transfer','status':0})
        except ticket.DoesNotExist:
            return render(request,'html/essay/transfer.html',{'view' : 'Transfer','status':0})
    else:
        pass
        return render(request,'html/essay/transfer.html',{'view':'Transfer'})
    
def result(request):
    
    if request.method == 'GET':
        pin= request.GET['pin']
        try:
            tickobj=ticket.objects.get(Q(pin__exact = pin))
            owner= tickobj.Name
            ticket_type = tickobj.ticket_types
            status = tickobj.status
            if(status == False):
                tickobj.status = True
                status = True
                tickobj.save()
                result= {'status':status,'owner':owner,'ticket_type': ticket_type,'pin':pin}
                jsonresult = json.dumps(result)
                return jsonresult
            else:
                status = False
                result= {'status':status,'owner':owner,'ticket_type': ticket_type,'pin':pin} 
                jsonresult = json.dumps(result)
                return jsonresult
        except ticket.DoesNotExist:
            status = False
            result= {'status':status,'owner':owner,'ticket_type': ticket_type,'pin':pin} 
            jsonresult = json.dumps(result)
            return jsonresult

def applogin(request):
    if request.method == 'GET':
        username = request.GET['username']
        password = request.GET['password']
        try:
            profobj = User.objects.get(Q(username__exact = username))
            tpassword = profobj.password
            if password == tpassword :
                result = {'status':True}
                jsonresult= json.dumps(result)
                return jsonresult
            else:
                result = {'status': False}
        except User.DoesNotExist:
            result = {'status': False}