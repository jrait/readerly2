from django.db import models

# Create your models here.

########################################################
#webscraper3: gets all event data from all 10 pages of search results, PLUS the geocoded latitude and longitude
# adding geocoding to get lat and long for each address

from bs4 import BeautifulSoup
import requests
import json

class scrapeData(models.Model):
    def createObject():
        eventArr = []

        #function definition to geocode addresses:
        GOOGLE_API_KEY = 'AIzaSyAIHI0Kl4S-dIqSCgN08vXpqRfhYlOc5FA' 

        def extract_lat_long_via_address(address_or_zipcode):
            lat, lng = None, None
            api_key = GOOGLE_API_KEY
            base_url = "https://maps.googleapis.com/maps/api/geocode/json"
            endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
            # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
            r = requests.get(endpoint)
            if r.status_code not in range(200, 299):
                return None, None
            try:
                '''
                This try block incase any of our inputs are invalid. This is done instead
                of actually writing out handlers for all kinds of responses.
                '''
                results = r.json()['results'][0]
                lat = results['geometry']['location']['lat']
                lng = results['geometry']['location']['lng']
            except:
                pass
            return lat, lng

        for i in range (11):
            url = 'https://stores.barnesandnoble.com/events?page={i}&size=10&sort=date%2ctime&view=events2&v=1'
            response = requests.get(url, timeout=5)
            content = BeautifulSoup(response.content, "html.parser")

            

            #gather event titles
            # for event in content.findAll('h5', attrs = {"class" : "lgTitles"}):
            #     print event.text.encode('utf-8')

            #gather all event data
            for event in content.findAll('div', attrs={"class" : "col-sm-8 col-md-5 col-lg-5 col-xs-8"}):
                eventObject = {
                    "title" : event.find('h5', attrs={"class" : "lgTitles"}).text,
                    "genres" : event.find('span', attrs={"class" : "gray"}).text,
                    "datetime" : event.find('span', attrs={"itemprop" : "startDate"}).text,
                    "streetAddress" : event.find("span", attrs={"itemprop" : "streetAddress"}).text,
                    "city" : event.find("span", attrs={"itemprop" : "addressLocality"}).text,
                    "state" : event.find("span", attrs={"itemprop" : "addressRegion"}).text,
                    "postalCode" : event.find("span", attrs={"itemprop" : "postalCode"}).text,
                    "geocode" : extract_lat_long_via_address(event.find("span", attrs={"itemprop" : "postalCode"}).text)
                }
                eventArr.append(eventObject)
            # with open('bn_eventData.json', 'w') as outfile:
            #     json.dump(eventArr, outfile)
        
        return eventArr






        

########################################################
#webscraper2: gathers the event data for all events on all 10 pages of the search results
# Trying to loop through all pages

# from bs4 import BeautifulSoup
# import requests
# import json

# eventArr = []

# for i in range (11):
#     url = 'https://stores.barnesandnoble.com/events?page={i}&size=10&sort=date%2ctime&view=events2&v=1'
#     response = requests.get(url, timeout=5)
#     content = BeautifulSoup(response.content, "html.parser")

    

#     #gather event titles
#     # for event in content.findAll('h5', attrs = {"class" : "lgTitles"}):
#     #     print event.text.encode('utf-8')

#     #gather all event data
#     for event in content.findAll('div', attrs={"class" : "col-sm-8 col-md-5 col-lg-5 col-xs-8"}):
#         eventObject = {
#             "title" : event.find('h5', attrs={"class" : "lgTitles"}).text,
#             "genres" : event.find('span', attrs={"class" : "gray"}).text,
#             "datetime" : event.find('span', attrs={"itemprop" : "startDate"}).text,
#             "streetAddress" : event.find("span", attrs={"itemprop" : "streetAddress"}).text,
#             "city" : event.find("span", attrs={"itemprop" : "addressLocality"}).text,
#             "state" : event.find("span", attrs={"itemprop" : "addressRegion"}).text,
#             "postalCode" : event.find("span", attrs={"itemprop" : "postalCode"}).text,
#         }
#         eventArr.append(eventObject)
#     with open('bn_eventData.json', 'w') as outfile:
#         json.dump(eventArr, outfile)



        

###########################################################
#webscraper1: gathers the event data for one single event on the page
# we can parse the data to find relevant information. The scraping and the parsing will both be handled by separate Python scripts. The first will collect the data. The second will parse through the data we’ve collected.
# we’ll use two libraries: Beautiful Soup, and Requests. The Request library allows us to make requests to urls, and access the data on those HTML pages. Beautiful Soup contains some easy ways for us to identify the tags we discussed earlier, straight from our Python script.
# Here, we’ll set up all of the logic that will actually request the data from the site we want to scrape.

# from bs4 import BeautifulSoup
# import requests
# import json

# url = 'https://stores.barnesandnoble.com/events?page=0&size=10&sort=date%2ctime&view=events2&v=1'
# response = requests.get(url, timeout=5)
# content = BeautifulSoup(response.content, "html.parser")

# eventArr = []

# #gather event titles
# # for event in content.findAll('h5', attrs = {"class" : "lgTitles"}):
# #     print event.text.encode('utf-8')

# #gather all event data
# for event in content.findAll('div', attrs={"class" : "col-sm-8 col-md-5 col-lg-5 col-xs-8"}):
#     eventObject = {
#         "title" : event.find('h5', attrs={"class" : "lgTitles"}).text,
#         "genres" : event.find('span', attrs={"class" : "gray"}).text,
#         "datetime" : event.find('span', attrs={"itemprop" : "startDate"}).text,
#         "streetAddress" : event.find("span", attrs={"itemprop" : "streetAddress"}).text,
#         "city" : event.find("span", attrs={"itemprop" : "addressLocality"}).text,
#         "state" : event.find("span", attrs={"itemprop" : "addressRegion"}).text,
#         "postalCode" : event.find("span", attrs={"itemprop" : "postalCode"}).text,
#     }
#     eventArr.append(eventObject)
# with open('bn_eventData.json', 'w') as outfile:
#     json.dump(eventArr, outfile)

##################################################################################
#GEOCODER
#the following is the code to geocode a single location -example: by zip code 90210, exports the latitude and longitude of the zipcode
# import requests

# GOOGLE_API_KEY = 'AIzaSyAIHI0Kl4S-dIqSCgN08vXpqRfhYlOc5FA' 

# def extract_lat_long_via_address(address_or_zipcode):
#     lat, lng = None, None
#     api_key = GOOGLE_API_KEY
#     base_url = "https://maps.googleapis.com/maps/api/geocode/json"
#     endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
#     # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
#     r = requests.get(endpoint)
#     if r.status_code not in range(200, 299):
#         return None, None
#     try:
#         '''
#         This try block incase any of our inputs are invalid. This is done instead
#         of actually writing out handlers for all kinds of responses.
#         '''
#         results = r.json()['results'][0]
#         lat = results['geometry']['location']['lat']
#         lng = results['geometry']['location']['lng']
#     except:
#         pass
#     return lat, lng

# print(extract_lat_long_via_address(90210))