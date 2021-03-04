from django.shortcuts import render, render_to_response
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views import generic
from django.views.generic import FormView
from .forms import CustomUserCreationForm
from .forms import CustomAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from .models import Member
from .models import Category
from .models import Product
from .models import Session
from .models import CustomUser
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
import json as simplejson
import datetime
import pytz
from django.shortcuts import get_object_or_404
from bokeh.plotting import figure, output_file, show 
from bokeh.embed import components
from bokeh.core.properties import value
from bokeh.models import Legend
from django.http import JsonResponse
from itertools import islice
import random


def index(request):
    if request.user.is_authenticated:
        logged_in_user = request.user
        logged_in_user_posts = Product.objects.filter(author=request.user)
        timezones = []
        for tz in pytz.all_timezones:
            timezones.append((str(tz)))

        #Gets time of day message to user
        tz_zone = pytz.timezone(logged_in_user.timezone)
        user_time = datetime.datetime.now(tz_zone).strftime("%H")
        converted = int(user_time)
        msg = ""
        if converted < 11:
            msg = "Good morning, "
        elif converted >= 12:
            msg = "Good afternoon, "
        elif converted >= 18:
            msg = "Good Evening, "

        return render(request, 'home.html', {'timezone_user': logged_in_user.timezone, 'timezones': timezones, 'msg': msg, 'visibility' : logged_in_user.visibility, 'volume' : logged_in_user.volume})
    else:
        return render(request, 'home.html')






# Change timezone for a user
def changeTimezone_profile(request, username):
    if request.method == 'POST' and request.is_ajax(): 
        print("Changed timezones profile")
        timezone_choosen = request.POST['name']
        logged_in_user = request.user
        logged_in_user.timezone = timezone_choosen
        logged_in_user.save()
                 
        return HttpResponse("")
# Change timezone for a user
def changeTimezone(request):
    if request.method == 'POST' and request.is_ajax(): 
        print("Changed timezones")
        timezone_choosen = request.POST['name']
        logged_in_user = request.user
        logged_in_user.timezone = timezone_choosen
        logged_in_user.save()              
        return redirect('/')



# Change if public or private
def change_volume(request):
    if request.method == 'POST' and request.is_ajax(): 
        print("Changed volume")
        volume_val = request.POST['volume_choosen']
        print(volume_val)
        logged_in_user = request.user
        logged_in_user.volume = volume_val
        logged_in_user.save()              
        return redirect('/')
    return redirect('/')



# Change if public or private
def change_visibility(request):
    print("in here")
    if request.method == 'GET' and request.is_ajax(): 
        print("Changed visiblity")
        visibility = request.GET['visibility_choosen']
        print(visibility)
        logged_in_user = request.user
        logged_in_user.visibility = visibility
        logged_in_user.save()              
        return redirect('/')
    return redirect('/')



# Insert a product into DB
def insertProduct(request):
    if not Product.objects.filter(name=request.POST['name'], author=request.user).exists():
        productVar = Product(name=request.POST['name'], author=request.user)
        productVar.save()
        print("Does not exsist, so create")
    else:
        print("Does exist!")
    return redirect('/')



# Insert a category into DB
def insertCategory(request):
    if not Category.objects.filter(name=request.POST['name'], author=request.user).exists():
        categoryVar = Category(name=request.POST['name'], author=request.user)
        categoryVar.save()
    else:
        print("Does exist!")
    return redirect('/')



# Insert a category into DB
def insertStartPageJournal(request, username):
    if request.user.is_authenticated:
        logged_in_user = request.user
        u = get_object_or_404(CustomUser, email = username)
        if logged_in_user.email == u.email:
            u.startPage = request.POST['name']
            u.save()
            return redirect('/')
        else:
            return render(request, 'home.html')    
    else:
        return render(request, 'home.html')
    
    

