import requests
import json


# this is a generator that yields successive functions to get IP data
def get_data(site: str) -> requests.models.Response:
    """a function that takes a URL, and returns a requests.models.Response
    object associated with it, failing if not.
    Returns
    -------
    r
     requests object"""
    r = requests.models.Response()
    try:
        r = requests.get(site)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        exit()
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        exit()
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        exit()
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)
        exit()
    assert isinstance(r, requests.models.Response), "couldn't get IP data"
    return r


def return_dict(arg) -> dict[str, str]:
    """ takes a parameter, returning it immediately if it's a valid dictionary
    returns an empty dictionary if it's not"""
    if type(arg) == dict:
        return arg
    else:
        return {"": ""}


def ip_to_json(ip: str) -> dict[str, str]:
    jsondata = json.loads("{" + "\"ip\": " + "\"" + ip.strip() + "\"" + "}")
    return return_dict(jsondata)


def getsites():
    """A generator that yields successive methods for scraping
    JSON-formatted IP data in decreasing order of feature-richness
    Returns
    -------
    data
        JSON object containing IP data
    """
    def func1() -> dict[str, str]:
        jdata = json.loads(get_data("https://ipinfo.io").text)
        return return_dict(jdata)

    def func2() -> dict[str, str]:
        ip = get_data("https://ifconfig.me").text
        jdata = ip_to_json(ip)
        return return_dict(jdata)

    def func3() -> dict[str, str]:
        ip = get_data("https://ip.me").text
        jdata = ip_to_json(ip)
        return return_dict(jdata)
    yield func1
    yield func2
    yield func3
