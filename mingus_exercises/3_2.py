'''
Created on Jan 6, 2017

@author: stephenkoh
'''

import mingus.core.intervals as intervals

key = str(input('Please enter a key: '))
note = str(input('Please enter a note: '))
third = intervals.third(note, key)
fifth = intervals.fifth(note, key)
print(note, third, fifth)
