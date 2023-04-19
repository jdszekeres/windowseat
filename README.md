# WindowSeat
WindowSeat is a Python project that generates a video of the view out of a plane as if on the window seat. The project uses the Mapbox API to download satellite images along a flight path and stitches them together to create a video.

## Installation
Clone the repository
bash
Copy code
git clone https://github.com/<username>/WindowSeat.git
Install the required packages
Copy code
pip install -r requirements.txt
Obtain a Mapbox API key from https://account.mapbox.com/access-tokens/

Add your Mapbox API key to the mapboxkey file.

## Usage
Call the function get_video(start, end, time, fps) with the following parameters:

start: Tuple of starting coordinates (latitude, longitude)
end: Tuple of ending coordinates (latitude, longitude)
time: Flight time in seconds
fps: Frames per second for the video
Example:


from WindowSeat import get_video

start = (32.7317,-117.19)
end = (40.76078, -111.89105)
time = 30
fps = 30

get_video(start, end, time, fps)
This will create a video file flight.mp4 in the current directory.

## License
This project is licensed under the MIT License. Feel free to use and modify the code for your own purposes.