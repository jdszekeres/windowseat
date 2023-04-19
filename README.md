# Windowseat - Python script that creates a video from a flight path
This Python script generates a video from a flight path by downloading satellite images from Mapbox API and stitching them together into a video using FFmpeg.

## Requirements
- Python 3
- requests
- numpy
- FFmpeg

You will also need a Mapbox API key. If you don't have one, you can create a free account on their website to obtain it.

## Usage
```bash
python windowseat.py start_location end_location duration fps zoom orientation
```
- start_location: The starting airport code (e.g., JFK).
- end_location: The ending airport code (e.g., LAX).
- duration: The length of the video in seconds.
fps: The frames per second of the video.
z- oom: The zoom level of the Mapbox satellite images (0-22).
- orientation: The orientation of the camera, either 'l' for left or 'r' for right.

### Output

The script generates a video file named flight.mp4.

## Credits
This script uses the Global Airport Database by Arash Partow to obtain the latitude and longitude of the airports.
# MIT License