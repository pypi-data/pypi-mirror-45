#!/usr/bin/python3
from imgbase64.imgbase64 import *
import argparse

parser = argparse.ArgumentParser(description='transform images into base64')
parser.add_argument('--url', help='specify the url to image', type=str)
parser.add_argument('--file', help='specify the path to image', type=str)

args = parser.parse_args()

if args.url:
    print(url2base64(args.url))
elif args.file:
    print(file2base64(args.file))
