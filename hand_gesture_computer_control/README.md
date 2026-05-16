# GestureOS

GestureOS is a real time computer vision project that uses a webcam to detect hand gestures and control a computer.

## Features

Open palm controls mouse movement.

Pinch performs left click.

Peace sign performs right click.

Fist pauses control.

Keyboard safety controls allow pause, resume, and quit.

## Tech Stack

Python

OpenCV

MediaPipe

PyAutoGUI

NumPy

## How It Works

Webcam input is captured with OpenCV.

MediaPipe detects hand landmarks.

Custom gesture logic classifies hand signs.

PyAutoGUI maps gestures to mouse and keyboard actions.

## Run

Install dependencies:

pip install -r requirements.txt

Run the app:

cd app
python main.py

## Controls

q quits the app.

p pauses control.

r resumes control.