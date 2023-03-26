import pytest
import rich
import time
from ipinfo import trysites
from ipinfo import sites
import requests

@pytest.fixture(scope="session")
def ip():
    output = trysites.trysites()
    yield output.get("ip")


def test_chars(ip):
    assert ip, "IP not present"
    assert ip.replace('.', '').isalnum(), "invalid chars in IP"


def test_octets(ip):
    octets = ip.split(".")
    print(f"{ip=}, {octets=}")
    assert len(octets) == 4, "wrong number of octets in IP"
    for octet in octets:
        assert int(octet) > -1, f"octet {octet} smaller than 0"
        assert int(octet) < 256, f"octet {octet} greater than 255"


def test_getsites():
    gs = sites.getsites()
    while True:
        try:
            # sleep delay included as primitive form of rate-limiting
            time.sleep(0.5)
            nextfunc = next(gs)
            assert callable(nextfunc), "generator yielded non-callable"
            jdata = next(gs)()
            assert type(jdata) == dict, "func in getsites not returning dict"
        except StopIteration:
            break


# let's find some expected outputs
@pytest.mark.parametrize("ip", [
    ("192.168.0.1"),
    ("0.0.0.0"),
    ("8.8.8.8"),
    ("255.255.255.255"),
    ("127.0.0.1"),
    ("136.15.2.1")
])
def test_ipconv(ip):
    assert sites.ip_to_json(ip) == {"ip": ip}


@pytest.mark.parametrize("param",
                         [("hello"), ({}), ({"ip": "192.168.0.1"})])
def test_returndict(param):
    assert type(sites.return_dict(param)) == dict


@pytest.mark.parametrize("site",
                         [("https://google.com"),
                          ("https://ipinfo.io"), ("https://wttr.in")])
def test_getdata(site):
    assert type(sites.get_data(site)) == requests.models.Response
