import requests
import shutil
import numpy as np
from subprocess import run
from math import atan2, degrees
import threading
import random
import sys
import csv
from PIL import Image
from io import BytesIO
import staticmaps

def get_photo(center, zoom, key, bearing, loc, style="yopo/clgn5udy3001u01pl40l05mwj"):
    # Define the download URLs
    minimap_context = staticmaps.Context()
    minimap_context.set_tile_provider(staticmaps.tile_provider_OSM)
    point = staticmaps.create_latlng(center[1],center[0])
    image_url = f"https://api.mapbox.com/styles/v1/{style}/static/{center[0]},{center[1]},{zoom},{bearing},60/480x640?access_token={key}"
    # Download the images
    # minimap_resp = requests.get(minimap_url, stream=True)
    minimap_context.add_object(staticmaps.Marker(point, color=staticmaps.RED, size=12))
    minimap_context.set_center(point)
    minimap_context.set_zoom(6)
    image_resp = requests.get(image_url, stream=True)
    # Open the minimap image and resize it to 100x100 pixels
    minimap_img = minimap_context.render_pillow(100,100)
    # Open the image and create a new blank image with the same dimensions
    image = Image.open(BytesIO(image_resp.content))
    # Paste the minimap image on the bottom left corner of the new image
    image.paste(minimap_img, (0, 0))
    # Save the new image to disk
    image.save(f"{loc}.jpg")



def get_points_on_line(coord1, coord2, count):
    x1, y1 = coord1
    x2, y2 = coord2
    dx = (x2 - x1) / (count - 1)
    dy = (y2 - y1) / (count - 1)
    points_on_line = [(x1 + i*dx, y1 + i*dy) for i in range(count)]
    return points_on_line

def get_angle_between_coordinates(coord1, coord2):
    # Get latitude and longitude differences between coordinates
    delta_lat = coord2[0] - coord1[0]
    delta_lon = coord2[1] - coord1[1]

    # Calculate the angle in radians using atan2
    angle = atan2(delta_lat, delta_lon)

    # Convert angle from radians to degrees
    angle_degrees = degrees(angle)

    # Ensure angle is between 0 and 360 degrees
    if angle_degrees < 0:
        angle_degrees += 360

    return angle_degrees
def get_db(start,end):
    with open("GlobalAirportDatabase.txt") as file:
        print("This program uses the Global Airport Database by Arash Partow")
        csvs = csv.reader(file, delimiter=":")
        for i in csvs:
            if i[1] == start.upper():
                sstart = [float(i[-1]),float(i[-2])]
                print("start: ",i[3])
            if i[1] == end.upper():
                send = [float(i[-1]),float(i[-2])]
                print("end: ",i[3])
    return sstart, send
if __name__ == "__main__":
    # Get command line arguments for start, end, time, fps, and zoom
    start = sys.argv[1]
    end = sys.argv[2]
    time = int(sys.argv[3])
    fps = int(sys.argv[4])
    zoom = float(sys.argv[5])
    left = "l" in sys.argv[6].lower()


    start, end = get_db(start,end)

    keys = open("mapboxkey").read().splitlines()
    pol = get_points_on_line(start, end, fps * time)
    bearing = get_angle_between_coordinates(start, end) + 90
    if left:
        bearing -= 180
    threads = []

    # Start a thread for each photo download
    for i, v in enumerate(pol):
        filename = f"photos/{i:04n}"
        t = threading.Thread(target=get_photo, args=(v, zoom, random.choice(keys), bearing, filename))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    code = run(f"ffmpeg -framerate {fps} -i 'photos/%04d.jpg' flight.mp4; rm photos/*.jpg".split(" "))
    if code.returncode != 0:
        print(f"command 'ffmpeg -framerate {fps} -i 'photos/%04d.jpg' flight.mp4; rm photos/*.jpg' returned an non-zero return code. Make sure you have ffmpeg installed.")
