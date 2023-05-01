# Desktop Recorder to RTMP Server

This Python script allows you to record your desktop screen and send it to an RTMP server in real-time. The script utilizes OpenCV for face detection and drawing, FFmpeg for video encoding, and PyAutoGUI for capturing the desktop screen and mouse cursor information.

## Features

- Records the entire desktop screen (1920x1080 resolution by default)
- Detects and highlights faces in the recorded video using Haar cascades
- Captures and displays the mouse cursor position
- Streams the recorded video to the specified RTMP server

## Dependencies

To run this script, you'll need the following Python libraries installed:

- OpenCV (`opencv-python`)
- FFmpeg (`ffmpeg-python`)
- PyAutoGUI
- keyboard
- mouseinfo
- numpy

You can install these dependencies using the following command:

```bash
pip install opencv-python imageio-ffmpeg pyautogui keyboard mouseinfo numpy
```

## Usage

To run the script, you'll need to provide the URL to your RTMP server using the `-u` or `--url` argument:

```bash
python desktop_recorder_rtmp.py -u <RTMP_SERVER_URL>
```

For example:

```bash
python desktop_recorder_rtmp.py -u rtmp://example.com/live/stream-key
```

To stop the recording and close the application, press the "q" key on your keyboard.

## Setting up your own RTMP server

You can set up your own RTMP server using the Nginx plugin and Docker. A pre-configured Docker image is available on Docker Hub: [tiangolo/nginx-rtmp](https://hub.docker.com/r/tiangolo/nginx-rtmp).

To get started, simply pull the Docker image and follow the instructions provided on the Docker Hub page.

## Example

Here's an example of the application in action. A GIF showcasing the desktop recording and streaming to an RTMP server will be inserted here.

![Example GIF](example.gif)

## Customization

You can easily customize the script to fit your needs, such as:

- Change the default screen resolution by modifying the `width` and `height` variables in the `start_recording` function.
- Adjust the video quality by modifying the `bufsize`, `preset`, and `crf` variables in the `start_recording` function.
- Customize the face detection parameters, like `scaleFactor`, `minNeighbors`, and `minSize`, in the `detect_faces` function.

## License

This project is licensed under the MIT License.


