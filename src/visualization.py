import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import re
import fileManipulation as fM

def titleMetadata(filename):
    wh = filename.split('_')[0]
    Date = filename.split('_')[1]
    year = Date.split('-')[0]
    MthType = Date.split('-')[1]
    month = MthType[0:2]
    inc = MthType[2:3]
    
    return wh, year, month, inc

def CummulativeWWFGraphs(targetFolder, granularity = 'H'):
    filesL = os.listdir(targetFolder)
    for filename in filesL:
        wh, year, month, inc = titleMetadata(filename)
        if inc == granularity:
            tempFile = os.path.join(targetFolder, filename)
            df = pd.read_excel(tempFile)
            df['Period'] = range(1, len(df)+1)
            df['AvgWeight'] = (df['birdWeightMax'] + df['birdWeightMin']) / 2
            normWeight = df['AvgWeight']/max(df['AvgWeight'])
            normWater = df['water1']/max(df['water1'])
            normFeed = df['accumulatedFeedConsumed']/max(df['accumulatedFeedConsumed'])
            plt.figure(figsize=(10, 7))
            plt.plot(df['Period'], normWeight, label = 'Normed Weight')
            plt.plot(df['Period'], normWater, label = 'Normed Water Consumption')
            plt.plot(df['Period'], normFeed, label = 'Normed Feed Consumption')
            plt.legend(loc="upper left")
            plt.title(wh)
            plt.xlabel('Periods')

            #Check to see if directory exists if not, create it, then save graphs. 
            cwd = os.getcwd()
            adir = os.path.dirname(cwd)
            savepath = os.path.join(adir, 'results')
            resFol = fM.createDirs(savepath, ['EDA_graphs'])
            plt.savefig(resFol[0] + '/' + filename.split('.')[0]+'CWWF.png')
            
def featureDelta(feature, df): #feature can be "water", "humidity", "temperature", or "birdWeight"
    featureMX = feature+'Max'
    featureMN = feature+'Min'
    delta = df[featureMX] - df[featureMN]
        
    return delta

def minMaxDeltaGraphs(targetFolder, features = ["water", "humidity", "temperature", "birdWeight"], granularity = 'H'):
    for f in features:
        filesL = os.listdir(targetFolder)
        plt.figure(figsize=(10, 7))
        for filename in filesL:
            wh, year, month, inc = titleMetadata(filename)
            if inc == granularity:
                tempFile = os.path.join(targetFolder, filename)
                df = pd.read_excel(tempFile)
                delta = featureDelta(f, df)
                plt.plot(delta, label = wh)
        plt.legend(loc="upper left")
        plt.title(f)
        plt.xlabel('Periods')
        
        cwd = os.getcwd()
        adir = os.path.dirname(cwd)
        savepath = os.path.join(adir, 'results')
        resFol = fM.createDirs(savepath, ['EDA_graphs'])
        plt.savefig(resFol[0] + '/' + year + '-'+ month +'MMD' + inc + '.png')
        
def uplwGraphs(targetFolder, features = ["water", "humidity", "temperature", "birdWeight"], granularity = 'H'):
    for f in features:
        filesL = os.listdir(targetFolder)
        
        for filename in filesL:
            plt.figure(figsize=(10, 7))
            wh, year, month, inc = titleMetadata(filename)
            if inc == granularity:
                tempFile = os.path.join(targetFolder, filename)
                df = pd.read_excel(tempFile)
                plt.plot(df[f+'Max'], label = 'Max')
                plt.plot(df[f+'Min'], label = 'Min')
                plt.legend(loc="upper left")
                plt.title('Upper & Lower ' + f + ' for ' + wh)
                plt.xlabel('Periods')
        
                cwd = os.getcwd()
                adir = os.path.dirname(cwd)
                savepath = os.path.join(adir, 'results')
                resFol = fM.createDirs(savepath, ['EDA_graphs'])
                plt.savefig(resFol[0] + '/' + f + filename.split('.')[0]+'UpLw' + inc + '.png')