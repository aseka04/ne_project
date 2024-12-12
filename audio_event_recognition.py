import torch
import torch.nn as nn
import librosa
import numpy as np
import os

# Define the model architecture to match the saved state dictionary
class AudioEventModel(nn.Module):
    def __init__(self):
        super(AudioEventModel, self).__init__()
        self.fc1 = nn.Linear(40, 128)  # First fully connected layer
        self.relu = nn.ReLU()          # Activation function
        self.fc2 = nn.Linear(128, 2)   # Output layer with 2 classes (adjust if needed)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


# Load the model and state dictionary
MODEL_PATH = os.path.join("models", "audio_event_model.pth")

# Initialize the model and load the state dictionary
audio_event_model = AudioEventModel()
try:
    audio_event_model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    audio_event_model.eval()  # Set the model to evaluation mode
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")


def extract_features(audio_path):
    """
    Extract MFCC features from the given audio file.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        np.ndarray: MFCC features.
    """
    try:
        # Load the audio file
        y, sr = librosa.load(audio_path, sr=16000)
        # Extract MFCC features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        return mfccs
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None


def recognize_audio_events(audio_path):
    """
    Recognizes key audio events (e.g., applause, whistles) from an audio file.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        list[dict]: Detected audio events with their timestamps.
    """
    features = extract_features(audio_path)
    if features is None:
        return []

    events = []

    # Loop through the features and predict audio events
    for i in range(features.shape[1]):
        feature = torch.tensor(features[:, i], dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            output = audio_event_model(feature)
            predicted_class = torch.argmax(output, dim=1).item()

        # Map predicted class indices to event names (adjust this mapping if needed)
        event_mapping = {0: "none", 1: "applause"}
        event = event_mapping.get(predicted_class, "none")

        if event != "none":
            timestamp = i * (512 / 16000)  # Assuming hop length of 512 and sample rate of 16000
            events.append({"time": timestamp, "type": event})

    return events


if __name__ == "__main__":
    # Example usage
    AUDIO_FILE_PATH = "data/test_video.wav"  # Replace with your actual audio file path

    if os.path.exists(AUDIO_FILE_PATH):
        print("Analyzing audio events...")
        detected_events = recognize_audio_events(AUDIO_FILE_PATH)
        for event in detected_events:
            print(f"Detected {event['type']} at {event['time']:.2f} seconds")
    else:
        print(f"Audio file not found at: {AUDIO_FILE_PATH}")
