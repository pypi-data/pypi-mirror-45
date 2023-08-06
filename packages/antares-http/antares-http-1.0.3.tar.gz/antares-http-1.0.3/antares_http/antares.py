'''
Antares Python v1.0.0

Available functions:

setAccessKey()
getAccessKey()
get()
getAll() 
getAllId()
getDevices()
send()

'''

import requests
import json

_antaresAccessKey = ''

def test():
    print('Hello from antares package!')

def setAccessKey(accessKey, debug=False):
    global _antaresAccessKey
    _antaresAccessKey = accessKey

    if(debug):
        print('Access key:', _antaresAccessKey)
    

def getAccessKey():
    global _antaresAccessKey
    return _antaresAccessKey

def get(projectName, deviceName, debug=True):
    # print('Requesting...')
    url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}/la'.format(projectName, deviceName)
    
    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json;ty=4',
        'Accept' : 'application/json'
    }

    r = requests.get(url, headers=headers)
    response = r.json()
    data = response['m2m:cin']
    
    parsedContent = {}
    try:
        parsedContent = json.loads(data['con'])
    except:
        parsedContent = data['con']

    finalResponse = {
        'resource_name': data['rn'],
        'resource_identifier': data['ri'],
        'parent_id': data['pi'],
        'created_time': data['ct'],
        'last_modified_time': data['lt'],
        'content' : parsedContent
    }
    
    if(debug):
        print(json.dumps(finalResponse, indent=4))
    # print(finalResponse['content'])
    return finalResponse

def getDevices(projectName, debug=True):
    # print('Requesting...')
    url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}?fu=1&ty=3'.format(projectName)
    
    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json;ty=3',
        'Accept' : 'application/json'
    }

    r = requests.get(url, headers=headers)
    response = r.json()
    deviceUrl = response['m2m:uril']

    devicesList = []
    for device in deviceUrl:
        device = device.split('/');
        devicesList.append(device[4]) 
    
    if(debug):
        print(json.dumps(devicesList, indent=4))
    # print(finalResponse['content'])
    return devicesList

def getAll(projectName, deviceName, limit=0, debug=False):
    # print('Requesting...')
    if(limit != 0):
        url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}?fu=1&ty=4&drt=1&lim={}'.format(projectName, deviceName, limit)
    else:
        url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}?fu=1&ty=4&drt=1'.format(projectName, deviceName)

    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json',
        'Accept' : 'application/json'
    }

    r = requests.get(url, headers=headers)
    response = r.json()
    allData = response['m2m:uril']
    dataCounter = 0
    dataStorage = []
    for urlInd in allData:
        # print(urlInd)
        url = 'https://platform.antares.id:8443/~{}'.format(urlInd)
        r = requests.get(url, headers=headers)
        response = r.json()['m2m:cin']
        dataCounter+=1

        # Parse content
        parsedContent = {}
        try:
            parsedContent = json.loads(response['con'])
        except:
            parsedContent = response['con']

        finalResponse = {
            'resource_name': response['rn'],
            'resource_identifier': response['ri'],
            'parent_id': response['pi'],
            'created_time': response['ct'],
            'last_modified_time': response['lt'],
            'content' : parsedContent
        }

        if(debug):
            print('Get success:{} out of {}'.format(dataCounter, len(allData)))
        
        dataStorage.append(finalResponse)
        if(limit > 0):
            if(dataCounter >= limit):
                if(debug):
                    print(json.dumps(dataStorage, indent=4))
                    print('Data size: {}'.format(len(dataStorage)))
                return dataStorage
        else:
            if(dataCounter >= len(allData)):
                if(debug):
                    print(json.dumps(dataStorage, indent=4))
                    print(len(dataStorage))
                return dataStorage

def getAllId(projectName, deviceName, limit=0, debug=False):
    # print('Requesting...')
    if(limit != 0):
        url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}?fu=1&ty=4&drt=1&lim={}'.format(projectName, deviceName, limit)
    else:
        url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}?fu=1&ty=4&drt=1'.format(projectName, deviceName)

    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json',
        'Accept' : 'application/json'
    }

    r = requests.get(url, headers=headers)
    response = r.json()
    allData = response['m2m:uril']
    
    if(debug):
        print(json.dumps(allData, indent=4))
        print('Length: {} data'.format(len(allData)))
    return allData

def send(data, projectName, deviceName, debug=False):
    # print('Requesting...')
    url = 'https://platform.antares.id:8443/~/antares-cse/antares-id/{}/{}'.format(projectName, deviceName)
    
    # print('Access key: ', getAccessKey())

    headers = {
        'X-M2M-Origin' : getAccessKey(),
        'Content-Type' : 'application/json;ty=4',
        'Accept' : 'application/json',
    }

    strData = ''
    try:
        strData = json.dumps(data)    
    except:
        strData = data

    dataTemplate = {
        "m2m:cin" : {
            "con" : strData,
        }
    }
    dataTemplate = json.dumps(dataTemplate)

    # print(dataTemplate)
    # print(url)

    r = requests.post(url, headers=headers, data=dataTemplate)
    response = r.json()
    data = response['m2m:cin']

    parsedContent = {}

    try:
        parsedContent = json.loads(data['con'])
    except:
        parsedContent = data['con']

    finalData = {
        'resource_name' : data['rn'],
        'resource_identifier' : data['ri'],
        'parent_id' : data['pi'],
        'created_time' : data['ct'],
        'last_modified_time' : data['lt'],
        'content' : parsedContent
    }

    if(debug):
        print(json.dumps(finalData, indent=4))

    return(finalData)
