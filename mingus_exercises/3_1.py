'''
Created on Jan 6, 2017

@author: stephenkoh
'''

import mingus.core.notes as notes
import mingus.core.intervals as intervals

note = "C"
third_b = intervals.minor_third(note)
third_b_int = notes.note_to_int(third_b)
print("minor third: ", third_b, third_b_int)
third = intervals.major_third(note)
third_int = notes.note_to_int(third)
print("major third: ", third, third_int)
fourth_b = intervals.minor_fourth(note)
fourth_b_int = notes.note_to_int(fourth_b)
print("minor fourth: ", fourth_b, fourth_b_int)
fourth = intervals.major_fourth(note)
fourth_int = notes.note_to_int(fourth)
print("major fourth: ", fourth, fourth_int)