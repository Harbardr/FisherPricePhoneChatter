#! /usr/lib/python

# http://www.supinfo.com/articles/single/1587-synthese-vocale-fluide-linux-avec-pico
import os
import subprocess
import re

def say(words, lang='fr-FR'):
    tempfile = "temp.wav"
    devnull = open("/dev/null","w")
    subprocess.call(["pico2wave", '--lang='+lang, "-w", tempfile, words],stderr=devnull)
    subprocess.call(["aplay", tempfile],stderr=devnull)
    os.remove(tempfile)
