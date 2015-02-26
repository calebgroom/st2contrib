import requests
import random


def list_locations(wpt_url, key=None):
    '''
    Takes a base URL and appends the locations path.
    Returns a list of location ids.
    '''
    if key:
        locations_path = "/getLocations.php?f=json&k={0}".format(key)
    else:
        locations_path = "/getLocations.php?f=json"
    r = requests.get(wpt_url + locations_path)
    locations = r.json()['data']

    result = []
    for location, values in sorted(locations.items()):
        result.append(location)

    return result


def request_test(domain, location_id, wpt_url, key=None):
    '''
    Uses a domain and location id to request a test.
    Returns a dictionary with the response.
    '''
    if key:
        test_params = "/runtest.php?f=json&url={0}&location={1}&k={2}".format(domain, location_id, key)
    else:
        test_params = "/runtest.php?f=json&url={0}&location={1}".format(domain, location_id)
    test_uri = wpt_url + test_params
    r = requests.get(wpt_url + test_params)
    return r.json()


def get_test_results(test_id, wpt_url, key=None):
    '''
    Returns a dictionary with the test results.
    '''
    if key:
        test_results = "/jsonResult.php?test={0}&k={1}".format(test_id, key)
    else:
        test_results = "/jsonResult.php?test={0}".format(test_id)
    r = requests.get(wpt_url + test_results)
    return r.json()


def test_random_location(domain, wpt_url, key=None):
    '''
    Tests a domain at a random location.
    '''
    locations = list_locations(wpt_url)
    test = request_test(domain, random.choice(locations), wpt_url, key)
    try:
        ret = test['data']['userUrl']
    except KeyError as exc:
        ret = ("Error: {0}".format(test))
    return ret


if __name__ == "__main__":

    wpt_url = "http://webpagetest.org"
    wpt_key = None

    test_url = test_random_location("www.onitato.com", wpt_url, wpt_key)
    print("Your test results are here:\n{0}".format(test_url))
