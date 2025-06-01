import os
import pickle
from music21 import converter, instrument, note, chord

midi_folder = 'midi_data'
notes = []

midi_files = [f for f in os.listdir(midi_folder) if f.lower().endswith('.mid') or f.lower().endswith('.midi')]

for midi_file in midi_files:
    midi_path = os.path.join(midi_folder, midi_file)
    try:
        midi = converter.parse(midi_path)
        parts = instrument.partitionByInstrument(midi)
        if parts:
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = midi.flat.notes
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
    except Exception as e:
        print(f'Error processing {midi_file}: {e}')

with open('notes.pkl', 'wb') as f:
    pickle.dump(notes, f)

print(f'Total notes/chords extracted: {len(notes)}')
print('Saved to notes.pkl') 