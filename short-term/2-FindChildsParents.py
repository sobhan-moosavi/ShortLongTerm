'''
Created on May 15, 2018; Latest update: May 28, 2018. 
This code is to find correlated events and specify childs and parents for a given event
@author: sobhan
'''

import time
import math
from datetime import date, datetime, timedelta
import thread
import threading

class event:
    eventId = ''
    type = ''
    refinedType = ''
    startTime = '' #UTC 
    endTime = '' #UTC
    locationLat = 0
    locationLng = 0
    distance = 0 #mi
    airportCode = ''
    number = 0
    street = ''
    side = ''
    city = ''
    county = ''
    state = ''
    zipCode = ''
    childs = set()
    parents = set()
    
    def __init__(self, eventId, type, refinedType, startTime, endTime, locationLat, locationLng, distance, 
                 airportCode, number, street, side, city, county, state, zipCode, childs=set(), parents=set()):
        self. eventId = eventId
        self.type = type
        self.refinedType = refinedType
        self.startTime = datetime.strptime(startTime.replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        self.endTime = datetime.strptime(endTime.replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        self.locationLat = locationLat
        self.locationLng = locationLng
        self.distance = distance
        self.airportCode = airportCode
        self.number = number
        self.street = street
        self.side = side
        self.city = city
        self.county = county
        self.state = state
        self.zipCode= zipCode
        self.childs = childs
        self.parents = parents
        
def haversineDistance(aLat, aLng, bLat, bLng):
    #From degree to radian
    fLat = math.radians(aLat)
    fLon = math.radians(aLng)
    sLat = math.radians(bLat)
    sLon = math.radians(bLng)
        
    R = 3958.7564 #mi
    #R = 6371000.0 #meters
    #R = 6371.0 #km
    dLon = sLon - fLon
    dLat = sLat - fLat
    a = math.sin(dLat/2.0)**2 + (math.cos(fLat) * math.cos(sLat) * math.pow(math.sin(dLon/2.0), 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    
    return R * c

def loadZipToAirportCode():
    zipToAirpot = {}
    
    with open(path + 'AirportForZipsUSA_Augmented.csv', 'r') as lines:
        header = True
        for r in lines:
            if header:
                header = False
                continue
            r = r.replace('\r', '').replace('\n', '').split(',')
            zipToAirpot[r[0]] = r[1]            
    
    zipToAirpot['N/A'] = 'N/A'
    
    return zipToAirpot

def loadEventData():    
    zip_to_traffic_event = {}
    airport_to_weather_event = {}
    
    start = time.time()
    count = 0
    
    with open(path + 'AllEvents_Distinct.csv', 'r') as events:
        header = True
        
        for r in events:
            if header:
                header = False
                continue
            r = r.replace('\r', '').replace('\n', '').split(',')
            events = {}
            if r[1] == 'W':
                if r[8] in airport_to_weather_event:
                    events = airport_to_weather_event[r[8]]
                childs = set()
                parents = set()
                e = event(eventId=r[0], type='W', refinedType=r[2], startTime=r[3], endTime=r[4], locationLat=0, locationLng=0,  
                          distance=0, airportCode=r[8], number=0, street='NA', side='NA', city='NA', county='NA', state='NA', 
                          zipCode='NA', childs=childs, parents=parents)
                events[e.eventId] = e
                airport_to_weather_event[r[8]] = events
            else:
                if len(r[15]) == 0:
                    continue
                if r[15] in zip_to_traffic_event:
                    events = zip_to_traffic_event[r[15]]
                childs = set()
                parents = set()
                e = event(eventId=r[0], type='T', refinedType=r[2], startTime=r[3], endTime=r[4], locationLat=float(r[5]), 
                          locationLng=float(r[6]), distance=float(r[7]), airportCode=r[15], number=(0 if r[9]=='N/A' else int(r[9])), 
                          street=r[10], side=r[11], city=r[12], county=r[13], state=r[14], zipCode=r[15], childs=childs, parents=parents)
                events[e.eventId] = e
                zip_to_traffic_event[r[15]] = events  
            
            count += 1
            if count %100000 ==0: print 'processed {} lines'.format(count)
                    
            
    print ('Event data is loaded in: %.1f sec'%(time.time()-start))
    return zip_to_traffic_event, airport_to_weather_event

def findChildParents(wTimeThreshs, trTimeThresh = 10, distanceThresh = 0.2): 
    '''Time thresholds are in minutes'''
    start = time.time()
    count = 0
    totalRels = 0
    
    for z in zipToAirport:      
        count += 1
        if count%10 == 0:
            print '#Processed Zips: %d, progress: %.2f' % (count, float(count)/len(zipToAirport)*100)
              
        incidents = {}
        events = {}
        if z in zip_to_traffic_event: 
            incidents = zip_to_traffic_event[z]
        if zipToAirport[z] in airport_to_weather_event:
            events= airport_to_weather_event[zipToAirport[z]]
        
        if len(incidents) == 0:
            continue
        
        for i1 in incidents:            
            trigger = False
            for i2 in incidents:               
                if trigger:
                    dist = haversineDistance(incidents[i1].locationLat, incidents[i1].locationLng, incidents[i2].locationLat, incidents[i2].locationLng)
                    if dist > (incidents[i1].distance + distanceThresh) or \
                        incidents[i1].street!=incidents[i2].street or \
                        incidents[i1].side!=incidents[i2].side or \
                        (incidents[i1].endTime + timedelta(minutes=trTimeThresh))<incidents[i2].startTime or \
                        incidents[i1].startTime>(incidents[i2].endTime + timedelta(minutes=trTimeThresh)):
                        continue
                    
                    if incidents[i1].startTime < incidents[i2].startTime:
                        incidents[i1].childs.add(i2)
                        incidents[i2].parents.add(i1)
                    else:           
                        incidents[i2].childs.add(i1)
                        incidents[i1].parents.add(i2)
                    
                    totalRels += 1
                   
                elif i1 == i2:
                    trigger = True
        
        
            for e in events:   
                try: th = wTimeThreshs[events[e].refinedType]
                except: th = 5              
                '''(1) incident can't start way after the event is ended. (2) incident can't finish before the event starts. 
                (3) incident can't start before the event starts'''
                if incidents[i1].startTime> (events[e].endTime + timedelta(minutes=th)) or \
                    incidents[i1].endTime < events[e].startTime or \
                    incidents[i1].startTime < (events[e].startTime + timedelta(minutes=5)) :   #this last one is actually to consider the gap in weather report
                    continue            
                
                incidents[i1].parents.add(e)
                events[e].childs.add(i1)    
                totalRels += 1            
#                 print e, events[e].childs, events[e].parents      
            
#             if len(incidents[i1].childs)>0 or len(incidents[i1].parents)>0:    
#                 print i1, incidents[i1].childs, incidents[i1].parents          
        
        if len(incidents) > 0:
            zip_to_traffic_event[z] = incidents        
        if len(events) > 0:
            airport_to_weather_event[zipToAirport[z]] = events
    
    print '\n%d Child-Parents are found in: %.1f sec'%(totalRels, time.time()-start)
    return zip_to_traffic_event, airport_to_weather_event

def writeAllEvents():
    
    writer = open(path + 'AllEvents_CP.csv', 'w')
    
    with open(path + 'AllEvents_Distinct.csv', 'r') as events:
        header = True
        
        for r in events:
            if header:
                writer.write(r.replace('\r', '').replace('\n', '') + ',Childs,Parents\n')
                header = False
                continue
            l = r
            r = r.replace('\r', '').replace('\n', '').split(',')
            childs = parents = set()
            if r[1] == 'W':
                if r[8] in airport_to_weather_event:
                    events = airport_to_weather_event[r[8]]                                
                    childs, parents = events[r[0]].childs, events[r[0]].parents                 
            else:
                if len(r[15]) == 0:
                    continue
                if r[15] in zip_to_traffic_event:
                    events = zip_to_traffic_event[r[15]]
                    childs, parents = events[r[0]].childs, events[r[0]].parents
            
            cl_list = p_list = ''
            if len(childs) > 0:
                for c in childs: cl_list += ';' + c
                cl_list = cl_list[1:]
            if len(parents) > 0:
                for p in parents: p_list += ';' + p
                p_list = p_list[1:]
            
            writer.write(l.replace('\r', '').replace('\n', '') + ',' + cl_list + ',' + p_list + '\n')
            
    writer.close()
    

if __name__ == "__main__":  	
	path = '/users/PAS0536/osu9965/Traffic/EventProcessing/Data/'
	zipToAirport = loadZipToAirportCode()
	zip_to_traffic_event, airport_to_weather_event = loadEventData()
	wTimeThreshs = {'rain-light':5, 'rain-moderate': 10, 'rain-heavy':15, 'snow-light':20, 'snow-moderate': 40, 'snow-heavy': 60}  #Will be completed based on different weather event types 
	zip_to_traffic_event, airport_to_weather_event = findChildParents(wTimeThreshs)
	writeAllEvents()
