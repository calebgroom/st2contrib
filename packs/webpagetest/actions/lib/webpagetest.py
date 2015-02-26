import requests
import random


def list_locations(wpt_url):
    '''
    Takes a base URL and appends the locations path.
    Returns a list of location ids.
   '''
    locations_path = "/getLocations.php?f=json"
    r = requests.get(wpt_url + locations_path)
    locations = r.json()['data']

    result = []
    for location, values in sorted(locations.items()):
        result.append(location)

    return result


def request_test(domain, location_id, wpt_url):
    '''
    Uses a domain and location id to request a test.
    Returns a dictionary with the response.
    '''

    test_params = "/runtest.php?f=json&url={0}&location={1}".format(domain, location_id)
    r = requests.get(wpt_url + test_params)
    return r.json()


def get_test_results(test_id, wpt_url):
    '''
    Returns a dictionary with the test results.
    '''
    test_results = "/jsonResult.php?test={0}".format(test_id)
    r = requests.get(wpt_url + test_results)
    return r.json()


def test_random_location(domain, wpt_url):
    '''
    Tests a domain at a random location.
    '''
    locations = list_locations(wpt_url)
    test = request_test(domain, random.choice(locations), wpt_url)
    return test['data']['userUrl']


if __name__ == "__main__":

    wpt_url = "http://webpagetest.rax.io"
    wpt_key = None

    #locations = list_locations(wpt_url)
    #test = request_test("www.onitato.com", random.choice(locations), wpt_url)
    #test_results = get_test_results(test['data']['testId'], wpt_url)
    #print("Your test can be found here: {0}".format(test['data']['userUrl']))

    print(test_random_location("www.onitato.com", wpt_url))