# Insert a session into DB
def insertSession(request):
    source_date = datetime.datetime.now()
    source_time_zone = pytz.timezone('Europe/Copenhagen')
    source_date_with_timezone = source_time_zone.localize(source_date)
    target_time_zone = pytz.timezone(request.user.timezone)
    target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)

    sessionVar = Session(sessionTime=request.POST['session_time'], categoryTime=request.POST['session_time_category'], productTime=request.POST['session_time_product'], author=request.user, sessionDateTime=target_date_with_timezone)
    sessionVar.save()
    return redirect('/')



def getProducts(request):
    if request.method == 'GET' and request.is_ajax():     
        result_set = []
        if request.user.is_authenticated:
            all_products = []
            selected_user = get_user_model
            all_products = Product.objects.filter(author=request.user)
            for products in all_products:
                result_set.append({'name': products.name})

        return HttpResponse(simplejson.dumps(result_set), content_type='application/json')
        # return JsonResponse(result_set,status = 200)
    else:
        return redirect('/')



def getCategories(request):
    if request.method == 'GET' and request.is_ajax():
        result_set = []
        all_categories = []
        all_baseCategories = []
        all_baseCategories = Category.objects.filter(baseCategory=True)  

        for category in all_baseCategories:
            result_set.append({'name': category.name})
        if request.user.is_authenticated:
            all_categories = Category.objects.filter(author=request.user)
            for category in all_categories:
                result_set.append({'name': category.name})

        return HttpResponse(simplejson.dumps(result_set), content_type='application/json')
    else:
        return redirect('/')



def getTodaysSessions(request):
    if request.method == 'GET' and request.is_ajax():         
        result_set = []
        if request.user.is_authenticated:
            # Gets time from user
            source_date = datetime.datetime.now()
            source_time_zone = pytz.timezone('Europe/Copenhagen')
            source_date_with_timezone = source_time_zone.localize(source_date)
            target_time_zone = pytz.timezone(request.user.timezone)
            target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)


            date_from = target_date_with_timezone.strftime('%Y-%m-%d 00:00')
            date_to = target_date_with_timezone.strftime('%Y-%m-%d 24:59')

            sessions = []
            sessions = Session.objects.filter(sessionDateTime__range=[date_from, date_to])
            sessions = sessions.filter(author=request.user)

            for session_name in sessions:
                result_set.append({'sessiontime': session_name.sessionTime, 'category': session_name.categoryTime, 'product': session_name.productTime})

                 
        return HttpResponse(simplejson.dumps(result_set), content_type='application/json')
    else:
        return redirect('/')



