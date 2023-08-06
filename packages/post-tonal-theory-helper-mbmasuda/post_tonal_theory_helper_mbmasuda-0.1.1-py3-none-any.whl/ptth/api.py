"""
Post-Tonal Theory Helper
api.py

Copyright (c) 2018-2019 by Mari Masuda <mbmasuda.github@gmail.com>,
all rights reserved.

This file contains some basic functions for post-tonal
music theory calculations.

Pitch classes are represented internally by numbers from 0-11.

0 = C
1 = C#
2 = D
3 = D#
4 = E
5 = F
6 = F#
7 = G
8 = G#
9 = A
10 = A#
11 = B

When supplying pitches to the below functions, either provide them
as a tuple, such as (11, 2, 8, 5, 10), or a string, with "t" for 
10 and "e" for 11, such as "e285t", as noted in the docstrings.

"""
import functools

from .forte_names import FORTE_NAMES


def normalize(pitch_class_string, de_dup=True, sort=True):
    """
    Normalizes a pitch class string by putting the pitch
    classes in ascending order and removing duplicates.
    Changes "T" and "t" into 10 and "E" and "e" into 11.
    
    Params:
        * pitch_class_string (string): a string representing
                                       a pitch class set.
        * sort (boolean): optional -- sort the pitches in
                          ascending order

    Returns:
        * a tuple of pitch classes in ascending order
    """
    if not isinstance(pitch_class_string, str):
        raise TypeError('must enter a string, such as "05T38"')
    
    if de_dup:
        pitches = list(set(pitch_class_string.lower()))
    else:
        pitches = list(pitch_class_string.lower())
        
    for pitch in pitches:
        if pitch not in ('0', '1', '2', '3', '4', '5', '6',
                         '7', '8', '9', 't', 'e'):
            raise ValueError('pitch class string must contain '
                             'only the numbers 0-9 and/or the '
                             'letters "T" or "t" and "E" or "e"')

    def _to_int(string):
        return_val = None
        try:
            return_val = int(string)
        except:
            if string.lower() == 't':
                return_val = 10
            elif string.lower() == 'e':
                return_val = 11
        return return_val

    pitches = [_to_int(p) for p in pitches]
    if sort:
        pitches.sort()
    return tuple(pitches)


def _tuple_to_string(tup):
    """
    Converts a tuple of pitches to a string

    Params:
        * tup (tuple): a tuple of pitch classes, like (11, 10, 5, 9, 3)

    Returns:
        * string: e.g., 'et593'
    """
    def _convert(pitch):
        pitch = mod_12(pitch)
        if pitch not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11):
            # should never happen
            raise ValueError('unexpected pitch found: %s' % pitch)
        
        if pitch == 10:
            return 't'
        elif pitch == 11:
            return 'e'
        else:
            return str(pitch)
    
    output = []
    for pitch in tup:
        output.append(_convert(pitch))
    return ''.join(output)



def normal_form(pitches):
    """
    Returns the normal form as a tuple of pitch classes.

    Params:
    *  tuple or string of pitches
    """
    if isinstance(pitches, tuple):
        pitches = _tuple_to_string(pitches)
        
    pitches = normalize(pitches)

    compare = []
    for i in range(0, len(pitches)):
        n = i + 1
        compare.append(rotate_pitches(pitches, n=n))
    return functools.reduce(get_most_packed_to_the_left, compare)


def prime_form(pitches):
    """
    Returns the prime form as a tuple of pitch classes.

    Params:
    *  tuple or string of pitches
    """
    normal = normal_form(pitches)
    l_to_r, r_to_l = get_intervals(normal)
    chord1 = make_chord_from_intervals(l_to_r)
    chord2 = make_chord_from_intervals(r_to_l)
    return get_most_packed_to_the_left(chord1, chord2)

    
