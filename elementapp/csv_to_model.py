from pathlib import Path
import csv
import pandas as pd
import re
import validators
from .models import *
import traceback
import logging
from datetime import datetime
import threading
import time
import os


logging.basicConfig(filename=("logs/"+str(datetime.now().timestamp()))+'.log', level=logging.ERROR)
# logging.basicConfig(filename='sher_assignment.log', encoding='utf-8', level=logging.DEBUG)



def getfilepath():
    relative_path = Path(__file__)
    csv_file_parent = relative_path.parent.parent
    csv_file =  (str(csv_file_parent)+'\\test_application_data-Sheet1.csv')
    return csv_file



def largecsvreading():
    
    csv_file = getfilepath()
    if os.path.isfile(csv_file)==False:
        print(csv_file)
        print("Sorry, CSV file does not exist at given path or has been moved out")
        return False

    """ we will read the file and will perform some validation on it """

    """ divide the reading into chunk size if the csv file is too large and pandas has this feature """
    chunks = pd.read_csv(csv_file, chunksize=100000)
    data  = pd.concat(chunks)

    """ lets define some validation functions for our data  """
   
    def reg_check(arg_string):
        return re.sub('[^A-Za-z0-9,."\n]+',' ',arg_string)
    
    def utf_8_check(test_string):
        if isinstance(test_string,type('unicode')):
            return test_string
        else:
            return Nan

    def validate_url(url):
        if validators.url(url):
            return url
        else:
            return 'https://www.default.com'

    """ lets do some validation straight away on dataframe """
    """ first lets check for duplicates """
    if data.duplicated().sum() > 0:
        data.drop_duplicates()

    """ we want to drop the data from dataframe where there are null values in any column"""
    """ there can be lot of different ways but it all depends on requirements of client, how they want to
    handle NaN values, either defaults needs to inserted, or drop these rows, or leave it as or put custom msg"""
    """ __we will drop these as of this case to make data consistent__ """ 
    data = data.dropna()

    """ lets have a look at data """
    # print(data.head())

    """ strip leading and trailing extra spaces """
    data['title'] = data['title'].astype('str').str.strip()
    data['description'] = data['description'].astype('str').str.strip()
    data['image'] = data['image'].astype('str').str.strip()

   
    
    """ make sure there no special characters for title and description except comma,period, double quotes """
    """ this is based on my onbservation from data, it all depends on project requirements  """
    data['title'] = data['title'].apply(reg_check)
    data['description'] = data['description'].apply(reg_check)

    """ now we will check if the image urls are valid URLS as there can be malformd urls """
    """ otherwise replace with default URL or other actions can be performed such as removing etc  """
    """ it all depends on requirements of the project and instruction from team lead """
    data['image'] = data['image'].apply(validate_url)


    """ check if the columns are utf-8 compliant else write Nan and we will drop these later """
    data['title'] = data['title'].apply(utf_8_check)
    data = data.dropna()
    savetodb(data)
    return data


def savetodb(data):
    # print(data)
    """ finally we have to save this data in database, and we want to avoid duplicates """
    for i in range(len(data)):
        if information.objects.filter(title=data.iloc[i]['title']).exists()==False:
            information_table  = information(title=data.iloc[i]['title'],description=data.iloc[i]['description'],image=data.iloc[i]['image'])
            """ we have checked everything before saving but still something comes up we want it to exit gracefully """
            try:
                information_table.save()
            except Exception:
                logging.error(str(datetime.now())+"  :  "+str(traceback.print_exc()))
                print(str(traceback.print_exc()))


def main():
    largecsvreading()
#    sync_thread = threading.Thread(target=largecsvreading,name='database_synchronizer')
    print("Synchronizing the csv file with db periodically!")
    """ frequency really depends on requirement for now I put 1 hour """
    threading.Timer(3600,main).start()
