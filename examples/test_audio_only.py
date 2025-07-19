#!/usr/bin/env python3
"""
Simple Audio Test Script

This script tests audio input and output separately to help isolate audio issues.
"""

import pyaudio
import time
import numpy as np

SAMPLE_RATE = 44100  # Changed from 16000 to 44100


def test_audio_devices():
    """Test all audio devices"""
    print("🎤 Testing Audio Devices")
    print("=" * 40)

    try:
        pa = pyaudio.PyAudio()

        print(f"Found {pa.get_device_count()} audio devices:")
        print()

        # List all devices
        for i in range(pa.get_device_count()):
            try:
                device_info = pa.get_device_info_by_index(i)
                print(f"Device {i}: {device_info['name']}")
                print(f"  - Input channels: {device_info['maxInputChannels']}")
                print(f"  - Output channels: {device_info['maxOutputChannels']}")
                print(f"  - Sample rate: {device_info['defaultSampleRate']}")
                print()
            except Exception as e:
                print(f"Device {i}: Error reading info - {e}")
                print()

        pa.terminate()
        return True
    except Exception as e:
        print(f"Error initializing PyAudio: {e}")
        return False


def test_audio_input(device_id=None):
    """Test audio input"""
    print("🎤 Testing Audio Input")
    print("=" * 40)

    try:
        pa = pyaudio.PyAudio()

        if device_id is None:
            # Find first working input device
            for i in range(pa.get_device_count()):
                try:
                    device_info = pa.get_device_info_by_index(i)
                    if device_info["maxInputChannels"] > 0:
                        device_id = i
                        break
                except:
                    continue

        if device_id is None:
            print("❌ No input devices found")
            pa.terminate()
            return False

        print(f"Testing input device {device_id}")

        # Try to open the stream
        stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=SAMPLE_RATE,
            input=True,
            input_device_index=device_id,
            frames_per_buffer=1024,
        )

        print("✅ Audio input stream opened successfully")
        print("Recording for 3 seconds... (speak into your microphone)")

        # Record for 3 seconds
        frames = []
        for i in range(0, int(SAMPLE_RATE / 1024 * 3)):
            try:
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(data)
            except Exception as e:
                print(f"Error reading audio: {e}")
                break

        stream.stop_stream()
        stream.close()
        pa.terminate()

        if frames:
            print(f"✅ Successfully recorded {len(frames)} audio frames")
            # Calculate audio level
            audio_data = np.frombuffer(b"".join(frames), dtype=np.int16)
            level = np.sqrt(np.mean(audio_data**2))
            print(f"Audio level: {level:.2f}")
            if level > 100:
                print("✅ Audio input is working (detected sound)")
            else:
                print(
                    "⚠️  Audio input working but no sound detected (check microphone)"
                )
        else:
            print("❌ No audio frames recorded")
            return False

        return True
    except Exception as e:
        print(f"❌ Audio input test failed: {e}")
        return False


def test_audio_output(device_id=None):
    """Test audio output"""
    print("\n🔊 Testing Audio Output")
    print("=" * 40)

    try:
        pa = pyaudio.PyAudio()

        if device_id is None:
            # Find first working output device
            for i in range(pa.get_device_count()):
                try:
                    device_info = pa.get_device_info_by_index(i)
                    if device_info["maxOutputChannels"] > 0:
                        device_id = i
                        break
                except:
                    continue

        if device_id is None:
            print("❌ No output devices found")
            pa.terminate()
            return False

        print(f"Testing output device {device_id}")

        # Try to open the stream
        stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=SAMPLE_RATE,
            output=True,
            output_device_index=device_id,
            frames_per_buffer=1024,
        )

        print("✅ Audio output stream opened successfully")
        print("Playing test tone for 2 seconds...")

        # Generate a test tone (440 Hz sine wave)
        sample_rate = SAMPLE_RATE
        duration = 2
        frequency = 440

        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = np.sin(2 * np.pi * frequency * t) * 0.3
        audio_data = (tone * 32767).astype(np.int16)

        # Play the tone
        try:
            stream.write(audio_data.tobytes())
            print("✅ Test tone played successfully")
        except Exception as e:
            print(f"Error playing audio: {e}")
            stream.close()
            pa.terminate()
            return False

        stream.stop_stream()
        stream.close()
        pa.terminate()

        return True
    except Exception as e:
        print(f"❌ Audio output test failed: {e}")
        return False


def main():
    print("🎵 Audio Test Tool")
    print("=" * 40)

    # Test device enumeration
    if not test_audio_devices():
        print("❌ Failed to enumerate audio devices")
        return

    # Test audio input
    if not test_audio_input():
        print("❌ Audio input test failed")
        return

    # Test audio output
    if not test_audio_output():
        print("❌ Audio output test failed")
        return

    print("\n" + "=" * 40)
    print("🎉 All audio tests passed!")
    print("💡 Your audio system should work with the video chat application.")


if __name__ == "__main__":
    main()
