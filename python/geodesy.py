"""This module contain a few function relevant when dealing with geodesy — also known as geodetics or geodetics engineering —
a branch of applied mathematics and earth sciences, is the scientific discipline that deals with the measurement and representation of the Earth"""

import math

def DistMidLatLong(FoLat, FoLng, ToLat, ToLng):
    R = 6371000 # metres
    rFoLat = math.radians(FoLat)
    rToLat = math.radians(ToLat)
    dLat =  math.radians(ToLat-FoLat)
    dLong = math.radians(ToLng - FoLng)

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(rFoLat) * math.cos(rToLat) * math.sin(dLong/2) * math.sin(dLong/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = R * c
    return d

def distance_on_unit_sphere(FoLat, FoLng, ToLat, ToLng):
    """ Convert latitude and longitude to spherical coordinates in radians."""
    phi1 = math.radians(90.0 - FoLat)
    phi2 = math.radians(90.0 - ToLat)

    theta1 = math.radians(FoLng)
    theta2 = math.radians(ToLng)

    """Compute spherical distance from spherical coordinates.

     For two locations in spherical coordinates
     (1, theta, phi) and (1, theta', phi')
     cosine( arc length ) =
        sin phi sin phi' cos(theta-theta') + cos phi cos phi'
     distance = rho * arc length"""

    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + math.cos(phi1) * math.cos(phi2))
    arc = math.acos(cos)

    """Remember to multiply arc by the radius of the earth in your favorite set of units to get length."""
    return arc