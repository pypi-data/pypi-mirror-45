#!/usr/bin/python
import requests
import base64


def url2base64(url):
    return "data:image/jpeg;base64,"+base64.b64encode(requests.get(url).content).decode()


def file2base64(path):
    with open(path, "rb") as file:
        return "data:image/jpeg;base64,"+base64.b64encode(file.read()).decode()
