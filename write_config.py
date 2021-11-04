import os
from utils import *

config = {
    "info":
"""
""",
    "filename": "config.pkl",
    "history filename": "-icfilehistory.pkl",
    "hostnames":[
        (r'ZEEEE', "peg"),
        (r'SANPEE', "uc")
    ],
    "paths":{
        "peg":[
            r'C:\Projects\Ice Canyon',
            r'F:\Ice Canyon (Thumbdrive Version)',
            r'D:\Brownie\My Little Pony\Ice Canyon Backup',
            r'F:\Ice Canyon TEST version'
        ],
        "uc":[
            r'G:\Ice Canyon (Thumbdrive Version)',
            r'I:\Backup\Pony\MLP\Ice Canyon Backup',
            r'P:\MLP\Ice Canyon Backup'
        ]
    },
    "path presets":{
        "peg":[
            ("Default: PEG IC - IC External", 0, 1),
            ("Peg Debug", 0, 3),
            ("PEG IC - PEG IC Backup", 0, 2),
            ("IC External - PEG IC", 1, 0),
        ],
        "uc":[
            ("Default: IC External - UC IC", 0, 1),
            ("UC IC - UC Brownie", 1, 2)
        ]
    },
    "ignored folders":r'^IC-Anchorage Testing|^Videos|^Frostbite',
    "ignored files":r"Thumbs\.db|-icfilehistory\.pkl",
    "stop on errors":True # this needs to be implemented into the error catching code.
}

def writeConfig(data):
    writePickle(config["filename"], data)

def viewConfigs():
    # loaded by the main code at some point
    print(dumpJson(loadPickle(config["filename"])))

def runThis():
    writeConfig(config)

if __name__ == "__main__": 
    writeConfig(config)