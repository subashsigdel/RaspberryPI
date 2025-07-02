import cv2
import requests
import base64
import time
import threading
from picamera2 import Picamera2
from SpeechToText import TTS  # Ensure TTS works correctly

# === Configuration ===
SERVER_URL = "http://localhost:8080/v1/chat/completions"
INSTRUCTION = "What do you see?"
INTERVAL_SECONDS = 5  # Time between photo captures

# === Camera Setup ===
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()
time.sleep(1)  # Warm-up time

# === Global States ===
last_request_time = 0
processing = False
speaking = False
status_message = "Idle"

# === TTS speak function ===
def speak_response(text):
    global speaking, status_message
    try:
        speaking = True
        status_message = "Speaking..."
        TTS(text=text, lang='en', filename='temp_output.mp3')  # Blocks until done
    except Exception as e:
        print("TTS failed:", e)
    finally:
        speaking = False
        status_message = "Idle"

# === Send image to VLM server ===
def process_frame(frame):
    global processing, status_message
    processing = True
    status_message = "Encoding image..."

    try:
        _, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        image_base64 = base64.b64encode(jpeg.tobytes()).decode('utf-8')
        image_data_url = f"data:image/jpeg;base64,{image_base64}"
    except Exception as e:
        print("Encoding failed:", e)
        status_message = "Idle"
        processing = False
        return

    payload = {
        "max_tokens": 100,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": INSTRUCTION},
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                ]
            }
        ]
    }

    try:
        status_message = "Sending to API..."
        response = requests.post(SERVER_URL, headers={"Content-Type": "application/json"}, json=payload)

        if response.ok:
            answer = response.json()["choices"][0]["message"]["content"]
            print("Response:", answer)
            tts_thread = threading.Thread(target=speak_response, args=(answer,), daemon=True)
            tts_thread.start()
        else:
            print(f"API error {response.status_code}: {response.text}")
            status_message = "API Error"
    except Exception as e:
        print("Request failed:", e)
        status_message = "Request failed"

    processing = False

# === Main Loop ===
print("[INFO] Press 'q' to quit.")
try:
    while True:
        frame = picam2.capture_array()

        # Status display
        cv2.putText(frame, f"Status: {status_message}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("SmolVLM Pi", frame)

        current_time = time.time()
        should_capture = (current_time - last_request_time >= INTERVAL_SECONDS and not processing and not speaking)

        if should_capture:
            last_request_time = current_time

            for msg in ["Be ready...", "3", "2", "1"]:
                frame = picam2.capture_array()
                font_scale = 1.5 if msg == "Be ready..." else 4.0
                thickness = 2 if msg == "Be ready..." else 5
                cv2.putText(frame, msg, (100, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), thickness)
                cv2.imshow("SmolVLM Pi", frame)
                cv2.waitKey(1000)

            print("[INFO] Capturing image for analysis...")

            for _ in range(5):
                picam2.capture_array()
                time.sleep(0.05)

            final_frame = picam2.capture_array()
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"captured_{timestamp}.jpg"
            cv2.imwrite(filename, final_frame)
            print(f"[INFO] Saved image: {filename}")

            threading.Thread(target=process_frame, args=(final_frame.copy(),), daemon=True).start()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n[INFO] Interrupted by user.")

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    print("[INFO] Camera stopped. Exiting.")