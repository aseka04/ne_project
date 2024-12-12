import random

import cv2

from text_module.comment_generator import generate_comment
from vision_module.game_event_recognition import analyze_game_video

from sound_module.audio_event_recognition import recognize_audio_events
from sound_module.audio_adjustment import adjust_audio_volume
import librosa
import soundfile as sf

def detect_game_events(video_path, output_path):
    """
    Detects game events from video using player detection and overlays comments.
    """
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    frame_count = 0
    detected_events = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Simulate player detection event (replace with real detection logic)
        if frame_count % 150 == 0:
            event_type = random.choice(["goal", "penalty", "assist", "whistle", "applause"])
            event = {"type": event_type, "frame": frame_count}
            detected_events.append(event)
            comment = generate_comment(event)

            # Overlay comment on the frame
            cv2.putText(frame, comment, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        out.write(frame)

    cap.release()
    out.release()
    return detected_events

def main():
    print("Starting the Sports Broadcasting System...")

    # Paths to input and output files
    video_path = "data/test_video.mp4"
    audio_path = "data/test_video.wav"
    output_video_path = "data/annotated_game_video.mp4"
    output_audio_path = "data/adjusted_audio.wav"

    # Detect game events and overlay comments
    print("Detecting game events from video and generating commentary...")
    game_events = detect_game_events(video_path, output_video_path)

    # Recognize audio events
    print("Recognizing audio events from the audio file...")
    audio_events = recognize_audio_events(audio_path)

    # Adjust the audio track based on events
    print("Adjusting audio volume based on recognized events...")
    y, sr = librosa.load(audio_path, sr=16000)
    adjusted_audio = adjust_audio_volume(audio_events, y, sr)

    # Save adjusted audio
    sf.write(output_audio_path, adjusted_audio, sr)
    print(f"Adjusted audio saved to {output_audio_path}")

    # Generate comments for game events
    print("Generating comments for the game events...")
    for event in game_events:
        if 'type' in event:
            comment = generate_comment(event)
            print(f"Event: {event['type']}, Comment: {comment}")
        else:
            print("Event has no 'type' key. Skipping comment.")

    print("Process completed. Check the output video with commentary and adjusted audio!")

if __name__ == "__main__":
    main()



