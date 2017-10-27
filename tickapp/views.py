from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from tickapp.models import profile,ticket,tickettype,Show
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils import timezone
# Create a pin code
import random,datetime
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
            ticket_types.append(tickobj.tike_type)
            element = ticket_types[-1]
            ticketdict[element]=(tickobj.amount)
        show = Show.objects.get(title = event)
        total = show.tickets_no 
        soldobj = list()
        stobj = list()
        sumofsalesobj=list()
        #sumofsalesobjs = ticket.objects.filter(seller =username)#no need since each seller has one event and we already have the event !this is when object relations comes in handy
        sum_ = 0
        #and since they removed object relations in the ticket's table
        #i will play with functional programming just to make it cool
        '''
        claude log:
        an optimisation here based on the codes in tools sadly 
        object relations take's too much space :) what a paradox
        and loops too much time yet they say you need time and space to know
        if i sound as someone who got dumped it's not true i just want to make
        a joke about the codes imma change and the model it is built on  
        '''
        tk_types=[tk_type for tk_type in tickettype.objects.filter(event =event)]
        for tk_type in tk_types:
            factor=tk_type.amount
            query=ticket.objects.filter(Q(event=event.title)&Q(seller=username)&Q(ticket_type=tk_type.tike_type))
            sum_=(len(query)*factor)+sum_#take that dumb loop over tickets KABOOM!          

        '''
        for sumofsalesobj in sumofsalesobjs:
            sum_= sum_ + int(sumofsalesobj.ticket_type)#change to s.tk.amount and there is an efficient way by getting the len check codes in tools
'''
        #strange calculations i tought we were calculating from the total ticket Show.tickets_no
        #:) i don't want to work here anymore, anyway will look into that
        soldobj = ticket.objects.filter(event= show)
        sold= len(soldobj)
        stobj = ticket.objects.filter(event = event, seller= objs)#s__username
        st= len(stobj)
        #better calculation KABOOM! dumb //
        perc =  int(round((sold/(total*1.0))* 100))
    if request.method == 'POST':
        event= request.POST['event']
        ticket_type = request.POST['ticket_type']
        name= request.POST['name']
        email= request.POST['email']
        tel= request.POST['tel']
        usage = request.POST['usage'] 
        pin = id_generator()
        eventobj= Show.objects.get(title = event)
        venue = eventobj.venue
        sellerobj= profile.objects.get(seller__username = username)
        tobj= tickettype.objects.get(tike_type = ticket_type,event__title=event)
        fee = tobj.amount
        datetime= eventobj.date 
        
        try:
            pinobj=ticket.objects.get(Q(pin__exact = pin))
            #another crappy contribution of mine 
            #at exactly the 6*(10e36)th ticket the system crashed
            #come find me... /also it will get slower and slower over time
            while(pinobj):
                pin = id_generator()
                pinobj=ticket.objects.get(Q(pin__exact = pin))
        except ticket.DoesNotExist:
            pass
        if usage == '0':
            try:
                sold1 = sold +1
                '''htmlmsg = render_to_string('html/essay/email.html',{'event':event,'names': name,'ticket_type':ticket_type,'fee': fee,'date':datetime,'pin':pin,'sold':sold1})
                send_mail('Your ticket to attend the event','',me,email,html_message= htmlmsg, fail_silently= False)
                '''
                if event not in ['',' ']:
                    #newticket= ticket.objects.create()
                    newticket= ticket(phone_number = tel, email= email, Name= name, pin = pin, event = event, seller= username,ticket_type= ticket_type,date=timezone.now())#change according to model
                    newticket.save()
            except smtplib.SMTPException:
                return render(request,'html/essay/sell.html',{'view' : 'Sell', 'event': event, 'ticket_types' : ticket_types, 'action': True,'username':username,'st': st, 'income': sum_,'ticketdict': ticketdict , 'total': total,'sold': sold,'perc': perc,'email':email,'pin':pin})
            
            total = total
            st = st + 1
            sold = sold + 1
            perc = (sold/total)* 100
            return render(request,'html/essay/sell.html',{'view' : 'Sell', 'event': event, 'ticket_types' : ticket_types, 'action': False,'username':username,'st':st,'income': 0,'ticketdict': ticketdict,'total': total,'sold': sold,'perc': perc,'email':email })
        if usage == '1':
            
            try:
                sold1= sold +1
                api.service('sms').action('send')
                msg = "Owner:"+name+"\nEvent:"+event +"\nCode:"+str(pin)+'\nvenue:'+str(venue) +"\nTicket:"+str(fee)+'\nDate:'+str(datetime)#.strftime("%d-%m-%y")
                api.set_content('Ticket [%3%] \n[%1%] \nIssued by Tike ltd\nplease keep this ticket safe.\n Any question call [%2%]. ')
                Phone = '250789267775'
                api.set_params(msg,Phone,sold1)
                api.set_to(tel)
                api.set_from('Tike') #Requested sender name
                '''
                result = api.execute()
                for r in result:
                    print (r.id, r.points, r.status)
                '''
                sum_ = sum_ + fee
                st = st + 1
                sold = sold + 1
                perc = (sold/total)* 100
                if event not in ['',' ']:
                    #newticket= ticket.objects.create()
                    newticket= ticket(phone_number = tel, email= email, Name= name, pin = pin, event = event, seller= username,ticket_type= ticket_type,date=timezone.now())
                    newticket.save()
                print(pin)
                return render(request,'html/essay/sell.html',{'view' : 'Sell', 'event': event, 'ticket_types' : ticket_types, 'action': False,'username':username,'st':st,'income': sum_,'ticketdict': ticketdict,'total': total,'sold': sold,'perc': perc,'tel': tel })
            except ApiError as e:
                print(tel)
                print ('%s - %s' % (e.code, e.message))
                return render(request,'html/essay/sell.html',{'view' : 'Sell', 'event': event, 'ticket_types' : ticket_types, 'action': True,'username':username,'st': st, 'income': 0,'ticketdict': ticketdict , 'total': total,'sold': sold,'perc': perc,'tel':tel})
            
        
        
    else:
        print(sum_)
        return render(request,'html/essay/sell.html',{'view' : 'Sell', 'event': event,'ticket_types': ticket_types,'username': username,'st':st,'income': sum_,'ticketdict': ticketdict,'total': total,'sold': sold,'perc': perc,})
   

    
   
 
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
    if request.method == 'POST':#maybe change to GET for quick qrcode scans in a browsers
        pin = request.POST['pin']
        try:
            tickobj=ticket.objects.get(Q(pin__exact = pin))
            owner= tickobj.Name
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
            ticket_type = tickobj.ticket_type
            status = tickobj.status
            if(status == False):
                tickobj.status = True
                status = True
                tickobj.save()
                result= {'status':status,'owner':owner,'ticket_type': ticket_type,'pin':pin}
                return JsonResponse(result)
            else:
                status = False
                result= {'status':status,'owner':owner,'ticket_type': ticket_type,'pin':pin} 
                return JsonResponse(result)
        except ticket.DoesNotExist:
            status = False
            result= {'status': False} 
            return JsonResponse(result)

