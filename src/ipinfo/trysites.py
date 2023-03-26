#!/usr/bin/env python
# coding: utf-8

from time import sleep
from ipinfo import sites


def trysites() -> dict[str, str]:
    gs = sites.getsites()
    while True:
        try:
            # sleep delay included as primitive form of rate-limiting
            sleep(0.5)
            jdata = next(gs)()
            if (jdata.get("ip")):
                if type(jdata) == dict:
                    return jdata
                else:
                    return {"": ""}
        except StopIteration:
            break
    return {"": ""}
