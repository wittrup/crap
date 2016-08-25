import math


def frespetowav(frequency, speed):
    return speed / frequency


def wavdimtonrf(wavelength, diameter):
    return diameter**2 / 4 / wavelength


def idxtopre(idx, args):
    precision, flat_active_area, radius_of_curvature, near_field = args
    distance = idx / precision
    if flat_active_area:
        k = 1
    elif radius_of_curvature == distance:
        k = 10000
    else:
        k = radius_of_curvature / (radius_of_curvature - distance)
    return k * math.sin(math.pi * near_field / 2 / k / distance)


def near_field_shift(foclenwat, patlenwat, acovelwat, acovelmet):
    """
    :param foclenwat: Fw = focal length in water
    :param patlenwat: Xw = path length in water
    :param acovelwat: Cw = acoustic velocity in water
    :param acovelmet: Cm = acoustic velocity in metal
    :return: Fv = new (virtual) focal length		foclenvir"""
    return patlenwat + (foclenwat - patlenwat) * acovelwat / acovelmet


def focwattomet(foclenvir, patlenwat):
    """
    :param foclenvir: Fv = new (virtual) focal length
    :param patlenwat: Xw = path length in water
    :return: Xm = path length in metal to focus	patlenmet"""
    return foclenvir - patlenwat


def bsttrav(ilst, args):
    ilef, imid, irig = ilst

    plef = idxtopre(ilef, args)
    prig = idxtopre(irig, args)

    if prig > plef: # go right
        ilef = imid
    elif plef > prig: # go left
        irig = imid
    else:
        ilef = imid
        irig = imid
    imid = int((irig + ilef) / 2)
    return [ilef, imid, irig]


def towavnrffod(frequency, active_diameter, radius_of_curvature, medium_velocity, flat_active_area=False, precision = 100):
    """
    :param frequency:           Operating center frequency of the transducer
    :param active_diameter:     Active diameter of the transducer
    :param radius_of_curvature: Check if the transducer is flat
    :param medium_velocity:     Spherical concave radius of curvature of the active surface
    :param flat_active_area:    Sound velocity in the medium in contact with the transducer
    :return: list of []
    :wavelength:                Wavelength of the emitted beam
    :near_field:                Near field distance
    :focal_distance:            Distance of the maximum of intensity on the beam axis"""

    wavelength = frespetowav(frequency, medium_velocity) / 1000 # mm-Mhz ratio
    near_field = wavdimtonrf(wavelength, active_diameter)

    indx = int(min(radius_of_curvature, near_field) * precision)
    ilef = int(0.5 * indx)
    irig = int(1.5 * indx)
    ilst = [ilef, indx, irig]

    while ilst[0] != ilst[2] and ilst[0] != ilst[2] - 1:
        ilst = bsttrav(ilst, [precision, flat_active_area, radius_of_curvature, near_field])
    focal_distance = ilst[2] / precision

    return [wavelength, near_field, focal_distance]

if __name__ == '__main__':
    print(towavnrffod(5, 10, 75, 1480))
    print([0.296, 84.45945945945947, 47.81039], 'fasit')