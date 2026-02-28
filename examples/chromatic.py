# -*- coding: utf-8 -*-
"""
Convert a note pitch like A#4 to its frequency
"""

def name(pitch_class: str, octave: int) -> str:
    """Generate a unique pitch for a note based on its pitch class in the chromatic scale and the octave it's in.
    """
    return f"{pitch_class}{octave}"


#  Spellings (names) for the twelve pitch classes in the Chromatic Octave
CHROMATIC_OCTAVE = "C,C#,D,D#,E,F,F#,G,G#,A,A#,B".split(',')


# Octaves we'll consider
OCTAVES = range(8)

PITCH_CLASS_NAMES = [name(pitch_class, octave) for octave in OCTAVES for pitch_class in CHROMATIC_OCTAVE]
"""The names of the notes we'll consider: C0, C#0 and so on up to B8
"""

"""
The ratio between the frequency of a note and frequency of the semitone above it.

Frequency doubles in an octave, and there are twelve notes in an octave,
so the ratio is the twelfth root of two.
"""
SEMITONE_FACTOR = 2 ** (1 / 12.0)


def tone_for(i: int) -> int:
    """Convert an index in the list of notes to its frequency"""
    return round(440 * SEMITONE_FACTOR ** (i - 57))


# A map from pitch to frequency
NOTE_FREQUENCIES = dict([(name, tone_for(i)) for i, name in enumerate(PITCH_CLASS_NAMES)])

"""
Add entries for enharmonics.
 
Notes are enharmonics if they are notes with the same frequency but with different names.
"""

for octave in OCTAVES:
    for (first, second) in [("C#", "D♭"), ("D#", "E♭"), ("F#", "G♭"), ("G#", "A♭"), ("A#", "B♭")]:
        NOTE_FREQUENCIES[name(second, octave)] = NOTE_FREQUENCIES[name(first, octave)]


# convert a note pitch to its frequency
def frequency_for_note(name: str) -> int:
    if 'S' in name:
        name = name.replace('S','#')
    return -1 if name not in NOTE_FREQUENCIES else NOTE_FREQUENCIES[name]