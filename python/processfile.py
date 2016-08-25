__author__ = 'wittr'


import math

def DistMidLatLong(FoLat, FoLong, ToLat, ToLong):
    R = 6371000 # metres
    rFoLat = math.radians(FoLat)
    rToLat = math.radians(ToLat)
    dLat =  math.radians(ToLat-FoLat)
    dLong = math.radians(ToLong-FoLong)

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(rFoLat) * math.cos(rToLat) * math.sin(dLong/2) * math.sin(dLong/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = R * c
    return d


def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to
    # spherical coordinates in radians.
    # degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    # phi1 = (90.0 - lat1)*degrees_to_radians
    # phi2 = (90.0 - lat2)*degrees_to_radians
    phi1 = math.radians(90 - lat1)
    phi2 = math.radians(90 - lat2)


    # theta = longitude
    theta1 = math.radians(long1) # *degrees_to_radians
    theta2 = math.radians(long2)

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc

def substr(str, start, stop):
    if start in str and stop in str:
        return str[str.find(start) + len(start):str.find(stop, str.find(start) + len(start))]
    else:
        return ''

import datetime

kmlfile = open("history-2015-10-03.kml")
tslast = None
flatlast = None
flonglast = None

for line in kmlfile:
    tsstr = substr(line, '<when>', '</when>')
    cord = substr(line, '<gx:coord>', '</gx:coord>')
    long = substr(cord, '', ' ')
    lat = substr(cord, long + ' ', ' ')
    if tsstr and lat and long:
        tstime = datetime.datetime.strptime(substr(tsstr, '', '.'), "%Y-%m-%dT%H:%M:%S")
        flat = float(lat)
        flong = float(long)

        if tslast != None:
            tsdelta = (tstime-tslast)
            dist1 = DistMidLatLong(flatlast, flonglast, flat, flong)
            speed = dist1 / tsdelta.seconds # meter pr second
            kmh = speed * 3.6
            dist2 = distance_on_unit_sphere(flatlast, flonglast, flat, flong) * 6371008.8
            print(tstime.strftime('%H:%M:%S'), "%.5f" % flat, "%.5f" % flong, "%.2f" % dist1, "%.2f" % dist2 )

        tslast = tstime
        flatlast = flat
        flonglast = flong










