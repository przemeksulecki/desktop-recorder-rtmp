import argparse
import cv2
import ffmpeg
import keyboard
import mouseinfo
import numpy as np
import pyautogui
import time
import threading

def draw_cursor(frame, x, y):
    color = (0, 0, 255)
    radius = 5
    thickness = 2
    cv2.circle(frame, (x, y), radius, color, thickness)

def detect_faces(frame, face_cascade, face_list):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    face_list.clear()
    face_list.extend(faces)

def draw_faces(frame, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

def start_recording(rtmp_url):
    width = 1920
    height = 1080
    fps = 15
    bufsize = "300k"
    preset = "ultrafast"
    crf = 25

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    process = (
        ffmpeg
        .input("pipe:", format="rawvideo", pix_fmt="bgr24", s="{}x{}".format(width, height), r=fps)
        .output(rtmp_url, format="flv", vcodec="libx264", pix_fmt="yuv420p", r=fps, crf=crf, preset=preset, tune="zerolatency")
        .overwrite_output()
        .global_args("-bufsize", bufsize, "-re")
        .run_async(pipe_stdin=True)
    )

    prev_time = time.time()
    face_list = []
    face_detection_thread = None
    time_diff = 0

    while True:
        screenshot = pyautogui.screenshot(region=(0, 0, width, height))
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        if face_detection_thread is None or not face_detection_thread.is_alive():
            face_detection_thread = threading.Thread(target=detect_faces, args=(frame, face_cascade, face_list))
            face_detection_thread.start()

        draw_faces(frame, face_list)

        x, y = mouseinfo.position()
        draw_cursor(frame, x, y)

        try:
            process.stdin.write(frame.tobytes())
        except Exception as e:
            print(f"Error writing frame to stdin: {e}")

        curr_time = time.time()
        elapsed_time = curr_time - prev_time - time_diff
        if elapsed_time < 1/fps:
            time.sleep(1/fps - elapsed_time)
            time_diff = 0
        else:
            time_diff += elapsed_time - 1/fps

        prev_time = curr_time

        if keyboard.is_pressed("q"):
            break

    face_detection_thread.join()
    process.stdin.close()
    process.wait()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", type=str, required=True, help="URL to RTMP server")
    args = parser.parse_args()

    rtmp_url = args.url
    start_recording(rtmp_url)
