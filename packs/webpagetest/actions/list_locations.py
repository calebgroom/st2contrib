import requests



def print_locations(url):
    '''
    Takes a base URL and appends the locations path.
    Prints the locations.
    '''
    locations_path = "/getLocations.php?f=json"
    r = requests.get(wpt_url + locations_path)
    locations = r.json()['data']

    print("Region - Browser - ID")
    for location, values in sorted(locations.items()):
        print("\t{0} / {1} / {2}".format(values['Label'], values['Browser'], location))

if __name__ == "__main__":
    wpt_url = "http://webpagetest.rax.io"
    wpt_key = None
    print_locations(wpt_url)
