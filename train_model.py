import numpy as np
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint

network_input = np.load('network_input.npy')
network_output = np.load('network_output.npy')
with open('note_to_int.pkl', 'rb') as f:
    note_to_int = pickle.load(f)

n_vocab = len(note_to_int)

network_input = np.reshape(network_input, (network_input.shape[0], network_input.shape[1], 1))
network_input = network_input / float(n_vocab)
network_output = to_categorical(network_output, num_classes=n_vocab)

model = Sequential()
model.add(LSTM(256, input_shape=(network_input.shape[1], network_input.shape[2]), return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(256))
model.add(Dropout(0.3))
model.add(Dense(128, activation='relu'))
model.add(Dense(n_vocab, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

print(model.summary())
checkpoint = ModelCheckpoint('model.h5', monitor='loss', verbose=1, save_best_only=True, mode='min')
model.fit(network_input, network_output, epochs=50, batch_size=64, callbacks=[checkpoint]) 