from __future__ import print_function

from mingus.containers.instrument import MidiInstrument
from mingus.midi.midi_file_in import MIDI_to_Composition
from mingus.midi.midi_file_out import write_Composition, write_Track,\
write_Bar, write_Note
from mingus.containers.composition import Composition
from mingus.containers.track import Track
from mingus.containers.bar import Bar
from mingus.containers.note_container import NoteContainer
from mingus.containers.note import Note
from mingus.core.intervals import measure
import sys
from math import floor
import warnings


'''Function sets the range and type of instrument.'''
def create_instrument(low, high):
    xylo = MidiInstrument()
    '''
    9 = 'Glockenspiel',
    11 = 'Vibraphone',
    12 = 'Marimba',
    13 = 'Xylophone'
    '''
    xylo.instrument_nr = 11
    xylo.set_range((low, high))
    xylo.name = 'ballophone'
    return xylo
    

'''Function prompts user for name of MIDI input or output file.'''
def get_name(kind, reserved = None):
    if (kind == 'in'):
        file = str(raw_input('Please enter the name of the MIDI to be used: '))
    elif (kind == 'out'): 
        # user prohibited from overwriting infile   
        file = str(raw_input('Please enter the name of the MIDI to be written: '))
        while (reserved == file):
            file = str(raw_input('You may not overwrite %s. Please enter a \
different name for the output MIDI: '))
    return file  


'''Function prints output from MIDI_to_Composition.'''
def print_midi(c, bpm):
    print(bpm)
    print(c, '\n')
        

'''Function writes rebuilt composition and playback events to location
specified by user and in a user-friendly format.'''
def write_log(c, bpm, filename, pb = None):
    # remove mid extension
    filename = filename[:-3]
    # add txt extension
    filename += 'txt'
    f = open(filename, 'w')
    f.write('BPM: ' + str(bpm) + '\n')
    for i in range(len(c)):
        f.write('TRACK %d\n' % i)
        for j in range(len(c[i])):
            f.write('\tBAR %d\n' % j)
            for lst in c[i][j]:
                f.write('\t\t' + str(lst) + '\n')
    if (pb != None): 
        print('--> Please refer to %s for output to be copied to Arduino \
program <--' % filename)
        f.write('\n\nPLAYBACK EVENTS:\n\n')
        f.write('%-20s%-20s\n' % ('time (ms):','lsa combo shorthand: '))
        for lst in pb:
            f.write('%-20s%-20s\n' % (str(lst[0]), str(lst[1])))
        f.write('\n\nCOPY THE BELOW OUTPUT TO \'pb\' IN \'stepMotors.c\':\n\n')
        f.write('{')
        for i in range(len(pb)):
            f.write(str(pb[i][0]) + ', \"' + str(pb[i][1]) + '\"')
            if (i < len(pb) - 1):
                f.write(',\n')
        f.write('}')


'''Wrapper function for is_good_track.'''
def select_tracks(c, bpm, xylo):
    for i in range(len(c)):
        if (is_good_track(c[i], bpm, xylo)):
            c.selected_tracks.append(i)
    return c.selected_tracks


'''Function prompts user whether or not a track should be included in 
what is played by the instrument. Function also acts as a wrapper for 
play_track_to_user.'''
def is_good_track(track, bpm, xylo):
    track.instrument = xylo
    play_track_to_user(track, bpm)
    '''
    query user to have them indicate whether or not track should be 
    included in what gets played by device:
    
    # query user until they give an acceptable response
    while (True):
        response = input('Should this track be included? (\'y\'/\'Y\' = \'yes\', \
        \'n\'/\'N\' = \'No\') )
        if (response == 'y' or response == 'Y'):
            return True
        elif (response == 'n' or response == 'N'):
            return False 
    '''
    pass


'''Function uses FluidSynth to play a portion of a single track to a user.'''
def play_track_to_user(track, bpm):
    # TODO: play track to user w/ FluidSynth, either a small portion
    # of it or allow user to exit out of playback 
    pass


'''Function uses FluidSynth to play a portion of the entire composition to a user.'''
def play_comp_to_user(c, bpm):
    # TODO: play c to user w/ FluidSynth, either a small portion
    # of it or allow user to exit out of playback
    pass
    

