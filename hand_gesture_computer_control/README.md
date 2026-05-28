# GestureOS: Hand Sign Computer Controller

GestureOS is a computer vision desktop automation project that uses a webcam to detect hand signs and trigger computer actions.

Instead of using a keyboard or mouse, the user can open apps and control desktop workflows using hand gestures.

## Project Goal

The goal of this project is to build a hands-free computer control system using:

Python

OpenCV

MediaPipe

PyAutoGUI

Computer automation

Gesture logging

This project is useful for productivity, accessibility, presentations, and touchless computer interaction.

## Current Gesture Controls

| Hand Sign | Action |
|---|---|
| One finger up | Open VS Code |
| Two fingers up | Open browser |
| Three fingers up | Open terminal |
| Four fingers up | Open LinkedIn |
| Open hand | Open calculator |
| Fist | Close active window |

To prevent accidental actions, each gesture must be held for about 1 second before the action runs.

## How It Works

The system follows this flow:

```python
Webcam frame
→ OpenCV captures video
→ MediaPipe detects hand landmarks
→ GestureDetector classifies the hand sign
→ ActionMapper runs the matching computer action
→ GestureLogger saves gesture activity to CSV