def applogin(request):
    if request.method == 'GET':
        username = request.GET['username']
        password = request.GET['password']
        user = authenticate(username= username, password= password)
        
        if user is not None:
            result = {'status':True}
            return JsonResponse(result)
        else:
            result = {'status': False}
            return JsonResponse(result) 
@login_required
def tools(request):
    '''
    Munyakabera jean claude log:
    the following includes tools to be used in getting information
    about the operations being undertaken,it is built to easily add
    new components with time first we get general variables and get
    into a body of IFs depending on the tool requested
    '''
    '''
    Alas object relations in thousands of tickets will be make the db too big
    so i'm forced to rewrite my over related yet flexible code ,i yearn for
    the time of quantum computers...
    '''
    if request.user.is_authenticated():
        username=request.user.username
        sellers=[]
        for profl in profile.objects.all():#.ordey_by('seller__username'):
            sellers.append(profl.seller.username)
        events=[]
        for evnt in Show.objects.all():#.order_by('title'):
            events.append(evnt.title)
        days,months,years=[range(32),range(1,13,1),range(datetime.date.today().year-20,datetime.date.today().year+21)]
       
        '''
        with this tools to be able to add different tools and view what you are using
        each tool shall manage it's 'active' key
        put active_toolnum ( for example active_0 for search) into the tab of that tool
        and if that tool is selected send 'active' for that key
        '''
        if request.method=='GET': #post or get? change according to needs
            if "toolnum" in request.GET.keys(): #to see if they want a tool and avoid an error if not
                toolnum=request.GET["toolnum"]
                '''
                Munyakabera Jean Claude log:
                i would like to suggest that there is a more useful way of adding tools the logic of selecting
                them is the same what is different is instead of writing long lines of codes following each
                if statement we make a file "tools.py" then call it and get different tools from there for now
                i won't pursue this approach since i'm supposed to deliver this tonight
                '''
                if toolnum=="0": #search
                    '''
                    foreword it searches tickets with some variables and will search
                    with any number of varible it is given when given a date it will 
                    give all tickets only if the date is a date of 0s(or maybe just the day) otherwise it
                    will give tickets of that date only, oh and it will differentiate 
                    phones with emails so only one field for contact info may add this
                    in the sell view
                    '''
                    search_vars=['event','seller','name','pin','contacts','day','month','year'] #all fields contained in the search page
                    tmp=""
                    search_queries=[Q(event__title=tmp),Q(seller__username=tmp),]
                    query_keywords=Q()
                    date=datetime.date.today()
                    #following is a functional approach to assign values for fields queried accurate only when search is done in a certain order
                    #i think there is a better way to do it in django till then imma use this idea
                    qevent,qseller,qname,qpin,qcontacts,qday,qmonth,qyear=[request.GET[var] for var in search_vars if var in request.GET.keys()]
                    for search_var in search_vars:
                        #print search_var,str(request.GET[search_var])
                        if search_var in request.GET.keys():
                            if search_var=="event" and request.GET[search_var] not in ['',' ',None]:
                                query_keywords= query_keywords & Q(event=request.GET[search_var])
                            elif search_var=="name" and request.GET[search_var] != '':
                                query_keywords= query_keywords & Q(Name__contains=request.GET[search_var])
                            elif search_var=="seller" and request.GET[search_var] != '':
                                query_keywords= query_keywords & Q(seller=request.GET[search_var])
                            elif search_var=="pin" and request.GET[search_var] != '':
                                query_keywords= query_keywords & Q(pin=request.GET[search_var].upper())
                            elif search_var=="contacts" and request.GET[search_var] != '':
                                if "@" in request.GET[search_var]:
                                    query_keywords= query_keywords & Q(email=request.GET[search_var])
                                elif request.GET[search_var] != '' and search_var != '':
                                    query_keywords= query_keywords & Q(phone_number=int(request.GET[search_var]))
                            #:) i'm too lazy to figure out what went wrong here
                            #is it the i don't send dates in the right format ?
                            #or is there some bugs in my overly sophisticated date retrieval system?
                            elif search_var in ["day",'month','year'] and request.GET[search_var] != '0':
                                if search_var == "day":   
                                    date.replace(day=int(request.GET[search_var]))
                                elif search_var=="month":
                                    date.replace(month=int(request.GET[search_var]))
                                elif search_var=="year":
                                    date.replace(year=int(request.GET[search_var]))
                    #only uncomment if you had the guts to collect the above bug with date
                    #else python will scream at you ,or is it you?
                    '''if date != datetime.date.today():
                        query_keywords= query_keywords #& Q(date__eq=join(date))'''
                    results=''
                    if str(query_keywords)not in ['(AND: )',]:
                        results=ticket.objects.filter(query_keywords)
                    parsed_results=[]
                    #print str(query_keywords),'---->',(results)#debug purposes only
                    for result in results: #this is rather unefficient will remove it once i know how to use managers or templating functions, or go ahead and do it
                        parsed_results.append(
                            [str(result.Name).lower().strip(),
                            str(result.event).lower().strip(),
                            str(result.ticket_type).lower().strip(),
                            str(result.pin).lower().strip(),
                            str(result.seller).lower().strip(),#result.seller result in an error
                            result.date.strftime("%d-%m-%y"),
                            str(result.phone_number),result.status])

                    
                    return render(request,'html/essay/search.html',{"err_disp":'none','active_0':'active','view':str(query_keywords),'days':days,'months':months,'years':years,'sellers':sellers,'events':events,'results':parsed_results,
                        })
                elif toolnum=='1':#seller stats
                    #thinking...
                    #see which show the current user supervise if none KABOOM!
                    try:
                        cur_show=Show.objects.get(Q(supervisor__username=username))
                        show_tickets=cur_show.tickets_no
                        #get available tike types for an efficient price calculator for only that event
                        cur_types=tickettype.objects.filter(event=cur_show)
                        #get all the sellers for this event
                        cur_sellers=profile.objects.filter(event=cur_show)
                        #for each type and seller get all tickets and record how much of each you have
                        crude=[]
                        tot_tickets,tot_money=[0,0]
                        for cur_seller in cur_sellers:
                            amount=0
                            num=0
                            for cur_type in cur_types:
                                factor=cur_type.amount
                                query=ticket.objects.filter(Q(event=cur_show) & Q(ticket_type=cur_type.tike_type) & Q(seller=cur_seller.seller.username))
                                amount=amount+(len(query)*factor)
                                num=num+len(query)
                            crude.append([str(cur_seller.seller.username),amount,num])
                            tot_money,tot_tickets=[tot_money+amount,tot_tickets+num]
                        #print crude,'\n',
                        perc=int(round(((1.0*tot_tickets)/show_tickets)*100))
                        #the type.amount*len(ticket__of_that_type) is the money we earned do this for each seller
                        return render(request,'html/essay/search.html',{'active_1':'active','view':'tools','days':days,'months':months,'years':years,'sellers':sellers,'events':events,'reports':crude,'tot_money':tot_money,'tot_tickets':tot_tickets,'perc':perc,'show_tickets':show_tickets,"err_disp":'none'})
                    except Exception as e:
                        print e
                        return render(request,'html/essay/search.html',{'active_0':'active','view':'tools','days':days,'months':months,'years':years,'sellers':sellers,'events':events,"err_disp":'',})
        else:
            return render(request,'html/essay/search.html',{"err_disp":'none','active_0':'active','view':'tools','days':days,'months':months,'years':years,'sellers':sellers,'events':events})
        return render(request,'html/essay/search.html',{"err_disp":'none','active_0':'active','view':'tools','days':days,'months':months,'years':years,'sellers':sellers,'events':events})
