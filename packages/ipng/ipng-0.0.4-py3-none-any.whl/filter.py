import math

def noop(current, previous, bpp):
    return current


def noop_reverse(current, previous, bpp):
    return current


def sub(current, previous, bpp):
    """
    To compute the Sub filter, apply the following formula to each
    byte of the scanline:

    Copy the scanline as we are computing difference between "Raw" bytes.

    Sub(x) = Raw(x) - Raw(x-bpp)

    :param current: byte array representing current scanline.
    :param previous: byte array representing the previous scanline (not used by this filter type)
    :param bpp: bytes per pixel
    :return: filtered byte array
    """
    result = bytearray(len(current))
    for x in range(len(current)):
        if x == 0:
            result[0] = 1
            if current[0] != 1:
                raise IOError(f'{current[0]} passed to Sub filter')
            continue

        result[x] = (current[x] - (current[x - bpp] if x - bpp > 0 else 0)) % 256
    return result


def sub_reverse(current, previous, bpp):
    """
    To reverse the effect of the Sub filter after decompression,
    output the following value:

    No need to copy as we are calculating Sub plus Raw and Raw is calculated on the fly.

    Sub(x) + Raw(x-bpp)

    :param current: byte array representing current scanline.
    :param previous: byte array representing the previous scanline (not used by this filter type)
    :param bpp: bytes per pixel
    :return: reverse-filtered byte array
    """
    for x in range(len(current)):
        if x == 0:
            if current[0] != 1:
                raise IOError(f'{current[0]} passed to Sub reverse filter')
            continue

        current[x] = (current[x] + (current[x - bpp] if x - bpp > 0 else 0)) % 256
    return current


def up(current, previous, bpp):
    """
    To compute the Up filter, apply the following formula to each byte
    of the scanline:

    Up(x) = Raw(x) - Prior(x)

    :param current: byte array representing current scanline.
    :param previous: byte array representing the previous scanline (not used by this filter type)
    :param bpp: bytes per pixel
    :return: filtered byte array
    """
    result = bytearray(len(current))
    for x in range(len(current)):
        if x == 0:
            result[0] = 2
            if current[0] != 2:
                raise IOError(f'{current[0]} passed to Up filter')
            continue

        result[x] = (current[x] - previous[x] if previous else 0) % 256
    return result


def up_reverse(current, previous, bpp):
    """
    To reverse the effect of the Up filter after decompression, output
    the following value:

    Up(x) + Prior(x)

    :param current: byte array representing current scanline.
    :param previous: byte array representing the previous scanline (not used by this filter type)
    :param bpp: bytes per pixel
    :return: reverse-filtered byte array
    """
    for x in range(len(current)):
        if x == 0:
            if current[0] != 2:
                raise IOError(f'{current[0]} passed to Up reverse filter')
            continue

        current[x] = (current[x] + (previous[x] if previous else 0)) % 256
    return current


def avg(current, previous, bpp):
    """
    To compute the Average filter, apply the following formula to each
    byte of the scanline:

    Average(x) = Raw(x) - floor((Raw(x-bpp)+Prior(x))/2)

    :param current: byte array representing current scanline.
    :param previous: byte array representing the previous scanline (not used by this filter type)
    :param bpp: bytes per pixel
    :return: filtered byte array
    """
    result = bytearray(len(current))
    for x in range(len(current)):
        if x == 0:
            result[0] = 3
            if current[0] != 3:
                raise IOError(f'{current[0]} passed to Avg filter')
            continue

        prior = previous[x] if previous else 0
        raw = current[x - bpp] if x - bpp > 0 else 0
        result[x] = (current[x] - math.floor((raw + prior) / 2)) % 256
    return result


def avg_reverse(current, previous, bpp):
    """
    To reverse the effect of the Average filter after decompression,
    output the following value:

    Average(x) + floor((Raw(x-bpp)+Prior(x))/2)

    :param current: byte array representing current scanline.
    :param previous: byte array representing the previous scanline (not used by this filter type)
    :param bpp: bytes per pixel
    :return: reverse-filtered byte array
    """
    for x in range(len(current)):
        if x == 0:
            if current[0] != 3:
                raise IOError(f'{current[0]} passed to Avg reverse filter')
            continue

        prior = previous[x] if previous else 0
        raw = current[x - bpp] if x - bpp > 0 else 0
        current[x] = (current[x] + math.floor((raw + prior) / 2)) % 256
    return current


def paeth(current, previous, bpp):
    """
    To compute the Paeth filter, apply the following formula to each
    byte of the scanline:

       Paeth(x) = Raw(x) - PaethPredictor(Raw(x-bpp), Prior(x), Prior(x-bpp))

    :param current: byte array representing current scanline.
    :param previous: byte array representing the previous scanline (not used by this filter type)
    :param bpp: bytes per pixel
    :return: filtered byte array
    """
    result = bytearray(len(current))
    for x in range(len(current)):
        if x == 0:
            result[0] = 4
            if current[0] != 4:
                raise IOError(f'{current[0]} passed to Paeth filter')
            continue

        left = current[x - bpp] if x - bpp > 0 else 0
        above = previous[x] if previous else 0
        upper_left = previous[x - bpp] if x - bpp > 0 and previous else 0
        result[x] = (current[x] - paeth_predictor(left, above, upper_left)) % 256
    return result


def paeth_reverse(current, previous, bpp):
    """
    To reverse the effect of the Paeth filter after decompression,
    output the following value:

       Paeth(x) + PaethPredictor(Raw(x-bpp), Prior(x), Prior(x-bpp))

    :param current: byte array representing current scanline.
    :param previous: byte array representing the previous scanline (not used by this filter type)
    :param bpp: bytes per pixel
    :return: reverse-filtered byte array
    """
    for x in range(len(current)):
        if x == 0:
            if current[0] != 4:
                raise IOError(f'{current[0]} passed to Paeth reverse filter')
            continue

        left = current[x - bpp] if x - bpp > 0 else 0
        above = previous[x] if previous else 0
        upper_left = previous[x - bpp] if x - bpp > 0 and previous else 0
        current[x] = (current[x] + paeth_predictor(left, above, upper_left)) % 256
    return current


def paeth_predictor(a, b, c):
    """
    The "paeth predictor" used for paeth filter.

    :param a: left
    :param b: above
    :param c: upper-left
    :return: predicted value
    """
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)

    if pa <= pb and pa <= pc:
        return a
    elif pb <= pc:
        return b
    else:
        return c


# PNG filter method 0 defines five basic filter types:
#
# Type    Name
#
# 0       None
# 1       Sub
# 2       Up
# 3       Average
# 4       Paeth
FILTER_TYPE_TO_FUNC = {
    0: (noop, noop_reverse),
    1: (sub, sub_reverse),
    2: (up, up_reverse),
    3: (avg, avg_reverse),
    4: (paeth, paeth_reverse)
}
