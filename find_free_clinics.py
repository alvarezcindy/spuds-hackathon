from BeautifulSoup import BeautifulSoup
import requests
import googlemaps
import os

FREE_CLINIC_URL = "https://www.freeclinics.com/cit/ca-san_francisco"

API_KEY = os.environ["AIzaSyD_DOgSSqBrqTUFqeqeudDT6XlOtZ8huZQ"]

google_maps_client = googlemaps.Client(key=API_KEY)

def get_soup(url):
    """Request webpage and return an object from Beautiful Soup"""

    clinic_list = requests.get(url)
    soup = BeautifulSoup(clinic_list.text)
    return soup

def get_resource_names(webpage_soup):
    """Get urls for clinics from a free clinic resource page"""

    holding_div = webpage_soup.find('div',
                                    {'class': 'listings'})
    all_clinic_links = holding_div.findAll('a')
    names = [ a['name'] for a in all_clinic_links ]
    return names


def get_resource_addresses(names):
    """Make a call to the Google Places API for each clinic name"""

    info = []
    for name in names:
        try:
            clinic_list = google_maps_client.places(name)
            if clinic_list['status'] == "OK":
                print('OK')
                info.append((name,
                             clinic_list['results'][0]['streetAddress']))
            except ApiError, e:
                print(e)
        return info


def find_nearest_clinic(current_location):
    """Given a current location, find the nearest free clinic"""

    clinic_locations = get_clinics_from_file("clinics.txt")
    addresses = [pair[1] for pair in clinic_locations]
    clinic_list = google_maps_client.distance_matrix(current_location,
                                                     addresses,
                                                     units='imperial')
    distances = []

    for el in resp['rows'][0]['elements']:
        distances.append(el['distance'])
    tups = [(distances[i]['value'], 
             clinic_locations[i][0],
             addresses[i],
             distances[i]['text'])
             for i in range(len(addresses))]
    return min(tups)


def get_clinics_from_file(filename):
    """Make a list of clinic names and addresses given a file"""

    file = open(filename)
    clinics = []
    for line in file:
        line_split = line.split("|")
        clinics.append((line_split[0], line_split[1]))
    return clinics