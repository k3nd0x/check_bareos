#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: showmatch ts=4 sts=4 sw=4 autoindent smartindent smarttab expandtab

##########################################################################
# check_bareos.py
#
# Author: https://github.com/k3nd0x
# Date 05.07.2022
# 
# Version: 0.1 
# This program is free software; you can redistribute it or modify
#
# Plugin check for icinga2
# Disclaimer: This plugin is under development and s not for production use 



import requests
import sys
import argparse
import json

def jp(data):
    x =  json.dumps(data, indent=4, sort_keys=True)
    print (x)

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", type=str, help="Bareos Backup Host", required=True)
    parser.add_argument("-p", "--port", type=str, help="HTTP Port API", required=False, default="8000")
    parser.add_argument("-u", "--user", type=str, help="API User", required=False, default="admin")
    parser.add_argument("-P", "--password", type=str, help="HTTP User password", required=False, default="admin")

    parser.add_argument("-m", "--mode", type=str, help="pools,jobs", required=False, default="Jobs")
    args = parser.parse_args()

    return args

def get_token(user,pw,host,port):
    
    headers = {
        'accept': 'application/json',
    }
    data = {
        'grant_type': '',
        'username': user,
        'password': pw,
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }
    url = "http://{}:{}/token".format(host,port)
    try:
        response = requests.post(url, headers=headers, data=data)
    except:
        print("[UNKNOWN] Token get failed - try again later")
        sys.exit(3)
    token = response.json()["access_token"]
    return token

def convert_byte(byte):
    import math

    if byte == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(byte, 1024)))
    p = math.pow(1024, i)
    s = round(byte / p, 2)
    return s, size_name[i]
    


def _api_request(method="get", token=None, url=None, data={}):

    def errorhandling(method="get",url=None,headers=None,json={}):
        if method == "get":
            if json:
                try:
                    response = requests.get(url,headers=headers,json=json)
                except:
                    print("[UNKNOWN] API Error - try again later")
                    sys.exit(3)
            else:
                try:
                    response = requests.get(url,headers=headers)
                except:
                    print("[UNKNOWN] API Error - try again later")
                    sys.exit(3)

        return response

    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }

    arg = args()

    host = arg.host
    port = arg.port

    url = 'http://{}:{}/{}'.format(host,port,url)

    response = errorhandling(method=method,url=url,headers=headers, json=data)

    if response.json() != { "detail": "Not Found"}:
        return response
    else:
        print("[UNKNOWN] Value not found - try again later")
        sys.exit(3)


def _get_jobtotals(token):

    url = 'control/jobs'
    data = { "hours": 24 } 
    data = _api_request("get",token,url,data).json()

    job_total = data["totalItems"]

    jobs = []
    code_max = []

    for job in data["jobs"]:

        if job["level"] == "F":
            level = "Full"
        elif job["level"] == "I":
            level = "Incremental"
        elif job["level"] == "D":
            level = "Differencial"
        else:
            level = job["level"]

        if job["jobstatus"] == "E":
            status = "[CRITICAL]"
            code = 2
            
        elif job["jobstatus"] == "W":
            status = "[WARNING]"
            code = 1
        elif job["jobstatus"] == "T":
            status = "[OK]"
            code = 0
        else:
            status = "[OK]"
            code = 0

        job_bytes = job["jobbytes"]

        job_bytes, unit = convert_byte(int(job_bytes))

        job_bytes = str(job_bytes) + unit
        
        jobs.append({"jobid": job["jobid"], "client": job["client"], "level": level, "status": status,
        "code": code, "duration": job["duration"], "countfiles": job["jobfiles"], "jobsize": job_bytes})
        

    jobs = sorted(jobs, key=lambda d: d['jobid'],reverse=True) 
    output = ""
    for i in jobs:
        if i["client"] not in output:
            output += "{} JobID: {}, {} ({}), ExecutionTime: {}, (Usage: {}, Files: {})\n".format(i["status"], i["jobid"], i["client"], i["level"], i["duration"], i["jobsize"], i["countfiles"])
            code_max.append(i["code"])

    max_crit = code_max.count(2)
    max_warn = code_max.count(1)
    max_ok = code_max.count(0)

    max_code = len(code_max)

    if max_crit > 0:
        output_header = "[CRITICAL] {} of {} Jobs failed:".format(max_crit,max_code)
    elif max_warn > 0:
        output_header = "[WARNING] {} of {} Jobs are in warning state:".format(max_warn,max_code)
    else:
        output_header = "[OK] {} of {} Jobs ok:".format(max_ok,max_code)

    print(output_header)
    print(output)

    sys.exit(max(code_max))


def _get_pools(token):
    url = 'control/jobs/totals'
    #data = { "hours": 24 } 
    data = _api_request("get",token,url).json()

    jp(data)




if __name__ == "__main__":
    arg = args()
    token = get_token(arg.user,arg.password,arg.host,arg.port)

    if arg.mode == "jobs":
        _get_jobtotals(token)
    elif arg.mode == "pools":
        _get_pools(token)
    else:
        _get_jobtotals(token)

