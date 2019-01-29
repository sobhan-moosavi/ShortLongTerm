'''
Created on May 6, 2018 - Modified on June 4'th 2018 (minor modification)
This script is to combine weather and traffic events data. 
Traffic: EventId, Type(T/W), RefinedType, StartTime(UTC), EndTime(UTC), LocationLat, LocationLng, Distance(mi), AirportCode, ZipCode, Number, Street, County, City, State
Weather: EventId, Type(W/T), RefinedType, StartTime(UTC), EndTime(UTC), AirportCode
@author: moosas1
'''
import random

main_path = '/users/PAS0536/osu9965/Traffic/EventProcessing/Data/'
traffic_path = '/users/PAS0536/osu9965/Traffic/Output/'
files = ['All_Weather_Events_Feb2016_Aug2018', 'MapQuest-Augmented_Refined']


writer = open(main_path + 'AllEvents_EntireData.csv', 'w');
writer.write('EventId,Type(W/T),RefinedType,StartTime(UTC),EndTime(UTC),LocationLat,LocationLng,Distance(mi),AirportCode,Number,Street,Side,City,County,State,ZipCode\n')

weatherId = set()
trafficId = set()
noZip = 0

for f in files:
    header= False
    traffic = False
    if 'Weather' in f: path = main_path + f + '.csv'
    else: 
        path = traffic_path + f + '.csv'
        traffic = True
    with open(path, 'r') as lines:
        for r in lines:
            if header is not True:
                header= True
                continue
            parts = r.replace('\r', '').replace('\n', '').split(',')
            
            if traffic:  #this is traffic event file
                rnd = random.random()
                if rnd < 0:
                    continue
                id = len(trafficId) + 1
                if len(parts[25]) == 0:
                    parts[25] = 'N/A'
                else:
                    parts[25] = parts[25].split('-')[0]
                writer.write('T-' + str(id) + ',T,' + parts[4] + ',' + parts[11] + ',' + parts[12] + ',' + parts[6] + ',' + parts[7] + ',' + parts[10] +
                             ',' + parts[27] + ',' + parts[18] + ',' + parts[19] + ',' + parts[20] + ',' + parts[21] + ',' + 
                             parts[22] + ',' + parts[23] + ',' + parts[25] + '\n')
                trafficId.add(id)
                
            else:  #This is weather event file
                rnd = random.random()
                if rnd < 0:
                    continue
                id = len(weatherId) + 1
                writer.write('W-' + str(id) + ',W,' + parts[1] + '-' + parts[2] + ',' + parts[3] + ',' + parts[4] + ',N/A,N/A,N/A,' + parts[0] +
                              ',N/A,N/A,N/A,N/A,N/A,N/A,N/A\n')
                weatherId.add(id)
            
                
    print('Done by "%s"' % (f))
              
writer.close()

print ('Max Weather ID: %s, Max Traffic ID: %s' % (len(weatherId), len(trafficId)))
                