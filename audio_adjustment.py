import numpy as np

def adjust_audio_volume(events, audio_signal, sr):
    """
    Dynamically adjusts the volume of an audio track based on recognized events.
    """
    adjusted_signal = np.copy(audio_signal).astype(np.float32)

    for event in events:
        # Ensure valid indices
        time = int(event["time"] * sr)
        end_time = min(time + 5000, len(adjusted_signal))  # Avoid out-of-bounds access

        if event["type"] == "applause":
            adjusted_signal[time:end_time] *= 1.2  # Increase volume for applause
        elif event["type"] == "whistle":
            adjusted_signal[time:end_time] *= 0.8  # Decrease volume for whistle

        # Clip values to prevent overflow
        adjusted_signal = np.clip(adjusted_signal, -1.0, 1.0)

    return adjusted_signal

