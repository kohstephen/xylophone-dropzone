'''
Created on Jan 6, 2017

@author: stephenkoh
'''

import mingus.core.keys as keys
import mingus.core.notes as notes

while(True):
    key = str(input('Please enter a key: '))
    keyz = keys.get_notes(key)
    #print(keys)
    for i in range(len(keyz)):
        keyz[i] = notes.augment(keyz[i])
    print(keyz)