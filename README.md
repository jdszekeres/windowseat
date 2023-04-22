# Windowseat - Python script that creates a video from a flight path
This Python script generates a video from a flight path by downloading satellite images from Mapbox API and stitching them together into a video using FFmpeg.

## Requirements
- Python 3
- requests
- numpy
- FFmpeg

You will also need a Mapbox API key. If you don't have one, you can create a free account on their website to obtain it. Put it in the file  **mapboxkey**

## Usage
```bash
python fullflight.py start_airport end_end duration fps orientation
```
- start_location: The starting airport code (e.g., JFK).
- end_location: The ending airport code (e.g., LAX).
- duration: The length of the video in seconds.
- fps: The frames per second of the video.
- orientation: The orientation of the camera, either 'l' for left or 'r' for right.

### Output

The script generates a video file named flight.mp4 from satelite image stitched together.
## Examples
SLC -> AUS 

![SLC-AUS](github.com/jdszekeres/windowseat/examples/SLC-AUS.gif)
## Credits
This script uses the Global Airport Database by Arash Partow to obtain the latitude and longitude of the airports and airnav.com for runway headings.
# MIT License
