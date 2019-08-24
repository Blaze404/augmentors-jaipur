from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse
from . import shortcuts
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import InformationHousehold
from . import utilities
from . import simulation as sim
import random
from . import constants as C

# Create your views here.

def index(request):
    if request.method == 'POST':
        # success = shortcuts.index(request)
        username = request.POST.get('uname')
        if username[:3] == 'uts':
            request.session['utility_service'] = username
            return render(request, 'webap/iframe.html', {'contact': True})
        request.session['identifier'] = request.POST.get('uname')
        success, context = shortcuts.get_user_statistics(username)
        if success:
            return render(request, 'webap/dashboard.html', context)
        return render(request, 'webap/dashboard.html', {})
        # else:
        #     return render(request, 'webapp/index.html', {'contact_error': True})

    if request.method == 'GET':
        a =  render(request, 'webap/index.html', {})
        # print('redndered')
        return a
    else:
        return HttpResponseNotFound("Request Type not supported")


def index_sim(request):
    if request.method == 'POST' or request.method == 'GET':
        # success = shortcuts.index(request)
        username = "MAC23372337"
        if username[:3] == 'uts':
            request.session['utility_service'] = username
            return render(request, 'webap/iframe.html', {'contact': True})
        request.session['identifier'] = "MAC23372337"
        success, context = shortcuts.get_user_statistics(username)
        shortcuts.automatic_simulation()
        limit = 40
        if context['this_day'] >= limit:
            context['limit'] = True
        context['daily_limit'] = limit
        if success:
            return render(request, 'webap/dashboard_sim.html', context)
        return render(request, 'webap/dashboard_sim.html', {})
        # else:
        #     return render(request, 'webapp/index.html', {'contact_error': True})


    else:
        return HttpResponseNotFound("Request Type not supported")



def index_last_hope(request):
    if request.method == 'POST' or request.method == 'GET':
        # success = shortcuts.index(request)
        usernames = ["MAC23372330", "MAC23372331", "MAC23372332", "MAC23372333"]

        contexes = {}
        success = False
        for i in range(4):
            success1, context = shortcuts.get_user_statistics(usernames[i])
            success = success1
            for key in context.keys():
                house = 'h' + str(i)
                contexes[house + key] = context[key]
        shortcuts.update_all_houses()
        sum_of_all = sum(sim.houses)
        avg_of_all = sum_of_all / 4
        contexes['price'] = utilities.price(0, random.randint(25, 45), sum_of_all, avg_of_all/200, sim.houses[1])
        limit = 40
        # if context['this_day'] >= limit:
        #     context['limit'] = True
        # context['daily_limit'] = limit
        if success:
            return render(request, 'webap/chaar_ghar.html', contexes)
        return render(request, 'webap/chaar_ghar.html', {})
        # else:
        #     return render(request, 'webapp/index.html', {'contact_error': True})


    else:
        return HttpResponseNotFound("Request Type not supported")


def login(request):
    pass

def stats(request):
    pass

def organization(request):
    pass

def org_stats(request):
    pass

def house_information(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        shortcuts.populate_house_information(uploaded_file_url)
        return render(request, 'webap/house_information.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'webap/house_information.html')

def recommend(request):
    if request.method == 'POST':
        heavy = request.POST.get('heavy')
        fans = request.POST.get('fans')
        lights = request.POST.get('lights')
        bulbs = request.POST.get('bulbs')

        plan = shortcuts.recommend(heavy, fans, lights, bulbs)
        print('#################' + plan)
        d = C.plans[plan]
        print(d)
        context = {
            'plan': d['plan'],
            'offer': d['offer']
        }
        return render(request, 'webap/recc.html', context)

def do_stuff(request):
    if request.method == 'GET':
        ih = InformationHousehold()
        ih.LCLid = 'MAC23372334'
        ih.stdorToU = 'sample'
        ih.Acorn = 'sample'
        ih.Acorn_grouped = 'sample'
        ih.file = 'block_n'
        ih.save()
        return HttpResponse('success')

def simulation(request):
    if request.method == 'POST':
        shortcuts.last_hope(request)
        print('its here')
        return HttpResponse('hello')
    else:
        return render(request, 'webap/smart_home.html', {})


def sample(request):
    if request.method == 'POST':
        print('its here')
        data = request.POST.get('sample')
        return HttpResponse(data)
    else:
        return render(request, 'webap/sample.html', {})