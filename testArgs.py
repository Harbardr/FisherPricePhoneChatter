#! /usr/lib/python

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--rotary", action="store_true", help="Use the encoder")
parser.add_argument("-k", "--keyboard", action="store_true", help="Use the keyboard")
parser.add_argument("-fr", "--french", action="store_true", help="French language")
parser.add_argument("-en", "--english", action="store_true", help="English language")
args = parser.parse_args()

print args
