#!/usr/bin/python3.1
# utf-8

import os.path
from pykml import parser
import gpxpy.gpx
import re


pattern = (r'(\d+[,\.]?\d*)\s' * 3)[:-2] # removes last whitespace
kmlfile = input()
gpxfile = os.path.splitext(kmlfile)[0]+'.gpx'

with open(kmlfile) as f:
    doc = parser.parse(f)

gpx = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack()    # Create first track in our GPX
gpx.tracks.append(gpx_track)
gpx_segment = gpxpy.gpx.GPXTrackSegment() # Create first segment in our GPX track
gpx_track.segments.append(gpx_segment)

for element in doc.getiterator():
    match = re.match(pattern, str(element))
    if match:
        long,lat,msl=map(float,match.groups())
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, long, elevation=msl))
print(gpx.to_xml(),file=open(gpxfile, 'w'))
