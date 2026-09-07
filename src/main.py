import sys
import os
import keyboard
try:
    from voice import listen_for_wakeword, record_user_speech, transcribe_audio
    from speech import speak
    from assistant import process_user_request
except ModuleNotFoundError:
    from src.voice import listen_for_wakeword, record_user_speech, transcribe_audio
    from src.speech import speak
    from src.assistant import process_user_request

print("\n=======================================================")
print("            STARK VOICE SYSTEM INITIALIZED            ")
print("=======================================================")
print("Say 'Hey Jarvis' once to start. Stark will keep listening for 10s.")
print("Say 'exit' OR press [ESC] anytime to stop.\n")

speak("Systems active.")

in_conversation = False

while True:
    try:
        if keyboard.is_pressed('esc'):
            print("\n[System]: ESC key detected. Shutting down...")
            speak("Goodbye.")
            os._exit(0)

        if not in_conversation:
            if listen_for_wakeword():
                in_conversation = True

        raw_speech = record_user_speech()
        user_input = transcribe_audio(raw_speech) if raw_speech is not None else ""

        if keyboard.is_pressed('esc'):
            print("\n[System]: ESC key detected. Shutting down...")
            speak("Goodbye.")
            os._exit(0)

        if not user_input:
            print("[System]: 10s timeout reached. Returning to idle mode...")
            in_conversation = False
            continue

        print(f"\nYou: {user_input}")
        clean_input = user_input.lower().strip()

        if clean_input in ["exit", "quit", "bye", "stop"]:
            farewell = "Shutting down systems. Goodbye."
            print(f"\nStark: {farewell}")
            speak(farewell)
            print("\nDisconnecting...")
            os._exit(0)

        response = process_user_request(user_input)
        if response:
            print(f"Stark: {response}\n")
            speak(response)

    except KeyboardInterrupt:
        print("\nDisconnecting...")
        os._exit(0)
    except Exception as e:
        print(f"[System Error]: {e}")