def get_most_packed_to_the_left(chord1, chord2):
    """
    Returns the chord that is the most packed to the left.

    Most packed to the left means the ordering
    that has the smallest interval from first
    (lowest) to last (highest).  If there is a 
    tie, compare the intervals between the first
    and second-to-last notes.  If there is still
    a tie, compare the intervals between the
    first and third-to-last notes, and so on.
    If there is still a tie after all notes
    have been compared, choose the ordering
    beginning with the pitch class represented
    by the smallest integer.

    Params:
        * chord1 (tuple): a pitch class set
        * chord2 (tuple): a pitch class set

    Returns:
        * winner (tuple): a pitch class set
    """
    if len(chord1) != len(chord2):
        raise ValueError('the chords must have the same number of notes')

    def _get_most_packed_to_the_left_size_one(chord1, chord2):
        one = chord1[0]
        two = chord2[0]

        if not two < one:
            return chord1
        else:
            return chord2

    if len(chord1) == 1:
        return _get_most_packed_to_the_left_size_one(chord1, chord2)
        
    for i in range(len(chord1) - 1, 0, -1):
        diff1 = mod_12(chord1[i] - chord1[0])
        diff2 = mod_12(chord2[i] - chord2[0])

        if diff1 < diff2:
            return chord1
        elif diff2 < diff1:
            return chord2
        else:
            if i == 1:
                if chord1[0] < chord2[0]:
                    return chord1
                elif chord2[0] < chord1[0]:
                    return chord2
                else:
                    return _get_most_packed_to_the_left_size_one(chord1, chord2)


def get_intervals(chord, use_mod_12=False):
    """
    Returns two tuples containing the number of half-steps
    between each member of a chord when read from left
    to right and right to left.  Example: inputting chord 
    (1, 5, 6, 7) would return ((4, 1, 1), (1, 1, 4))

    Params:
        * use_mod_12 (boolean): default False, return
                                mod_12'ed intervals
                                instead of absolute
                                intervals
    """
    if len(chord) < 2:
        return (tuple(), tuple())

    intervals = []
    for i in range(1, len(chord)):
        intervals.append(chord[i] - chord[i - 1])
    reversed_intervals = intervals.copy()
    reversed_intervals.reverse()

    if not use_mod_12:
        return (tuple(intervals), tuple(reversed_intervals))

    return (tuple(map(mod_12, intervals)),
            tuple(map(mod_12, reversed_intervals)))
    

def make_chord_from_intervals(intervals, starting_pitch=0):
    """
    Returns a chord (tuple) constructed by starting on 
    starting_pitch and successively adding the intervals.

    Example: intervals = (4, 1, 1) and starting_pitch = 0
             result: (0, 4, 5, 6)

    Example 2: intervals = (1, 1, 4) and starting_pitch = 0
               result: (0, 1, 2, 6)
    """
    chord = [starting_pitch]
    index = 0
    for num_half_steps in intervals:
        chord.append(mod_12(chord[index] + num_half_steps))
        index += 1
    return tuple(chord)

    
def mod_12(any_int):
    """
    Returns the value of the input modulo 12

    Params:
        * any_int (int): any integer

    Returns:
        * the integer modulo 12
    """
    return any_int % 12


def rotate_pitches(chord, n=1):
    """
    Given a chord (tuple) of pitch classes, such as
    (1, 2, 3, 4), returns the next rotation of pitches,
    such as (2, 3, 4, 1), depending on what n is.

    Params:
        * chord (tuple): an ordered pitch class set
        * n (int): number of places to shift.  A positive
                   n means rotate left; a negative n means
                   rotate right.

    Returns:
        * chord (tuple): the pitches in a rotated order
    """
    if not chord:
        raise ValueError('must provide a chord')
    
    pitches = list(chord)
    n %= len(pitches)
    return tuple(pitches[n:] + pitches[:n])


