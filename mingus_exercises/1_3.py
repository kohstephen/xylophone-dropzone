'''
Created on Jan 5, 2017

@author: stephenkoh
'''

import mingus.core.notes as notes

fibs = [1, 1]
for i in range(2, 1000):
    fibs.append(fibs[i - 2] + fibs[i - 1])
fib_notes = []
for n in fibs:
    fib_notes.append(notes.int_to_note(n % 12))
print(fibs)
print(len(fibs))
print(fib_notes)
print(len(fib_notes))