def profile(request, username):
    u = get_object_or_404(CustomUser, email = username)
    permission = 0

    if request.user.is_authenticated:
        if u.email == request.user.email or u.visibility == "public":
            permission = 1
    else:
        if u.visibility == "private":
            return redirect('home')
            print("PRIVATE");
        if u.visibility == "public":
            permission = 1

    if permission == 1:    
        # Gets the sessions in present week
        # Gets time for the user user
        source_date = datetime.datetime.now()
        source_time_zone = pytz.timezone('Europe/Copenhagen')
        source_date_with_timezone = source_time_zone.localize(source_date)
        target_time_zone = pytz.timezone(u.timezone)
        target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)

        # Get current monday and sunday date
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday())
        date_from = last_monday
        last_sunday = today + datetime.timedelta(days=6)
        date_to = last_sunday

        sessions = []
        sessions = Session.objects.filter(author=u)
        sessions = sessions.filter(sessionDateTime__range=[date_from, date_to])

        user_categories = []
        user_categories_week = []
        user_products = []
        i = 0
        totalTime = 0
        #for user_sesson in sessions:
        #    # Get total time
        #    totalTime += user_sesson.sessionTime

            # Arrange for statestic
        #    if user_sesson.categoryTime not in user_categories:
        #        user_categories.append(user_sesson.categoryTime)
        #        i += 1
        
        #    for user_sesson in sessions:
        #        if user_sesson.productTime not in user_products:
        #            user_products.append(user_sesson.productTime)

        user_categories = Category.objects.filter(author=u)
        user_products = Product.objects.filter(author=u)

        u_timezone = u.timezone
        u_email = u.email
        u_startPage = u.startPage
        timezones = []
        for tz in pytz.all_timezones:
            timezones.append((str(tz)))

        # Dynamic gets all the months from user creation
        time_creation = datetime.datetime.strftime(u.created_at, '%Y-%m-%d') 
        year_creation, month_creation, day_creation = (int(x) for x in time_creation.split('-'))  
        time_current = datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')
        year_current, month_current, day_current = (int(x) for x in time_current.split('-'))  
        months = []
        
        if year_creation == 2019:
            if month_current == 8:  #Current month is August
                if month_creation == 8:
                    months = ["August"]
            if month_current == 9:
                if month_creation == 8:
                    months = ["August", "September"]
                if month_creation == 9:
                    months = ["September"]
            if month_current == 10:
                if month_creation == 8:
                    months = ["August", "September", "October"]
                if month_creation == 9:
                    months = ["September", "October"]
                if month_creation == 10:
                    months = ["October"]
            if month_current == 11:
                if month_creation == 8:
                    months = ["August", "September", "October", "November"]
                if month_creation == 9:
                    months = ["September", "October", "November"]
                if month_creation == 10:
                    months = ["October", "November"]
                if month_creation == 11:
                    months = ["November"]
            if month_current == 12:
                if month_creation == 8:
                    months = ["August", "September", "October", "November", "December"]
                if month_creation == 9:
                    months = ["September", "October", "November", "December"]
                if month_creation == 10:
                    months = ["October", "November", "December"]
                if month_creation == 11:
                    months = ["November", "December"]
                if month_creation == 12:
                    months = ["December"]

        # Gets totaltime in hours decimal
        totalTime = round((totalTime / 3600), 2)

        return render(request,'profile.html', {'timezone_user': u_timezone,'timezones': timezones,'u_email': u_email,  'months': months, 'user_categories' : user_categories, 'user_products' : user_products, 'u_startPage' : u_startPage, 'totalTime' : totalTime, 'visibility' : u.visibility})
    else:
        return redirect('home')