def transpose(pitches, interval):
    """
    Returns the transposed tuple of pitch classes.
    
    Param:
        * pitches (tuple): the pitches
        * interval (int): the interval to transpose by
    """
    chord = list(pitches)
    chord = [mod_12(pitch + interval) for pitch in chord]
    return tuple(chord)


def invert(pitches, transpose=0):
    """
    Returns the inversion of the pitches followed by a
    transposition at an interval that defaults to 0.

    Param:
        * pitches (tuple): the pitches
        * transpose (int): the interval at which the
                           inverted pitches should
                           be transposed
    """
    pitches = list(pitches)
    pitches = [mod_12(12 - pitch + transpose) for pitch in pitches]
    return tuple(pitches)


def is_transpositionally_related(set1, set2):
    """
    Returns a tuple consisting of a boolean that tells
    if the two sets are transpositionally related, the
    transposition that maps set1 to set2, and the
    transposition that maps set2 to set1.  If the boolean
    is False, the transpositions are None.

    Params:
        * set1 (tuple or string): the pitches of the first set
        * set2 (tuple or string): the pitches of the second set
    """
    if isinstance(set1, tuple):
        set1 = _tuple_to_string(set1)

    if isinstance(set2, tuple):
        set2 = _tuple_to_string(set2)

    set1 = normalize(set1)
    set2 = normalize(set2)

    set1 = normal_form(set1)
    set2 = normal_form(set2)

    set1_intervals = get_intervals(set1, use_mod_12=True)
    set2_intervals = get_intervals(set2, use_mod_12=True)

    if set1_intervals != set2_intervals:
        return (False, None, None)

    # set2 = Tn(set1)
    # set1 = Tm(set2)
    set2_minus_set1 = [mod_12(x[1] - x[0]) for x in zip(set1, set2)]
    if float(sum(set2_minus_set1)) / float(len(set2_minus_set1)) \
       == float(set2_minus_set1[0]):
        # return (True, n, m)
        return (True, set2_minus_set1[0], mod_12(12 - set2_minus_set1[0]))
    else:
        return (False, None, None)
    

def is_inversionally_related(set1, set2):
    """
    Returns a tuple that tells whether the 2 sets are
    related by inversion, and if they are, also returns
    the index number.  If they are not related by inversion,
    the index number is None.

    Params:
        * set1 (tuple or string): the pitches in set1
        * set2 (tuple or string): the pitches in set2

    Returns:
        * tuple: (boolean, index) like (True, 5) or (False, None)
    """
    if isinstance(set1, tuple):
        set1 = _tuple_to_string(set1)

    if isinstance(set2, tuple):
        set2 = _tuple_to_string(set2)

    set1 = normalize(set1)
    set2 = normalize(set2)

    set1 = list(normal_form(set1))
    set2 = list(normal_form(set2))

    set2.reverse()

    potential_index = [mod_12(sum(x)) for x in zip(set1, set2)]
    if float(sum(potential_index)) / float(len(potential_index)) \
       == float(potential_index[0]):
        return (True, potential_index[0])
    return (False, None)


def get_set_class_members(pitches):
    """
    Returns a list of tuples that includes
    all members of the set class.

    Params:
        * pitches (tuple or string): the pitches
    """
    if isinstance(pitches, tuple):
        pitches = _tuple_to_string(pitches)

    pitches = normalize(pitches)

    normal = normal_form(pitches)

    output = []
    for i in range(0, 12):
        output.append(rotate_pitches(normal, i))

    inverted = invert(normal)
    for i in range(0, 12):
        output.append(rotate_pitches(inverted, i))

    return output


def get_forte_name(pitches):
    """
    Returns the Forte name of the pitch class set

    Params:
        * pitches (tuple or string): the pitches
    """
    prime = prime_form(pitches)
    pitch_string = _tuple_to_string(prime)
    pitch_string = pitch_string.upper()
    return FORTE_NAMES.get(pitch_string,
                           'An error occurred and the Forte name '
                           'for {} could not be found'.format(pitch_string))