'''Function uses LilyPond to display the sheet music for the entire 
composition to a user.'''
def display_score_to_user(c):
    # TODO: display c to user w/ LilyPond
    pass


'''
Function creates a new composition object using an old one. The new one:
    1) only contains the tracks the user approved
    2) has each track's instrument set to 'xylo'
    3) has garbage notes filtered out
    4) has every note transposed within range of instrument     
'''
def rebuild_composition(old, xylo, cutoff):
    lowest = Note.__int__(Note('C', 8))
    highest = Note.__int__(Note('C', 0))
    new = Composition()
    for i in old.selected_tracks:
        t = Track()
        t.instrument = xylo
        for bar in old[i]:
            b = Bar()
            b.key.name = bar.key.name
            b.set_meter(bar.meter)
            # note value per beat == the denominator in time signature
            dem = b.meter[1]
            for lst in bar:
                value = lst[1]
                if (is_garbage(value, dem, cutoff)):
                    continue
                nc = NoteContainer()
                for note in lst[2]:
                    if (Note.__int__(note) < lowest): lowest = Note.__int__(note)
                    if (Note.__int__(note) > highest): highest = Note.__int__(note)
                    nc + note
                b.place_notes(nc, value)
            t.add_bar(b)
        new.add_track(t)
    # can't do the transposing until all notes in all tracks have been
    # compared against lowest and highest, which is why it is done here
    n1 = Note()
    n2 = Note()
    low = n1.from_int(lowest)
    high = n2.from_int(highest)
    # print("lowest and highest notes:", low, high)
    if (not xylo.notes_in_range([low, high])):
        new = transposer(new, lowest, highest, xylo)
    return new


'''Wrapper function for simple_filter.'''
def is_garbage(value, dem, cutoff):
    return simple_filter(value, dem, cutoff)


'''Function indicates whether a note's brevity falls below a user-
specified cutoff.'''
def simple_filter(value, dem, cutoff):
    # eliminating NoteContainers with really long 'value' (really brief)
    return floor(value/dem) > cutoff
    

'''Function does a better job at indicating whether a note should not 
be included in the rebuilt composition.'''
def better_filter():
    # TODO: filter out notes in a way that does not require supervision
    # e.g. user does not have to specify specific cases for which notes
    # should be removed 
    pass
    

'''Wrapper function for simple_transpose and better_transpose.'''
def transposer(c, lowest, highest, xylo):
    '''
    5 cases:
        1) lowest < xylo.range[0] and highest > xylo.range[1]
        2) lowest < xylo.range[0] and highest < xylo.range[0]
        3) lowest > xylo.range[1] and highest > xylo.range[1]
        4) lowest < xylo.range[0]
        5) highest > xylo.range[1]
        
    (1) definitely requires better_transpose
    (2) and (4) require better_transpose if highest + (xylo.range[0] - lowest) > xylo.range[1]
    (3) and (5) require better_transpose if lowest - (highest - xylo.range[1]) < xylo.range[0]  
    '''
    xylo_low = Note.__int__(xylo.range[0])
    xylo_high = Note.__int__(xylo.range[1])
    if (lowest < xylo_low and highest > xylo_high):
        c = better_transpose('foo', 'bar')
    
    elif (lowest < xylo_low):
        # minimum number of half steps to transpose by such that lowest
        # note in the entire composition is within the range of the 
        # instrument
        interval = xylo_low - lowest 
        if (highest + interval > xylo_high):
            c = better_transpose('foo', 'bar')
        else: 
            # whether you can transpose a full octave
            full = False
            if (highest + interval + 12 <= xylo_high): full = True
            c = simple_transpose(c, full, interval, up = True)
            
    elif (highest > xylo_high):
        interval = highest - xylo_high
        if (lowest - interval < xylo_low):
            c = better_transpose('foo', 'bar')
        else:
            full = False
            if (lowest - interval - 12 >= xylo_low): full = True
            c = simple_transpose(c, full, interval, up = False)
            
    return c    
        

