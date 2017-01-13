'''
Created on Jan 6, 2017

@author: stephenkoh
'''

import mingus.core.chords as chords

key = input('Please enter a key: ')
song = [lambda x: chords.I(x), lambda x: chords.IV(x), 
        lambda x: chords.V(x), lambda x: chords.I(x)]
for i in range(len(song)):
    print(chords.determine(song[i](key), True)[0])