def get_statestic(request, username):
    if request.method == 'GET' and request.is_ajax(): 
        categories_from_site = request.GET.getlist('user_category[]')
        products_from_site = request.GET.getlist('user_product[]')
        u = get_object_or_404(CustomUser, email = username)



        # Gets the sessions in present week
        # Gets time for the user user
        source_date = datetime.datetime.now()
        source_time_zone = pytz.timezone('Europe/Copenhagen')
        source_date_with_timezone = source_time_zone.localize(source_date)
        target_time_zone = pytz.timezone(u.timezone)
        target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)

        # Get current monday and sunday date
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday())
        date_from = last_monday
        last_sunday = today + datetime.timedelta(days=6)
        date_to = last_sunday

        sessions = []
        sessions = Session.objects.filter(author=u)
        sessions = sessions.filter(sessionDateTime__range=[date_from, date_to])

        user_categories = []
        user_categories_week = []
        user_products = []
        colors = []
        i = 0
        r = lambda: random.randint(0,255)

        # Get total time
        totalTime = 0

        for category in categories_from_site:
            user_categories.append(category)
            colors.append('#%02X%02X%02X' % (r(),r(),r()))
            i += 1

        for product in products_from_site:
            user_products.append(product)


        # Sorting timesessions into user's categories
        for category in user_categories:
            mon = 0
            tue = 0
            ons = 0
            thur = 0
            fre = 0
            sat = 0
            sun = 0

            #Find the sessions with the category
            for user_sesson in sessions:
                if user_sesson.categoryTime == category and user_sesson.productTime in products_from_site:
                    #Find which day of the week it is
                    time = datetime.datetime.strftime(datetime.datetime.strptime(user_sesson.sessionDateTime, '%Y-%m-%d %H:%M:%S.%f%z').date(), '%Y-%m-%d')
                    year, month, day = (int(x) for x in time.split('-'))  
                    ans = (datetime.date(year, month, day)).weekday()
                    # Get total time
                    totalTime += user_sesson.sessionTime

                    if ans == 0:
                        mon += (user_sesson.sessionTime / 3600)
                    elif ans == 1:
                        tue += (user_sesson.sessionTime / 3600)
                    elif ans == 2:
                        ons += (user_sesson.sessionTime / 3600)
                    elif ans == 3:
                        thur += (user_sesson.sessionTime / 3600)
                    elif ans == 4:
                        fre += (user_sesson.sessionTime / 3600)
                    elif ans == 5:
                        sat += (user_sesson.sessionTime / 3600)
                    elif ans == 6:
                        sun += (user_sesson.sessionTime / 3600)
                    else:
                        return
            # Assign to category
            user_categories_week.append([mon,tue,ons,thur,fre,sat,sun])
            #user_categories_week.append({category  : [mon,tue,ons,thur,fre,sat,sun] })


        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        
        data = {'weekdays' : weekdays}

        y = 0
        for weekSession in user_categories:
            data[user_categories[y]] = user_categories_week[y]
            y += 1


        p = figure(x_range=weekdays, sizing_mode='stretch_both', title="Hours",
                toolbar_location=None, tools="hover", tooltips="$name @weekdays: @$name")

        v = p.vbar_stack(user_categories, x='weekdays', width=1, color=colors, source=data)

        if i >= 16:
            print("16-20")
            legend1 = Legend(items=[(x, [v[i]]) for i, x in enumerate(islice(user_categories,5))], location="bottom_left")
            p.add_layout(legend1, 'below')
            legend2 = Legend(items=[(x, [v[i+5]]) for i, x in enumerate(islice(user_categories,5,10))], location="bottom_left")
            p.add_layout(legend2, 'below')
            legend3 = Legend(items=[(x, [v[i+10]]) for i, x in enumerate(islice(user_categories,10,15))], location="bottom_left")
            p.add_layout(legend3, 'below')
            legend4 = Legend(items=[(x, [v[i+15]]) for i, x in enumerate(islice(user_categories,15,20))], location="bottom_left")
            p.add_layout(legend4, 'below')
        elif i >= 11:
            print("11-15")
            legend1 = Legend(items=[(x, [v[i]]) for i, x in enumerate(islice(user_categories,5))], location="bottom_left")
            p.add_layout(legend1, 'below')
            legend2 = Legend(items=[(x, [v[i+5]]) for i, x in enumerate(islice(user_categories,5,10))], location="bottom_left")
            p.add_layout(legend2, 'below')
            legend3 = Legend(items=[(x, [v[i+10]]) for i, x in enumerate(islice(user_categories,10,15))], location="bottom_left")
            p.add_layout(legend3, 'below')
        elif i >= 6:
            print("6-10")
            legend1 = Legend(items=[(x, [v[i]]) for i, x in enumerate(islice(user_categories,5))], location="bottom_left")
            p.add_layout(legend1, 'below')
            legend2 = Legend(items=[(x, [v[i+5]]) for i, x in enumerate(islice(user_categories,5,10))], location="bottom_left")
            p.add_layout(legend2, 'below')
        elif i <= 5:
            print("Less than or 5")
            legend = Legend(items=[(x, [v[i]]) for i, x in enumerate(islice(user_categories,5))], location="bottom_left")
            p.add_layout(legend, 'below')


        p.legend.orientation = "horizontal"
        p.legend.spacing = 10

        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.axis.minor_tick_line_color = None
        p.outline_line_color = None



        #Store components 
        script, div = components(p)

        # Gets totaltime in hours decimal
        totalTime = round((totalTime / 3600), 2)
         
        return render_to_response('graph.html', {"script": script, "div": div, "totalTime" : totalTime})
    else:
        return HttpResponse("Request method is not a GET")



