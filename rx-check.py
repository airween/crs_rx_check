#!/usr/bin/env python3

import sys
import os
import glob
import msc_pyparser
import argparse
import re2

oformat = "native"

class Check(object):
    def __init__(self, data):
        self.data = data

    def store_error(self, msg):
        # store the error msg in the list
        self.caseerror.append({
                                'ruleid' : 0,
                                'line'   : self.curr_lineno,
                                'endLine': self.curr_lineno,
                                'message': msg
                            })

def errmsg(msg):
    if oformat == "github":
        print("::error %s" % (msg))
    else:
        print(msg)

def errmsgf(msg):
    if oformat == "github":
        print("::error%sfile={file},line={line},endLine={endLine},title={title}".format(**msg) % (msg['indent']*" "))
    else:
        print("%sfile={file}, line={line}, endLine={endLine}, title={title}".format(**msg) % (msg['indent']*" "))

def msg(msg):
    if oformat == "github":
        print("::debug %s" % (msg))
    else:
        print(msg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CRS Rules Check tool")
    parser.add_argument("-o", "--output", dest="output", help="Output format native[default]|github", required=False)
    parser.add_argument("-r", "--rules", metavar='/path/to/coreruleset/*.conf', type=str,
                            nargs='*', help='Directory path to CRS rules', required=True,
                            action="append")
    args = parser.parse_args()

    crspath = []
    for l in args.rules:
        crspath += l

    if args.output is not None:
        if args.output not in ["native", "github"]:
            print("--output can be one of the 'native' or 'github'. Default value is 'native'")
            sys.exit(1)
    oformat = args.output

    retval = 0
    try:
        flist = crspath
        flist.sort()
    except:
        errmsg("Can't open files in given path!")
        sys.exit(1)

    if len(flist) == 0:
        errmsg("List of files is empty!")
        sys.exit(1)

    # process files in the list
    for f in flist:
        try:
            with open(f, 'r') as inputfile:
                data = inputfile.read()
        except:
            errmsg("Can't open file: %s" % f)
            sys.exit(1)

        ### check file syntax
        msg("Config file: %s" % (f))
        try:
            mparser = msc_pyparser.MSCParser()
            mparser.parser.parse(data)
            msg(" Parsing ok.")
        except Exception as e:
            err = e.args[1]
            if err['cause'] == "lexer":
                cause = "Lexer"
            else:
                cause = "Parser"
            errmsg("Can't parse config file: %s" % (f))
            errmsgf({
                'indent' : 2,
                'file'   : f,
                'title'  : "%s error" % (cause),
                'line'   : err['line'],
                'endLine': err['line'],
                'message': "can't parse file"})
            retval = 1
            continue

        # iterate over the parsed structure
        for s in mparser.configlines:
            if s['type'].lower() == "secrule":
                if s['operator'] == '@rx':
                    try:
                        r = re2.compile(s['operator_argument'])
                    except:
                        errmsgf({
                            'file'   : f,
                            'line'   : s['oplineno'],
                            'endLine': s['oplineno'],
                            'title'  : "RX operand is not re2 compatible",
                            'indent' : 2,
                        })
                        retval = 1

    sys.exit(retval)
