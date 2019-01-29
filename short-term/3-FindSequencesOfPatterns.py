'''
Created on May 13, 2018
This module is to extract sequential traffic pattern
@author: sobhan
'''

class event:
    type = ''
    refined_type = ''
    zip = ''
    childs = []
    parents = []
    visited = False
    def __init__(self, type, refined_type,zip, childs, parents):
        self.type         = type
        self.refined_type = refined_type
        self.zip          = zip
        self.childs       = (childs if childs[0] != '' else [])
        self.parents      = (parents if parents[0] != '' else [])
        self.visited      = False

def loadAllEvents():   
    allEvents = {}
    count = 0
    
    with open(path + 'AllEvents_CP_Aug2016-Aug2018.csv', 'r') as lines:
        header = True
        for r in lines:
            if header:
                header = False
                continue
            r = r.replace('\r', '').replace('\n', '').split(',')
            e = event(r[1], r[2], r[15], r[16].split(';'), r[17].split(';'))
            allEvents[r[0]]= e
            
            count += 1
            if count%500000 == 0: print('Loaded {} events!'.format(count))       
        
    print len(allEvents), 'events are loaded! \n'
    return allEvents

'''This function extracts and return all the existing sequences, given a node as root node'''
def recursivePatternChainFinder(root): 
    e = allEvents[root]
    if len(e.childs) == 0:
        return [[e.refined_type]]
    a_ls = []
    for c in e.childs:
        ls = recursivePatternChainFinder(c)
        for l in ls:
            a_ls.append([e.refined_type] + l)
    return a_ls

'''This function extracts and return all the existing sequences, given a node as root node'''
def iterativePatternChainFinder(root, _e): 
    
    finalSequences= []
    seq_current = [[root]]
    seq_next = []
    
    while len(seq_current)>0: 
                                                         
        for s in seq_current:   
            if s[-1] not in allEvents: continue
            e = allEvents[s[-1]]
            st = set()
            st.update(s)
            flag = True
            
            if len(e.childs) > 0:
                for c in e.childs:
                    if c not in allEvents: continue
                    _c = allEvents[c]
                    if _c.visited: continue
                    _c.visited = True
                    allEvents[c] = _c
                    
                    if c not in st:
                        flag = False
                        seq_next.append(s + [c])
                                            
            if flag or len(e.childs)==0:
                seq = []
                for _s in s: 
#                     seq.append(allEvents[_s].refined_type)
                    if _s not in allEvents: continue
                    seq.append(allEvents[_s].refined_type + '_' + _s)                    
                finalSequences.append(seq)
                                                                                                        
        seq_current = seq_next    
        seq_next = []    
        
    return finalSequences


def findSequences():
    zip_to_sequences = {}
    
    totalSeqs = 0
    eventCount = 0
    
    for _e in allEvents:        
        eventCount += 1
        if eventCount%100000 == 0: print('processed {} events out of {} total events'.format(eventCount, len(allEvents)))
        
        e = allEvents[_e]
                                         
                         
        
        if len(e.childs) == len(e.parents) == 0: #no child and parent
            continue
        if len(e.parents) > 0: #if some event has a parent, this means it is already processed or will be
            continue
        
        seq = []
        c_idx = []
        idx = 0
        for c in e.childs: #c is an event without parent
#             seqSet = recursivePatternChainFinder(c)
            if c not in allEvents: continue
            _c = allEvents[c] 
            if _c.visited: continue
            _c.visited = True
            allEvents[c] = _c
            
            seqSet = iterativePatternChainFinder(c, _e)            
                                             
            for s in seqSet:
                seq.append(([e.refined_type + '_' + _e] + s))
#                 seq.append(([e.refined_type] + s))
                c_idx.append(idx)
            idx += 1
        
        totalSeqs += len(seq)
        if totalSeqs % 50000 ==0:
            print 'totalSeqs:', totalSeqs
        
        idx = 0
        for s in seq:
            if e.type == 'T':
                z = e.zip
            else:
                if e.childs[c_idx[idx]] not in allEvents: continue
                z = allEvents[e.childs[c_idx[idx]]].zip
                
            seqs = []
            if z in zip_to_sequences:
                seqs = zip_to_sequences[z]
            seqs.append(s)
            zip_to_sequences[z] = seqs
            
            idx += 1
    
    print 'total extracted sequential patterns:', totalSeqs
    return zip_to_sequences

def printSequences():
    '''Print the extracted sequences for each zip'''
    writer = open(path + 'SequentialPatterns.csv', 'w')
    writer.write('Zip,Pattern\n')
    for z in zip_to_sequences:
#         if z != '94103': continue
        sequences = zip_to_sequences[z]
        for s in sequences:
            writer.write(z + ',' + ';'.join(s) + '\n')
    writer.close()     


path = '/users/PAS0536/osu9965/Traffic/EventProcessing/Data/'
                                                             
allEvents = loadAllEvents()        
zip_to_sequences = findSequences()
printSequences()