'''Function transposes every track in the composition by a uniform amount.'''
def simple_transpose(c, full, interval, up):
    # determine whether can transpose by a full octave (only want to 
    # transpose to nearest octave)
    if (full):
        for i in range(len(c)):
            for j in range(len(c[i])):
                for k in range(len(c[i][j])):
                    for l in range(len(c[i][j][k][2])):
                        if (up):
                            c[i][j][k][2][l].octave_up()  
                        else:
                            c[i][j][k][2][l].octave_down()  
    
    else:
        for i in range(len(c)):
            c[i] = c[i].transpose(interval, up)
    
    # switch to the below else branch if the above else branch that 
    # makes use of track.transpose isn't working. the below is far more 
    # tedious, but it should work 
    '''
    else: 
        for i in range(len(c)):
            for j in range(len(c[i])):
                for k in range(len(c[i][j])):
                    for l in range(len(c[i][j][k][2])):
                        n = Note()
                        if (up):
                            c[i][j][k][2][l] = n.from_int(Note.__int__(c[i][j][k][2][l]) + interval) 
                        else:
                            c[i][j][k][2][l] = n.from_int(Note.__int__(c[i][j][k][2][l]) - interval) 
    '''
             
    return c
    

'''Function transposes tracks in the composition by different amounts.'''
def better_transpose(foo, bar):
    # TODO: transpose a composition that has notes falling outside
    # range of instrument regardless of what uniform shift is applied
    print('better_transpose required')
    sys.exit(0)


'''Function creates a MIDI file of the rebuild composition in the user-
specified location.'''
def write_comp(c, bpm, filename):
    write_Composition(filename, c, bpm)

'''Function converts seconds float to milliseconds integer.'''
def convert_to_ms(secs):
    return int(round((secs * 1000)))


'''Function creates a compact data structure representing the rebuilt
composition.'''
def create_playback_events(c, bpm, xylo, lsa_ordering):
    secs_in_min = 60.0
    # seconds per beat
    spb = secs_in_min / bpm 
    # dict of noteContainers containing time-noteContainer pairings
    times_dict = {}
    for track in c:
        cur_time = 0
        for bar in track:
            # beats per bar
            bpb = bar.meter[0]
            for lst in bar:
                time_into_bar = lst[0] * bpb * spb
                key = convert_to_ms(cur_time + time_into_bar) 
                if (key in times_dict):
                    times_dict[key] + lst[2]
                else:
                    times_dict[key] = lst[2]
            cur_time += bpb * spb
            
    # list of lists containing [time, lsa-combo (int)] 
    # list(set(noteContainer)) to remove repeated notes 
    pb = [ [key, notes_to_lsa_bin(list(set(times_dict[key])), xylo, \
                                  lsa_ordering)] for key in times_dict ]
    # sort on each sublist's first element (time)
    pb = sorted(pb, key=lambda x: x[0], reverse=False)
    validate_pb(pb, lsa_ordering, times_dict)
    return pb


'''Function creates an integer whose binary form represents the on/off
states of every LSA at a time when notes are being played.'''
def notes_to_lsa_bin(notes, xylo, lsa_ordering):
    # convert to int so that sharps of one note and flat of next mean 
    # the same thing
    keys = [ Note.__int__(Note(n)) for n in lsa_ordering ]
    vals = range(len(lsa_ordering))
    # first lsa's note mapped to 0, second lsa's note mapped to 1, ...
    lsa_dict = dict(zip(keys, vals))
    bnry = ['0'] * len(lsa_dict)
    for note in notes:
        # flip LSA to 'on' state for that note
        bnry[lsa_dict[Note.__int__(note)]] = '1'
    # so that number of leading zeros do not affect place of 'on' LSAs
    bnry.reverse()
    bnry = ''.join(bnry)
    # int whose binary represents the on and off states of all LSAs
    # at a given time
    combo = int(bnry, 2)
    return combo


'''Function checks whether the decoded integer represents the correct 
LSAs for every time when notes are played.'''
def validate_pb(pb, lsa_ordering, times_dict):
    for lst in pb:
        time = lst[0]
        lsa_code = lst[1]
        original = list(set(times_dict[time]))
        decoded = decode_lsas(lsa_code, lsa_ordering)
        if (not NoteContainer(original) == NoteContainer(decoded)):
            warnings.warn('incorrect LSA encoding at time = %.3f' % (time))
            

