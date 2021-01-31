'''
Created on Jul 8, 2018
This code is to feed tree encodings to SLEUTH tree mining C++ code and get the frequent embedded (or maybe induced) unordered tree patterns.  
@author: sobhan
'''
import cPickle
import time
from time import sleep
import csv
from subprocess import check_output
import subprocess
import threading
import multiprocessing
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--min_sup_fixed', type=int, default=500)
parser.add_argument('--max_tree_length', type=int, default=25)
args = parser.parse_args()
min_sup_fixed = args.min_sup_fixed
max_tree_length = args.max_tree_length


def return_minsup(x):
    if x <= 100:
        return round(x*.2)
    if x <= 200:
        return round(max(100*.2, x*.18))
    if x <= 500:
        return round(max(200*.18, x*.15))
    if x <= 750:
        return round(max(500*.15, x*.12))
    if x <= 1200:
        return round(max(750*.12, x*.1))
    if x <= 2000:
        return round(max(1200*.1, x*.08))
    if x <= 3000:
        return round(max(2000*.08, x*.07))
    if x <= 4000:
        return round(max(3000*.07, x*.06))
    else:
        return round(max(4000*.06, x*.05))
        

def readCsvToDict(file):
    reader = csv.reader(open(path + file, 'r'))
    d = {}
    for row in reader:
       k, v = row
       d[k] = v
    return d

    
def sleuth(z, encodings, i_e = 'E'):
    total=passed = 0
    # make temporary db for encodings
    #print len(encodings)
    input_name = 'tmp/input_' + file_name + '.db'
    w = open(path + input_name, 'w')
    lg = 0
    for e in encodings: 
        l = int(e.split(' ')[2])        
        if l<max_tree_length:       
            w.write(e + '\n')
            lg+=1           
    w.close()
    
    total += len(encodings)
    passed += lg
    
    #print ('Length after filtering by tree length ==>', lg)
    min_sup = min(return_minsup(lg), min_sup_fixed)
    #return total, passed
    #min_sup = 100
    
    # run sleuth algorithm to find frequent induced/embedded unordered tree patterns
    #subprocess.call(['./vtreeminer', '-i', '/users/PAS0536/osu9965/Traffic/EventProcessing/' + input_name, '-S', str(min_sup), '-o'])  #using capital S to have absolute support value!
    out = check_output(['./vtreeminer', '-i', '/users/PAS0536/osu9965/Traffic/EventProcessing/' + input_name, '-S', str(min_sup), '-o'])
    w = open(path + file_name, 'a')
    #print out.split('F')[0].split(')')[1]
    out = out.split('F')[0].split(')')[1].split('\n')
    for p in out:
        if len(p)==0: continue
        sp = int(p.split(' - ')[1])*1.0
        p = p.split('- ')[0]
        p = p + '$'
        p = p.replace('  $', '').replace(' $', '')
        if len(p.split(' ')) == 1: continue
        #w.write(z + ',' + p + ',' + str(round(sp/len(encodings), 3)) + '\n')
        w.write(z + ',' + p + ',' + str(round(sp/lg, 3)) + '\n')
        
    w.close()
    return total, passed
    
path = '/users/PAS0536/osu9965/Traffic/EventProcessing/'

# load pickle files related to tree-encoding for all zip-codes
start = time.time()
zipToEncoding = cPickle.load(file(path + 'Data/zipToEncoding.pkl', 'r'))
labelToCode   = cPickle.load(file(path + 'Data/labelToCode.pkl', 'r'))

# load zip to city
zipToCity = readCsvToDict('Data/zip_to_CityState.csv')

# load zip to State
zipToState = readCsvToDict('Data/zip_to_State.csv')

cityToZips = {}
for z in zipToEncoding:
    if z == 'N/A': continue
    s = zipToCity[z]
    _zips = []
    if s in cityToZips: _zips = cityToZips[s]
    _zips.append(z)
    cityToZips[s] = _zips
print 'All datasets are loaded for %d zip codes in %.1f sec!' % (len(zipToEncoding), time.time()-start)

# the output file for frequent tree patterns
file_name = 'frequent_trees_City_MSF-{}_MTL-{}.csv'.format(min_sup_fixed, max_tree_length)
w = open(path + file_name, 'w')
w.write('City,Pattern,Support\n')
w.close()

print ('max_tree_length:', max_tree_length)
# mining frequent tree patterns
start = time.time()
count = totalTrees = totalKept = stoppedZipCodes = 0
main_start = time.time()
start = time.time()
st_count = 0
Total, Passed = 0,0

writer = open(path + 'State_TreeCount_CityBased.csv', 'w')
writer.write('State,Count\n')
state_total_pattern = {}

processed_citities = 0

for s in cityToZips:
    # if s != 'OilCity-PA': continue
    #time.sleep(0.1)
    encodingSet = []
    _zips = cityToZips[s]
    cnt = 0
    for z in _zips: 
        for enc in zipToEncoding[z]:
            _parts = enc.split(' ')            
            enc = str(len(encodingSet)+1) + ' ' + str(len(encodingSet)+1)
            for i in range(2,len(_parts)): enc += ' ' + _parts[i]
            encodingSet.append(enc)
        cnt += 1
        #if cnt ==250:  break
    
    if len(encodingSet) < 50: continue   #trivial cases which we filter for the sake of speed up in the process! this will discard 10% of the data, which is negligible!
    #print (str(st_count), 'City:', s, '#Encodings:', len(encodingSet))  
    
    st_count += 1
    tt, ps = sleuth(s, encodingSet, 'E')    
    Total += tt
    Passed += ps
    count += 1    
    #print 'City %s is processed in %.1f sec! total processing time: %.1f sec!' %(s, time.time()-start, time.time()-main_start)
    start = time.time()
    
    _state = s.split('-')[1]
    if _state in state_total_pattern: state_total_pattern[_state] = state_total_pattern[_state] + ps
    else: state_total_pattern[_state] = ps
    
    processed_citities += 1
    if processed_citities%100 == 0:
        print 'Processed {} cities out of {}, progress: {:.2f}%!'.format(processed_citities, len(cityToZips), float(processed_citities)/len(cityToZips)*100)
    #if st_count == 10: break

  
print 'Pattern mining process is completed in %.1f sec!' %(time.time()-start)
print 'Total Trees: %d, Total Passed the Criteria: %d, Pass Ratio %.2f' %(Total, Passed, (float(Passed)/Total)*100)

for st in state_total_pattern:
    writer.write(st + ',' + str(state_total_pattern[st]) + '\n')
writer.close()
