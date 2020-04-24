# DeepSpeech-Neural-Network-Recognition
Developed an end-to-end automatic speech recognition (ASR) pipeline Machine Translation System which takes user voice as input and converts the input into a an english Sentence of 2 primary Machine Learning Models using Keras Framework
The first model is the acoustic model developed using a Bidirectional RNN + TimeDistributed Dense with 
Mel-Frequency Cepstral Coefficients (MFCCs) as the audio feature representation.
The dataset used for training was LibriSpeech containing 1000 hours of speech derived from English audiobooks.
The second is a language model that helps convert phenmes to words . 
