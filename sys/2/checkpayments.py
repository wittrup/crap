#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PEP  263 -- Defining Python Source Code Encodings                         https://www.python.org/dev/peps/pep-0263/
# PEP 3120 -- Using UTF-8 as the default source encoding                    https://www.python.org/dev/peps/pep-3120/

"""At least once a day, get all bookings, last 32 hours from now.
If booking not in list, append to list, trigger new booking event.
Check if customer is in list, if not, fetch customer data.
If customer has Bnr, post datetime, amount, Bnr."""

import os
from datetime import timedelta, datetime
from dateutil.tz import tzlocal
import argparse
import requests
import json
import common
from time import strftime as now

m = [l.strip() for l in open("config.txt").readlines()]
apiKey, secretKey, host, hostpost = m[:4]
payload = {"apiKey": apiKey, "secretKey": secretKey}
paketoke = json.loads(m[4]) # payments keys to keep
meidcufi = m[5].lower()     # member id custom field
username = m[6]
token = m[7]


def getpayments(url, startTime, endTime, payload):
    payload.update({"startTime": strftime(startTime), "endTime": strftime(endTime)})
    r = requests.get(url, params=payload)
    if r.status_code != 200:
        print(r, r.text, file=logfile)
        return None
    else:
        response = json.loads(r.text)
        if all(key in response for key in ["info", "data"]):
            if all(key in response["info"] for key in ['totalPages', 'currentPage', 'pageNavigationToken']):
                # locals().update(response["info"])
                # for pageNumber in range(currentPage + 1, totalPages + 1):
                for pageNumber in range(response["info"]["currentPage"] + 1, response["info"]["totalPages"] + 1):
                    payload.update({"pageNavigationToken": response["info"]["pageNavigationToken"],
                                    "pageNumber": pageNumber})
                    r = requests.get(url, params=payload)
                    nextlist = json.loads(r.text)
                    if "data" in nextlist:
                        response["data"] += nextlist["data"]
        return response


def append(record):
    date = record["date"]
    timestamp = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    filekey = datetime.strftime(timestamp, "%Y-%m-%d")
    if filekey not in files or not files[filekey]:
        filename = datetime.strftime(timestamp, "%Y/%m %B/%d.json")
        files[filekey] = common.jsloifex(filename, {})
    customerId = record["customerId"]
    if not date in files[filekey]:
        files[filekey][date] = {}
    if not customerId in files[filekey][date]:
        files[filekey][date][customerId] = {}
    files[filekey][date][customerId].update((key, record[key]) for key in ["amount", "currency"])
    load_customer_id(host, customerId)
    memberId = customers[customerId]
    target = files[filekey][date][customerId]
    if memberId not in memberIds:
        r = requests.get(hostpost % r'members/' + memberId + r'/status', auth=(username, token))
        if r.status_code != 200:
            print("WARNING:", r.status_code, r.text, file=logfile)
        if "statusCode" in r.json():
            memberIds[memberId] = r.json()["statusCode"]
    sevaifno(target, "MID", memberId)
    sevaifno(target, "MSC", memberIds[memberId])
    if memberId in memberIds:
        if memberIds[memberId] == 1 and "TSC" not in target and "TRI" not in target:
            payload = {}
            payload["date"] = date
            payload.update((key, record[key]) for key in ["amount", "currency"])
            payload["memberId"] = memberId
            r = requests.post(hostpost % 'transactions', data=payload, auth=(username, token))
            if r.status_code != 200:
                print("WARNING:", r.status_code, r.text, file=logfile)
            else:
                print(r.text, file=logfile)
                sevaifno(target, "TSC", r.json()["statusCode"])
                sevaifno(target, "TRI", r.json()["data"]["transaction_ref_id"])



def load_customer_id(host, customerId):  #
    if customerId not in customers:
        customer = get_customer_id(host, customerId)
        if customer and "customFields" in customer and type(customer["customFields"]) is list:
            for customField in customer["customFields"]:
                if type(customField) is dict and all(k in customField for k in ["name", "value"]):
                    if customField["name"].lower() == meidcufi:
                        customers[customerId] = customField["value"]


def sevaifno(target, key, value):  # Set value if not exists
    if key not in target:
        target[key] = value

def write():
    for filekey, record in files.items():
        timestamp = datetime.strptime(filekey, "%Y-%m-%d")
        filename = datetime.strftime(timestamp, "%Y/%m %B/%d.json")
        common.jsstfacp(record, filename, odpl=True)


def get_customer_id(host, customerId):
    r = requests.get((host + "/%s") % ("customers", customerId), params=payload)
    return r.json() if r.status_code == 200 else None


def strftime(time):
    """ Return a string representing the date and time as expressed in the RFC 3339 date-time format.
    https://tools.ietf.org/html/rfc3339"""
    text = datetime.strftime(time, "%Y-%m-%dT%H:%M:%S%z")
    return text[:22] + ":" + text[22:]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-O', dest='output_folder', help="Output folder",
                        default=os.path.dirname(os.path.realpath(__file__)))
    parser.add_argument('-d', dest='date', help="Date to check, default today FORMAT: YYYY-MM-DD")
    parser.add_argument('-s', dest='strtime', help="Date to start at, default today minus one day")
    args = parser.parse_args()
    workpath = args.output_folder

    # Get the current date/time with the timezone.
    runTime = datetime.now(tzlocal())
    if args.date:
        argTime = datetime.strptime(args.date, '%Y-%m-%d')
        endTime = runTime.replace(argTime.year, argTime.month, argTime.day, hour=0, minute=0, second=0, microsecond=0)
        endTime += timedelta(days=1)
    else:
        endTime = runTime
    if args.strtime:
        argTime = datetime.strptime(args.strtime, '%Y-%m-%d')
        strTime = runTime.replace(argTime.year, argTime.month, argTime.day, hour=0, minute=0, second=0, microsecond=0)
    else:
        strTime = endTime - timedelta(days=1)

    logfile = open(now("%Y") + ".log", "a", encoding="utf-8")
    print(strftime(runTime), "Script Start - Checking for new payments", file=logfile)
    print(strftime(strTime), "startTime", file=logfile)
    print(strftime(endTime), "endTime", file=logfile)

    files = {}
    customers = common.jsloifex(workpath + r'/customers.json')
    memberIds = common.jsloifex(workpath + r'/memberIds.json')

    payments = getpayments(host % "payments", strTime, endTime, payload)["data"]

    for payment in payments:
        values = {}
        for key, val in paketoke.items():
            if key in payment:
                if type(val) is list:
                    for item in val:
                        values[item] = payment[key][item]
                elif type(val) is str:
                    values[val] = payment[key]
                else:
                    values[key] = payment[key]
                continue
            print("All required keys [" + key + "] not found in data: '", payment, "'", file=logfile)
            break
        if len(values["date"]) != 19:
            values["date"] = values["date"][:19].replace("T", " ")
        append(values)

    common.jsstfacp(customers, workpath + r'/customers.json', indent=2)
    common.jsstfacp(memberIds, workpath + r'/memberIds.json', indent=2)
    write()

    print(strftime(datetime.now(tzlocal())), "Script End", file=logfile)
