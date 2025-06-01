import numpy as np
import pickle
import random
from tensorflow.keras.models import load_model
from music21 import instrument, note, chord, stream

SEQUENCE_LENGTH = 100
GENERATE_LENGTH = 200

network_input = np.load('network_input.npy')
with open('note_to_int.pkl', 'rb') as f:
    note_to_int = pickle.load(f)
int_to_note = {number: note for note, number in note_to_int.items()}
n_vocab = len(note_to_int)

model = load_model('model.h5')

start = np.random.randint(0, len(network_input)-1)
pattern = network_input[start]
pattern = pattern.tolist()
generated_notes = []
for _ in range(GENERATE_LENGTH):
    input_seq = np.reshape(pattern, (1, SEQUENCE_LENGTH, 1))
    input_seq = input_seq / float(n_vocab)
    prediction = model.predict(input_seq, verbose=0)
    index = np.argmax(prediction)
    result = int_to_note[index]
    generated_notes.append(result)
    pattern.append(index)
    pattern = pattern[1:]

output_notes = []
for item in generated_notes:
    
    if ('.' in item) or item.isdigit():
        notes_in_chord = item.split('.')
        notes_objs = []
        for n in notes_in_chord:
            try:
                n_int = int(n)
                notes_objs.append(note.Note(n_int))
            except:
                notes_objs.append(note.Note(n))
        new_chord = chord.Chord(notes_objs)
        output_notes.append(new_chord)
    else:
        output_notes.append(note.Note(item))

midi_stream = stream.Stream(output_notes)
midi_stream.insert(0, instrument.Piano())
midi_stream.write('midi', fp='output.mid')

print('Generated music saved as output.mid') 