def get_statestic_year(request, username):
    if request.method == 'GET' and request.is_ajax(): 
        categories_from_site = request.GET.getlist('user_category[]')
        products_from_site = request.GET.getlist('user_product[]')
        u = get_object_or_404(CustomUser, email = username)


        # Gets the sessions in present week
        # Gets time for the user user
        source_date = datetime.datetime.now()
        source_time_zone = pytz.timezone('Europe/Copenhagen')
        source_date_with_timezone = source_time_zone.localize(source_date)
        target_time_zone = pytz.timezone(u.timezone)
        target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)

        date_from = target_date_with_timezone.strftime('2019-01-01 00:01')
        date_to = target_date_with_timezone.strftime('2019-12-31 24:59')

        sessions = []
        sessions = Session.objects.filter(author=u)
        sessions = sessions.filter(sessionDateTime__range=[date_from, date_to])

        totalTime = 0

        user_categories = []
        user_categories_week = []
        user_products = []
        colors = []
        r = lambda: random.randint(0,255)
        i = 0

        for category in categories_from_site:
            user_categories.append(category)
            colors.append('#%02X%02X%02X' % (r(),r(),r()))
            i += 1

        for product in products_from_site:
            user_products.append(product)





        # Sorting timesessions into user's categories
        for category in user_categories:
            jan = 0
            feb = 0
            marts = 0
            april = 0
            maj = 0
            juni = 0
            juli = 0
            august = 0
            september = 0
            oktober = 0
            november = 0
            december = 0

            #Find the sessions with the category
            for user_sesson in sessions:
                if user_sesson.categoryTime == category and user_sesson.productTime in products_from_site:
                    #Find which day of the week it is
                    time = datetime.datetime.strftime(datetime.datetime.strptime(user_sesson.sessionDateTime, '%Y-%m-%d %H:%M:%S.%f%z').date(), '%Y-%m-%d')
                    year, month, day = (int(x) for x in time.split('-'))  

                    # Get total time
                    totalTime += user_sesson.sessionTime

                    if month == 1 and year == 2019:
                        jan += (user_sesson.sessionTime / 3600)
                    elif month == 2 and year == 2019:
                        feb += (user_sesson.sessionTime / 3600)
                    elif month == 3 and year == 2019:
                        marts += (user_sesson.sessionTime / 3600)
                    elif month == 4 and year == 2019:
                        april += (user_sesson.sessionTime / 3600)
                    elif month == 5 and year == 2019:
                        maj += (user_sesson.sessionTime / 3600)
                    elif month == 6 and year == 2019:
                        juni += (user_sesson.sessionTime / 3600)
                    elif month == 7 and year == 2019:
                        juli += (user_sesson.sessionTime / 3600)
                    elif month == 8 and year == 2019:
                        august += (user_sesson.sessionTime / 3600)
                    elif month == 9 and year == 2019:
                        september += (user_sesson.sessionTime / 3600)
                    elif month == 10 and year == 2019:
                        oktober += (user_sesson.sessionTime / 3600)
                    elif month == 11 and year == 2019:
                        november += (user_sesson.sessionTime / 3600)
                    elif month == 12 and year == 2019:
                        december += (user_sesson.sessionTime / 3600)
                    else:
                        return
            # Assign to category
            user_categories_week.append([jan,feb,marts,april,maj,juni,juli,august,september,oktober,november,december])
            #user_categories_week.append({category  : [mon,tue,ons,thur,fre,sat,sun] })


        weekdays = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        data = {'weekdays' : weekdays}

        y = 0
        for weekSession in user_categories:
            data[user_categories[y]] = user_categories_week[y]
            y += 1



        p = figure(x_range=weekdays, sizing_mode='stretch_both', title="Hours",
                toolbar_location=None, tools="hover", tooltips="$name @weekdays: @$name")

        v = p.vbar_stack(user_categories, x='weekdays', width=1, color=colors, source=data)

        if i >= 16:
            print("16-20")
            legend1 = Legend(items=[(x, [v[i]]) for i, x in enumerate(islice(user_categories,5))], location="bottom_left")
            p.add_layout(legend1, 'below')
            legend2 = Legend(items=[(x, [v[i+5]]) for i, x in enumerate(islice(user_categories,5,10))], location="bottom_left")
            p.add_layout(legend2, 'below')
            legend3 = Legend(items=[(x, [v[i+10]]) for i, x in enumerate(islice(user_categories,10,15))], location="bottom_left")
            p.add_layout(legend3, 'below')
            legend4 = Legend(items=[(x, [v[i+15]]) for i, x in enumerate(islice(user_categories,15,20))], location="bottom_left")
            p.add_layout(legend4, 'below')
        elif i >= 11:
            print("11-15")
            legend1 = Legend(items=[(x, [v[i]]) for i, x in enumerate(islice(user_categories,5))], location="bottom_left")
            p.add_layout(legend1, 'below')
            legend2 = Legend(items=[(x, [v[i+5]]) for i, x in enumerate(islice(user_categories,5,10))], location="bottom_left")
            p.add_layout(legend2, 'below')
            legend3 = Legend(items=[(x, [v[i+10]]) for i, x in enumerate(islice(user_categories,10,15))], location="bottom_left")
            p.add_layout(legend3, 'below')
        elif i >= 6:
            print("6-10")
            legend1 = Legend(items=[(x, [v[i]]) for i, x in enumerate(islice(user_categories,5))], location="bottom_left")
            p.add_layout(legend1, 'below')
            legend2 = Legend(items=[(x, [v[i+5]]) for i, x in enumerate(islice(user_categories,5,10))], location="bottom_left")
            p.add_layout(legend2, 'below')
        elif i <= 5:
            print("Less than or 5")
            legend = Legend(items=[(x, [v[i]]) for i, x in enumerate(islice(user_categories,5))], location="bottom_left")
            p.add_layout(legend, 'below')


        p.legend.orientation = "horizontal"
        p.legend.spacing = 10
        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.axis.minor_tick_line_color = None
        p.outline_line_color = None

        #Store components 
        script, div = components(p)

        # Gets totaltime in hours decimal
        totalTime = round((totalTime / 3600), 2)
           
        return render_to_response('graph.html', {"script": script, "div": div, "totalTime" : totalTime})
    else:
        return HttpResponse("Request method is not a GET")



        # Find which month the user has been active



