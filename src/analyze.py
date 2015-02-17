#!/usr/bin/env python

import pickle
import sys
import argparse
import logging

import models
import time_bucket

logr = logging.getLogger("analyzer")
logr.setLevel(logging.DEBUG)

def analyze(generator, model):
    plotable_data = []
    for line in generator:
        tb = line[0]
        count = line[1]
        hour = int(tb.start_time.hour)
        model.update(count=count,hour=hour)
        plotable_data.append( (tb,count,model.get_mean(),model.get_eta()) )
        logr.debug("{0} {1:>8} {2:>8.2f} {3:.2f}".format(tb,str(count),model.get_mean(),model.get_eta())) 
    return plotable_data

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-a",dest="alpha",type=float,default=0.95)
    parser.add_argument("-m",dest="mode",default="lc")
    parser.add_argument("-i",dest="input_file_name",default="output.pkl")
    args = parser.parse_args()

    model = models.Poisson(alpha=args.alpha,mode=args.mode)
   
    generator = pickle.load(open(args.input_file_name))
    analyze(generator,model)

