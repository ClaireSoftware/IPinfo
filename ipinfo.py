#!/usr/bin/env python
# coding: utf-8

import requests
import json
import rich
from time import sleep


def get_data(site):
    """a function that takes a URL, and returns a requests.models.Response
    object associated with it, failing if not."""
    r = ""
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


# this is a generator that yields successive functions to get IP data
def getsites():
    """A generator that yields successive methods for scraping
    JSON-formatted IP data in decreasing order of feature-richness
    Returns
    -------
    data
        JSON object containing IP data
    """
    def func1():
        return json.loads(get_data("https://ipinfo.io").text)

    def func2():
        ip = get_data("https://ifconfig.me").text
        return json.loads("{" + "\"ip\": " + "\"" + ip.strip() + "\"" + "}")

    def func3():
        ip = get_data("ip.me").text
        return json.loads("{" + "\"ip\": " + "\"" + ip.strip() + "\"" + "}")

    yield func1
    yield func2
    yield func3


def main():
    gs = getsites()
    finaldata = False
    while True:
        try:
            # sleep delay included as primitive form of rate-limiting
            sleep(0.5)
            jdata = next(gs)()
            if (jdata.get("ip")):
                finaldata = jdata
                break
        except StopIteration:

            break

    if not finaldata:
        print("None of the IP sites could return even a valid IP.",
              "Perhaps check your network connection?")
    else:
        rich.print(finaldata)


if __name__ == "__main__":
    main()
# remove this, just using it for testing
else:
    main()