def get_statestic_month(request, username):
    if request.method == 'GET' and request.is_ajax(): 
        categories_from_site = request.GET.getlist('user_category[]')
        products_from_site = request.GET.getlist('user_product[]')
        u = get_object_or_404(CustomUser, email = username)
        choosen_month = request.GET.get('month')


        # Gets the sessions in present week
        # Gets time for the user user
        source_date = datetime.datetime.now()
        source_time_zone = pytz.timezone('Europe/Copenhagen')
        source_date_with_timezone = source_time_zone.localize(source_date)
        target_time_zone = pytz.timezone(u.timezone)
        target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
        sessions = []
        sessions = Session.objects.filter(author=u)

        if(choosen_month == "August"):
            date_from = target_date_with_timezone.strftime('2019-08-01 00:01')
            date_to = target_date_with_timezone.strftime('2019-08-31 24:59')
            sessions = sessions.filter(sessionDateTime__range=[date_from, date_to])
            days_in_month = 31

        if(choosen_month == "September"):
            date_from = target_date_with_timezone.strftime('2019-09-01 00:01')
            date_to = target_date_with_timezone.strftime('2019-09-30 24:59')
            sessions = sessions.filter(sessionDateTime__range=[date_from, date_to])
            days_in_month = 30

        if(choosen_month == "October"):
            date_from = target_date_with_timezone.strftime('2019-10-01 00:01')
            date_to = target_date_with_timezone.strftime('2019-10-31 24:59')
            sessions = sessions.filter(sessionDateTime__range=[date_from, date_to])
            days_in_month = 31

        if(choosen_month == "November"):
            date_from = target_date_with_timezone.strftime('2019-11-01 00:01')
            date_to = target_date_with_timezone.strftime('2019-11-30 24:59')
            sessions = sessions.filter(sessionDateTime__range=[date_from, date_to])
            days_in_month = 30

        if(choosen_month == "December"):
            date_from = target_date_with_timezone.strftime('2019-12-01 00:01')
            date_to = target_date_with_timezone.strftime('2019-12-31 24:59')
            sessions = sessions.filter(sessionDateTime__range=[date_from, date_to])
            days_in_month = 31


        # Get the sessions of the choosen month
        user_categories = []
        user_categories_week = []
        user_products = []
        colors = []
        dates_show = []
        dates = []
        r = lambda: random.randint(0,255)
        i = 0

        totalTime = 0

        for category in categories_from_site:
            user_categories.append(category)
            colors.append('#%02X%02X%02X' % (r(),r(),r()))
            i += 1

        for product in products_from_site:
            user_products.append(product)


        for y in range(1, days_in_month + 1):
            dates.append(str(y))
            #dates.append(str(y) + "/" + "08")


        # Sorting timesessions into user's categories
        for category in user_categories:
            
            month_days = []
      
            for y in range(1, days_in_month + 1):
                month_days.append(0)

            #Find the sessions with the category
            for user_sesson in sessions:
                if user_sesson.categoryTime == category and user_sesson.productTime in products_from_site:
                    #Find which day of the week it is
                    time = datetime.datetime.strftime(datetime.datetime.strptime(user_sesson.sessionDateTime, '%Y-%m-%d %H:%M:%S.%f%z').date(), '%Y-%m-%d')
                    year, month, day = (int(x) for x in time.split('-'))
                    month_days[day - 1] = (user_sesson.sessionTime / 3600)
                    # Get total time
                    totalTime += user_sesson.sessionTime
            # Assign to category
            user_categories_week.append(month_days)



        weekdays = dates
        
        data = {'weekdays' : weekdays}

        y = 0
        for weekSession in user_categories:
            data[user_categories[y]] = user_categories_week[y]
            y += 1


        p = figure(x_range=weekdays, sizing_mode='stretch_both', title="Hours",
                toolbar_location=None, tools="hover", tooltips="$name @weekdays: @$name")

        v = p.vbar_stack(user_categories, x='weekdays', width=1, color=colors, source=data)

        if i >= 16:
            print("16-20")
            legend1 = Legend(items=[(x, [v[i]]) for i, x in enumerate(islice(user_categories,5))], location="bottom_left")
            p.add_layout(legend1, 'below')
            legend2 = Legend(items=[(x, [v[i+5]]) for i, x in enumerate(islice(user_categories,5,10))], location="bottom_left")
            p.add_layout(legend2, 'below')
            legend3 = Legend(items=[(x, [v[i+10]]) for i, x in enumerate(islice(user_categories,10,15))], location="bottom_left")
            p.add_layout(legend3, 'below')
            legend4 = Legend(items=[(x, [v[i+15]]) for i, x in enumerate(islice(user_categories,15,20))], location="bottom_left")
            p.add_layout(legend4, 'below')
        elif i >= 11:
            print("11-15")
            legend1 = Legend(items=[(x, [v[i]]) for i, x in enumerate(islice(user_categories,5))], location="bottom_left")
            p.add_layout(legend1, 'below')
            legend2 = Legend(items=[(x, [v[i+5]]) for i, x in enumerate(islice(user_categories,5,10))], location="bottom_left")
            p.add_layout(legend2, 'below')
            legend3 = Legend(items=[(x, [v[i+10]]) for i, x in enumerate(islice(user_categories,10,15))], location="bottom_left")
            p.add_layout(legend3, 'below')
        elif i >= 6:
            print("6-10")
            legend1 = Legend(items=[(x, [v[i]]) for i, x in enumerate(islice(user_categories,5))], location="bottom_left")
            p.add_layout(legend1, 'below')
            legend2 = Legend(items=[(x, [v[i+5]]) for i, x in enumerate(islice(user_categories,5,10))], location="bottom_left")
            p.add_layout(legend2, 'below')
        elif i <= 5:
            print("Less than or 5")
            legend = Legend(items=[(x, [v[i]]) for i, x in enumerate(islice(user_categories,5))], location="bottom_left")
            p.add_layout(legend, 'below')


        p.legend.orientation = "horizontal"
        p.legend.spacing = 10

        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.axis.minor_tick_line_color = None
        p.outline_line_color = None

        #Store components 
        script, div = components(p)

        # Gets totaltime in hours decimal
        totalTime = round((totalTime / 3600), 2)
         
        return render_to_response('graph.html', {"script": script, "div": div, "totalTime" : totalTime})
    else:
        return HttpResponse("Request method is not a GET")



