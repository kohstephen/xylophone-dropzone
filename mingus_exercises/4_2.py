'''
Created on Jan 6, 2017

@author: stephenkoh
'''

import mingus.core.chords as chords
import mingus.core.keys as keys

#all_triads = []
print('TRIADS')
for i in range(len(keys.keys)):
    for elem in keys.keys[i]:
        print('\n%s' % elem)
        triads = chords.triads(elem)
        for triad in triads:
            typ = chords.determine(triad)
            for each in typ:
                print(each)
        
'''
all_triads = list(set(all_triads))
all_triads.sort()
print("\nTypes of triads naturally occurring:\n")
for elem in all_triads:
    print(elem)
'''

#all_sevenths = []
print('\nSEVENTHS:')
for i in range(len(keys.keys)):
    for elem in keys.keys[i]:
        print('\n%s' % elem)
        sevenths = chords.sevenths(elem)
        for seventh in sevenths:
            typ = chords.determine(seventh)
            for each in typ:
                print(each)
 
'''    
all_sevenths = list(set(all_sevenths))
all_sevenths.sort()
print("Types of sevenths naturally occurring:\n")
for elem in all_sevenths:
    print(elem)
'''