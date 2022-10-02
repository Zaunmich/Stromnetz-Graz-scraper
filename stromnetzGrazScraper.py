# IMPORTANT Note for the certificates:
#  stromnetz-graz.at does not supply the full certificate chain that is needed for API calls!
# Steps to add those certificates:
# 1. Run  https://www.ssllabs.com/ssltest/analyze.html?d=webportal.stromnetz-graz.at 
# 2. Under 'Certification Paths' you can download the missing certificates.
# 3. Run 'certifi.where()' to get the path to the cacert.pem used by pythons requests module (usually .venv\Lib\site-packages\certifi\cacert.pem)
# 4. Copy the missing certificates from step 2. into the cacert.pem file

import requests
import certifi

from datetime import date, datetime, timedelta, time

from config import STROMNETZGRAZ_EMAIL, STROMNETZGRAZ_PWD


def getLoginToken():

    # create payload
    loginPayload = {
        "email": STROMNETZGRAZ_EMAIL,
        "password": STROMNETZGRAZ_PWD
    }
    try:
        loginRequest = requests.post('https://webportal.stromnetz-graz.at/api/login', json=loginPayload,)
        loginResponse = loginRequest.json()
        token = loginResponse['token']
        print('Login successful!')
        return token
    except:
        print('Login request has failed. Have you added the required certificates to cacert.pem? Are they up to date?')
        raise

def getMeterID(token):
    
    # get an overview of all installations linked to that account
    authHeader = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    installationsRequest = requests.post('https://webportal.stromnetz-graz.at/api/getInstallations', headers=authHeader,)
    installationsResponse = installationsRequest.json()

    meterPointID = installationsResponse[0]['meterPoints'][0]['meterPointID'] # assume you only have 1 meter point (or are only interested in the first one)
    return meterPointID


def getReadings(token, meterPointID, startTime, endTime):
    # startTime and endTime should have timezone info available! e.g. datetime.datetime.now().astimezone()
    # max allowed time-frame is 1 day for quarterhourly data

    authHeader = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    queryPayload = {
    "meterPointId": meterPointID,
    "fromDate": startTime.isoformat(),
    "toDate": endTime.isoformat(),
    "interval": "QuarterHourly",
    "unitOfConsump": "KWH"
    }

    meterRequest = requests.post('https://webportal.stromnetz-graz.at/api/getMeterReading', headers=authHeader, json=queryPayload,)
    meterData = meterRequest.json()
    return meterData

def quickYesterdayData():
    # quick function to get the power consumption of yesterday

    # build the time-frame of interest
    today = date.today()
    yesterday = today - timedelta(days = 1)
    yesterdaystart = datetime.combine(yesterday, time.min).astimezone()
    yesterdayend = datetime.combine(yesterday, time.max).astimezone()

    # get the token
    token = getLoginToken()
    # get meterID
    meterPointID = getMeterID(token)
    # get the data
    data = getReadings(token,meterPointID,yesterdaystart,yesterdayend)

    return data

# print(quickYesterdayData())