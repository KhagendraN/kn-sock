#!/usr/bin/env python3
"""
Video Chat Diagnostic Tool

This script helps diagnose common issues with video and audio devices
before running the video chat application.
"""

import cv2
import pyaudio
import os
import sys

def check_display():
    """Check if display is working properly"""
    print("🔍 Checking display setup...")
    
    # Set display backend
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    
    try:
        # Try to create a simple window
        cv2.namedWindow('Test Window', cv2.WINDOW_NORMAL)
        test_frame = cv2.imread('/dev/null')  # This will be None, but we just want to test the window creation
        cv2.destroyAllWindows()
        print("✅ Display setup looks good!")
        return True
    except Exception as e:
        print(f"❌ Display error: {e}")
        print("💡 Try setting: export QT_QPA_PLATFORM=xcb")
        return False

def check_video():
    """Check if camera is available"""
    print("\n📹 Checking camera...")
    
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Could not open camera (device 0)")
            print("💡 Make sure your camera is connected and not in use by another application")
            return False
        
        ret, frame = cap.read()
        if not ret:
            print("❌ Could not read frame from camera")
            cap.release()
            return False
        
        print(f"✅ Camera working! Frame size: {frame.shape}")
        cap.release()
        return True
    except Exception as e:
        print(f"❌ Camera error: {e}")
        return False

def check_audio():
    """Check if audio devices are available"""
    print("\n🎤 Checking audio devices...")
    
    try:
        pa = pyaudio.PyAudio()
        
        # Check input devices
        input_devices = []
        for i in range(pa.get_device_count()):
            device_info = pa.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append((i, device_info['name']))
        
        if input_devices:
            print(f"✅ Found {len(input_devices)} audio input device(s):")
            for device_id, name in input_devices:
                print(f"   - Device {device_id}: {name}")
        else:
            print("❌ No audio input devices found")
            print("💡 Make sure your microphone is connected")
            pa.terminate()
            return False
        
        # Check output devices
        output_devices = []
        for i in range(pa.get_device_count()):
            device_info = pa.get_device_info_by_index(i)
            if device_info['maxOutputChannels'] > 0:
                output_devices.append((i, device_info['name']))
        
        if output_devices:
            print(f"✅ Found {len(output_devices)} audio output device(s):")
            for device_id, name in output_devices:
                print(f"   - Device {device_id}: {name}")
        else:
            print("❌ No audio output devices found")
            print("💡 Make sure your speakers/headphones are connected")
            pa.terminate()
            return False
        
        pa.terminate()
        return True
    except Exception as e:
        print(f"❌ Audio error: {e}")
        print("💡 Try installing: sudo pacman -S pulseaudio pulseaudio-alsa")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    try:
        import cv2
        print("✅ OpenCV installed")
    except ImportError:
        print("❌ OpenCV not installed")
        print("💡 Install with: pip install opencv-python")
        return False
    
    try:
        import pyaudio
        print("✅ PyAudio installed")
    except ImportError:
        print("❌ PyAudio not installed")
        print("💡 Install with: pip install pyaudio")
        return False
    
    try:
        import numpy
        print("✅ NumPy installed")
    except ImportError:
        print("❌ NumPy not installed")
        print("💡 Install with: pip install numpy")
        return False
    
    return True

def main():
    print("🎥 Video Chat Diagnostic Tool")
    print("=" * 40)
    
    all_good = True
    
    # Check dependencies
    if not check_dependencies():
        all_good = False
    
    # Check display
    if not check_display():
        all_good = False
    
    # Check video
    if not check_video():
        all_good = False
    
    # Check audio
    if not check_audio():
        all_good = False
    
    print("\n" + "=" * 40)
    if all_good:
        print("🎉 All checks passed! Your system is ready for video chat.")
        print("💡 You can now run: python examples/video_chat_client.py <server_ip> <room> <nickname>")
    else:
        print("⚠️  Some issues were found. Please fix them before running video chat.")
        print("💡 Common solutions:")
        print("   - Install missing packages: pip install opencv-python pyaudio numpy")
        print("   - Set display backend: export QT_QPA_PLATFORM=xcb")
        print("   - Install audio drivers: sudo pacman -S pulseaudio pulseaudio-alsa")
        print("   - Check camera permissions and connections")

if __name__ == "__main__":
    main() 