'''Function decodes which combination of notes are being played at a given
time.'''
def decode_lsas(lsa_code, lsa_ordering):
    bnry = [d for d in str(bin(lsa_code))[2:]]
    notes = []
    for i in range(len(bnry)):
        if (bnry[i] == '1'):
            notes.append(Note(lsa_ordering[(len(bnry) - 1) - i]))
    return notes


'''Wrapper function for sending playback events to the Arduino.'''
def send_to_Arduino(pb):
    # TODO: implement automated communication with Arduino
    pass


'''Function creates dictionary of lists of times at which notes are
played in the song. Function has no purpose other than to serve as 
an additional way for a user to see a song.'''
def create_dict(c, bpm):
    secs_in_min = 60.0
    # seconds per beat
    spb = secs_in_min / bpm 
    cur_time = 0
    notes_dict = {} 
    for i in range(len(c.selected_tracks)):
        for bar in c[i]:
            # beats per bar
            bpb = bar.meter[0]
            for lst in bar:
                time_into_bar = lst[0] * bpb * spb
                for note in lst[2]:
                    note = note.name + '-' + str(int(note.octave))
                    if note in notes_dict:
                        notes_dict[note].append(cur_time + time_into_bar)
                    else:
                        notes_dict[note] = [cur_time + time_into_bar]
            cur_time += bpb * spb
    return notes_dict


'''Function prints dictionary of lists of note-time pairings.'''
def print_dict(notes_dict):
    for key in notes_dict:
        print('%s: [' % key, end = "")
        for time in notes_dict[key]:
            print('%.2f, ' % time, end = "")
        print(']')


def main():
    # REPLACE WITH RELEVANT PATHS
    path_to_midi = '../../../Xylo/midis/' 
    path_to_log = '../../../Xylo/logs/'
    
    # F-3 to F-6 would be 37 keys. are we getting rid of 'F-3' or 'F-6'?
    low = Note('F-3')
    high = Note('F-6')
    xylo = create_instrument(low, high)
    
    infile = get_name('in') 
    c, bpm = MIDI_to_Composition(path_to_midi + infile)
    write_log(c, bpm, path_to_log + infile)
    
    # query user to select tracks we actually want from the midi
    # c.selected_tracks = select_tracks(c, bpm, xylo)
    
    # INSPECT LOG TO SEE WHICH TRACK NUMBERS YOU WANT INCLUDED AND 
    # PUT THEM INTO THE BELOW LIST
    c.selected_tracks = [1] # for mhall, only the track at index 1 is to be included
    
    # ratio of highest note value to keep in composition to beat unit.
    # e.g. if meter is 4/4, then a 'cutoff' of 2 would eliminate any
    # notes whose value exceeds 8 (anything briefer than an eighth note)
    cutoff = 2
    
    # composition containing only the selected tracks, the correct notes, 
    # with everything transposed w/in the range of the instrument
    c = rebuild_composition(c, xylo, cutoff)
    
    # check that everything sounds ok with selected tracks, removed notes,
    # and transposition 
    outfile = get_name('out', infile)
    write_Composition(path_to_midi + outfile, c, bpm)
    
    # TODO: replace with actual ordering once known. ordering by 
    # order of encounter from ball's perspective
    lsa_ordering = ['F-3', 'F#-3', 'G-3', 'G#-3', 'A-3', 'A#-3', 'B-3', 
                    'C-4', 'C#-4', 'D-4', 'D#-4', 'E-4', 'F-4', 'F#-4', 
                    'G-4', 'G#-4', 'A-4', 'A#-4', 'B-4', 'C-5', 'C#-5', 
                    'D-5', 'D#-5', 'E-5', 'F-5', 'F#-5', 'G-5', 'G#-5', 
                    'A-5', 'A#-5', 'B-5', 'C-6', 'C#-6', 'D-6', 'D#-6', 
                    'E-6', 'F-6']
    pb = create_playback_events(c, bpm, xylo, lsa_ordering)
    send_to_Arduino(pb)
    write_log(c, bpm, path_to_log + outfile, pb)
    
    play_comp_to_user(c, bpm)
    # optionally, display sheet music of the composition for further
    # diagnostics
    display_score_to_user(c)
    

if __name__ == "__main__": main()