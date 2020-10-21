from django.shortcuts import render
# from . import bn_eventData.json
from eventsApp.models import *

# Create your views here.
def simpleMap(request):
    #renders a simple google map with one centered pin
    context = {
        "api_key" : "AIzaSyAIHI0Kl4S-dIqSCgN08vXpqRfhYlOc5FA"
    }
    return render(request, "map_test.html", context)

def simpleMap2(request):
    #renders a simple google map with clustered pins. Each pin location is hard-coded
    context = {
        "api_key" : "AIzaSyAIHI0Kl4S-dIqSCgN08vXpqRfhYlOc5FA"
    }
    return render(request, "map_test2.html", context)

def simpleMap3(request):
    #renders a google map with clustered pins. Each pin gathers information from the scraped bn.com data stored in the JSON file

    # Read file 
    f = open('bn_eventData.json')
    json_string = f.read()
    f.close()

    # Convert json string to python object
    import json
    data = json.loads(json_string)
    
    context = {
        "api_key" : "AIzaSyAIHI0Kl4S-dIqSCgN08vXpqRfhYlOc5FA",
        "event_data" : data
    }

    return render(request, "map_test3.html", context)   