import wave
import math

def extract_melody_frequencies(wav_file_path, time_interval=0.1):
    """Extracts melody frequencies from a WAV file at given time intervals."""

    with wave.open(wav_file_path, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        audio_data = wav_file.readframes(num_frames)

    # Convert audio data to list of integers
    signal = [int.from_bytes(audio_data[i:i+2], byteorder='little', signed=True) 
              for i in range(0, len(audio_data), 2)]  # 2 bytes per sample

    hop_length = int(sample_rate * time_interval)  # Samples per interval
    frequencies = []

    # MIDI note to frequency lookup table (A4 = 440 Hz)
    note_freqs = {n: 440 * 2 ** ((n - 69) / 12) for n in range(128)}

    for i in range(0, num_frames, hop_length):
        segment = signal[i:i + hop_length]

        # Zero-crossing rate for frequency estimation
        zero_crossings = sum(1 for j in range(1, len(segment)) if segment[j-1] * segment[j] < 0)
        zero_crossing_rate = zero_crossings / (2 * time_interval)
        estimated_frequency = zero_crossing_rate / 2 

        # Check for zero frequency to avoid math domain error
        if estimated_frequency > 0: 
            note_number = 12 * math.log2(estimated_frequency / 440) + 69
            if note_number >= 0 and note_number < 128:
                note_name = note_name_from_number(round(note_number))
            else:
                note_name = "Out of Range"  # Indicate note is outside standard range
        else:
            note_name = "No Note"  # No significant frequency detected

        frequencies.append((estimated_frequency, note_name))

    return frequencies
def note_name_from_number(note_number):
    """Approximates the note name from a MIDI note number."""
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = note_number // 12 - 1
    note_idx = note_number % 12
    return notes[note_idx] + str(octave)

# Example usage:
wav_file_path = "nyancat.wav"
time_interval = 0.1  # Seconds
frequencies = extract_melody_frequencies(wav_file_path, time_interval)
print(frequencies)
