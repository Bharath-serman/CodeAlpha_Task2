import os
from music21 import converter, instrument, note, chord

midi_folder = 'midi_data'  

midi_files = [f for f in os.listdir(midi_folder) if f.lower().endswith('.mid') or f.lower().endswith('.midi')]

for midi_file in midi_files:
    print(f'\nProcessing: {midi_file}')
    midi_path = os.path.join(midi_folder, midi_file)
    try:
        midi = converter.parse(midi_path)
        notes_to_parse = None
        parts = instrument.partitionByInstrument(midi)
        if parts:  
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = midi.flat.notes
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                print(f'Note: {element.pitch}')
            elif isinstance(element, chord.Chord):
                print(f'Chord: {".".join(str(n) for n in element.normalOrder)}')
    except Exception as e:
        print(f'Error processing {midi_file}: {e}') 