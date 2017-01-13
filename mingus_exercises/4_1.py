'''
Created on Jan 6, 2017

@author: stephenkoh
'''

import mingus.core.chords as chords

key = str(input('Please enter a key: '))
triads = chords.triads(key)
print('\nTriads shorthand:')
for elem in triads:
    print(chords.determine(elem, True)[0])
sevenths = chords.sevenths(key)
print('\nSevenths shorthand:')
for elem in sevenths:
    print(chords.determine(elem, True)[0])
