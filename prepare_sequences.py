import pickle
import numpy as np

SEQUENCE_LENGTH = 100

with open('notes.pkl', 'rb') as f:
    notes = pickle.load(f)

pitches = sorted(set(notes))
n_vocab = len(pitches)
note_to_int = {note: number for number, note in enumerate(pitches)}
network_input = []
network_output = []
for i in range(len(notes) - SEQUENCE_LENGTH):
    seq_in = notes[i:i + SEQUENCE_LENGTH]
    seq_out = notes[i + SEQUENCE_LENGTH]
    network_input.append([note_to_int[n] for n in seq_in])
    network_output.append(note_to_int[seq_out])

n_patterns = len(network_input)
np.save('network_input.npy', np.array(network_input))
np.save('network_output.npy', np.array(network_output))
with open('note_to_int.pkl', 'wb') as f:
    pickle.dump(note_to_int, f)

print(f'Total sequences: {n_patterns}')
print(f'Vocabulary size: {n_vocab}')
print('Saved network_input.npy, network_output.npy, and note_to_int.pkl') 