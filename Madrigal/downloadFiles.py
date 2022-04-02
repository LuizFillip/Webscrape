# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 14:25:27 2022

@author: LuizF
"""


import madrigalWeb.madrigalWeb
import os,sys,os.path

def download_file(startTime = [2015, 2, 3, 21, 23, 42],
                  endTime = [2015, 2, 4, 7, 55, 21]):
    
    
    expList = madrigalObj.getExperiments(code, 2011,9,1,0,0,0, 2011,12,31,0,0,0)
    
    allfiles = []
    
    for i in range(len(expList)):
        fileList = madrigalObj.getExperimentFiles(expList[i].id)
        allfiles.append(fileList) 
        
    
    for i in range(len(allfiles)):
        fileList = allfiles[i]
        for thisFile in fileList:
            if thisFile.category == 1:
                thisFilename = thisFile.name
                Filename = thisFile.name.split('/')
                Filename = Filename[len(Filename) - 1]
                # Do download in 'txt' format
                filename = Filename.replace('hdf5', 'txt')
                result = madrigalObj.downloadFile(thisFilename, filename, 
                                       user_fullname, user_email, user_affiliation, "simple")
                break
            
            
def get_infos(madrigalUrl = 'http://cedar.openmadrigal.org',    
                user_fullname = "Luiz Fillip Rodrigues Vital",
                user_email = "luizfillip@outlook.com",
                user_affiliation = "UFCG"):
    #constants
    #madrigalurl = "http://www.haystack.mit.edu/madrigal"
    
    madrigalObj = madrigalWeb.madrigalWeb.MadrigalData(madrigalUrl)
    # create the main object to get all needed info from Madrigal
    
    return madrigalObj

def time_calculator():
    #start and end[year, month, day, hour, minute, second], step, parameter
    result = madrigalObj.madTimeCalculator(2013, 1, 1, 0, 0,0, 2013, 12, 31, 0, 0, 0, 1, 'kp, dst')
    result

# Get Instrument in single Experiment

madrigalObj = get_infos()

#choice name experiment and your site
instrument = 'Cariri Brazil FPI'
code = None
instList = madrigalObj.getAllInstruments()

for inst in instList:
    print(inst)
    #if inst.name.lower() == instrument.lower():
    #    code = inst.code
    #   print(inst) #p
    #    break
        