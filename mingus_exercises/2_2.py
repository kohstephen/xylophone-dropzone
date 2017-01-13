'''
Created on Jan 6, 2017

@author: stephenkoh
'''

import mingus.core.keys as keys
import mingus.core.notes as notes
#import mingus.core.intervals as intervals

for i in range(len(keys.keys)):
    key = keys.keys[i][0]
    note_int = notes.note_to_int(key)
    note1 = keys.int_to_note(note_int, key)
    note2 = notes.int_to_note(note_int)
    #if (intervals.measure(note1, note2) == 0):
    if (note1 != note2):
        print('Using notes.int_to_note: %s\n\
Using keys.int_to_note: %s\n\
Number: %d\nKey: %s\n' % (note1, note2, note_int, key))