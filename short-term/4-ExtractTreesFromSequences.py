'''
Created on Jul 7, 2018, Modified on Aug 27
Using this code, we extract tree structures out of sequences of patterns for different zip-codes. 
This way, we first extract raw tree structures, then apply DFS and generate the sequence encoding, as it is interpretable by TreeMiner C++ code. 
Modification: We have following label conversion here:
    snow-heavy, snow-moderate, snow-light ==> snow
    rain-heavy, rain-moderate, rain-light ==> rain
    construction-short, construction, Construction-Other ==> construction
    congestion-slow, congestion-moderate, congestion-fast ==> congestion
    event-short, event-long ==> event
    fog-moderate, fog-severe ==> fog
The rest of the types will remain as before. 
@author: sobhan
'''
import cPickle

class node:
    label = ''
    parent = ''
    childs = []
    color = 'w'
    def __init__(self, label, parent, cSet, color='w'):
        self.label  = label
        self.parent = parent
        self.childs = cSet
        self.color  = color  #w: not-visited, 'g': visited but not finished, 'b': finished
        

def loadSequenceData():
    zipToSequences = {}
    with open(path + 'SequentialPatterns.csv', 'r') as file:
        currentZip = ''
        patterns = []
        for ln in file:
            if 'Zip' in ln: continue
            parts = ln.replace('\r','').replace('\n', '').split(',')
            if parts[0] == currentZip: patterns.append(parts[1])
            else:
                if len(currentZip) > 0:
                    zipToSequences[currentZip] = patterns
#                     return zipToSequences
                patterns = [parts[1]]
                currentZip = parts[0]
                
        zipToSequences[currentZip] = patterns
           
    return zipToSequences


def createBasicUnorderedRootedTreeStructures():
    zipToNodes = {}
    zipToRoots = {}
    
    for z in zipToSequences:
        sequences = zipToSequences[z]
        nodes = {}
        roots = []
        for s in sequences:
            parts = s.split(';')
            for i in range(len(parts)):
                if parts[i] in nodes: 
                    n = nodes[parts[i]]
                    if i < len(parts)-1: 
                        n.childs.add(parts[i+1])                        
                else: 
                    cSet = set()
                    if i < len(parts)-1: cSet.add(parts[i+1])
                    n = node(parts[i].split('_')[0], (-1 if (i-1)<0 else parts[i-1]), cSet)
                    if n.parent == -1: roots.append(parts[i]) 
                
                nodes[parts[i]] = n            
        zipToNodes[z] = nodes
        zipToRoots[z] = roots
#         print z, len(nodes), len(roots)
    
    return zipToNodes, zipToRoots

def createLabelToCode():
    labelToCode = {}
    
    labelToCode['snow-light'] = '1'
    labelToCode['snow-moderate'] = '1'
    labelToCode['snow-heavy'] = '1'
    
    labelToCode['rain-light'] = '2'
    labelToCode['rain-moderate'] = '2'
    labelToCode['rain-heavy'] = '2'
    
    labelToCode['Construction'] = '3'
    labelToCode['Construction-Other'] = '3'
    labelToCode['Construction-Short'] = '3'
    
    labelToCode['Congestion-Fast'] = '4'
    labelToCode['Congestion-Moderate'] = '4'
    labelToCode['Congestion-Slow'] = '4'
    
    labelToCode['Event-Short'] = '5'
    labelToCode['Event-Long'] = '5'
    
    labelToCode['fog-moderate'] = '6'
    labelToCode['fog-severe'] = '6'
    
    labelToCode['Lane-Blocked'] = '7'
    labelToCode['cold-severe'] = '8'
    labelToCode['Other'] = '9'
    labelToCode['storm-severe'] = '10'
    labelToCode['Broken-Vehicle'] = '11'
    labelToCode['Incident-Weather'] = '12'
    labelToCode['precipitation-UNK'] = '13'
    labelToCode['hail-other'] = '14'
    labelToCode['Incident-Other'] = '15'
    labelToCode['Incident-Flow'] = '16'
    labelToCode['Accident'] = '17'
    
    return labelToCode
    
def convertToTreePreOrderedDfsEncoding():
    labelToCode = createLabelToCode()
    zipToEncoding = {}
    
    for z in zipToRoots:
        roots = zipToRoots[z]
        nodes = zipToNodes[z]
        encodings = []
        
        for r in roots:
            list = [r]
            #if nodes[r].label not in labelToCode: labelToCode[nodes[r].label] = str(len(labelToCode) + 1) 
            enc = labelToCode[nodes[r].label]
            nodes[r].color = 'b'  # as our graph is a tree, we don't need three colors; thus, just use white (w) and black (b)
            while len(list)>0:
                n = list[len(list)-1]
                flag = False                
                for c in nodes[n].childs:
                    if nodes[c].color == 'w':
                        flag = True
                        nodes[c].color = 'b'
                        list.append(c)
                        
                        #if nodes[c].label not in labelToCode: labelToCode[nodes[c].label] = str(len(labelToCode) + 1)
                        enc += ' ' + labelToCode[nodes[c].label]
                        break
                if flag: continue
                list.pop(len(list)-1)
                if n not in roots:  enc += ' -1'
            
            enc = str(len(encodings)+1) + ' ' + str(len(encodings)+1) + ' ' + str(len(enc.split(' '))) + ' ' + enc 
            encodings.append(enc)
        zipToEncoding[z] = encodings
    
    return zipToEncoding, labelToCode
                
                
path = 'Data/'
zipToSequences = loadSequenceData()
print 'Sequences are loaded!'
zipToNodes,zipToRoots = createBasicUnorderedRootedTreeStructures()
print 'Trees are created!'
zipToEncoding, labelToCode = convertToTreePreOrderedDfsEncoding()
print 'Encodings are created!'

cPickle.dump(zipToEncoding, file(path + 'zipToEncoding.pkl', 'w'))
cPickle.dump(labelToCode, file(path + 'labelToCode.pkl', 'w'))
print 'dumping is completed!'