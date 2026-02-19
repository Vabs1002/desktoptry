import tensorflow as tf
from tensorflow.keras import layers, models
import os
import numpy as np

def train_cnn_model():
    data_dir = "data/"
    gestures = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    X, y = [], []
    
    for idx, name in enumerate(gestures):
        path = os.path.join(data_dir, name)
        files = os.listdir(path)
        for file in files[:500]: # Ensure exactly 500
            X.append(np.load(os.path.join(path, file)))
            y.append(idx)

    X, y = np.array(X), np.array(y)

    model = models.Sequential([
        layers.Input(shape=(63,)),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(128, activation='relu'),
        layers.Dense(len(gestures), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X, y, epochs=40, batch_size=32, shuffle=True)
    
    os.makedirs("models", exist_ok=True)
    model.save("models/gesture_model.h5")
    np.save("models/labels.npy", np.array(gestures))
    return "CNN Trained on 15 Gestures"