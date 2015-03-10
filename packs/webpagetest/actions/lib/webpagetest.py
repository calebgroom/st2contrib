"""WebPageTest actions."""

import random

import requests


def list_locations(wpt_url, key=None):
    """Return available locations."""
    params = {'f': 'json'}
    if key:
        params['k'] = key
    request = requests.get("%s/getLocations.php" % wpt_url, params=params)
    locations = request.json()['data']
    return sorted(locations.keys())


def request_test(domain, location_id, wpt_url, key=None):
    """Execute a test for the given domain at a specific location.

    Optional key is required for Google's public instance.
    """
    params = {'f': 'json', 'url': domain, 'location': location_id}
    if key:
        params['k'] = key

    request = requests.get("%s/runtest.php" % wpt_url, params=params)
    return request.json()


def get_test_results(test_id, wpt_url, key=None):
    """Retrieve test results.

    Optional key is required for Google's public instance.
    """
    params = {'test': test_id}
    if key:
        params['k'] = key

    request = requests.get("%s/jsonResult.php" % wpt_url, params=params)
    return request.json()


def test_random_location(domain, wpt_url, key=None):
    """Execute a test for the given domain at a random location.

    Optional key is required for Google's public instance.
    """
    locations = list_locations(wpt_url)
    test = request_test(domain, random.choice(locations), wpt_url, key)
    try:
        return test['data']['userUrl']
    except KeyError:
        return "Error: %s" % test

if __name__ == "__main__":
    print "Test results: %s" % (
        test_random_location("http://example.com", "http://webpagetest.org",
                             "your-api-key-here"))
