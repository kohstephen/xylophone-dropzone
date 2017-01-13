'''
Created on Jan 6, 2017

@author: stephenkoh
'''

import mingus.core.notes as notes

note = str(input('Please enter a note: '))
if (notes.is_valid_note(note)):
    note = notes.to_minor(note)
    note = notes.diminish(note)
    print(note)