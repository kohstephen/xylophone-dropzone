'''
Created on Jan 5, 2017

@author: stephenkoh
'''


import mingus.core.notes as notes

note = str(input("Please enter a note: "))
if (notes.is_valid_note(note)):
    for i in range(4):
        note = notes.augment(note)
note_int = notes.note_to_int(note)
note = notes.int_to_note(note_int)
print(note)
