import sys
import gpxpy.gpx

try:
    file1 = sys.argv[1]
    file2 = sys.argv[2]
except Exception:
    print("Usage: gpx-merge <file1> <file2>")
    print("Merge <file2> into <file1> and optionally delete <file2>")
    sys.exit(1)


gpx_file = open(file1)
gpx = gpxpy.parse(gpx_file)
# Create new track in our GPX:
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)
# Create first segment in our GPX track:
gpx_segment = gpxpy.gpx.GPXTrackSegment()
gpx_track.segments.append(gpx_segment)


gpx_file = open(file2)
gpx2 = gpxpy.parse(gpx_file)

for track in gpx2.tracks:
    for segment in track.segments:
        for point in segment.points:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point.latitude, point.longitude, elevation=point.elevation))
print(gpx.to_xml(),file=open(file1, 'w'))
