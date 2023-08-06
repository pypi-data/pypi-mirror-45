import math

def parseMs(time):

    if time > 0:
        roundTowardsZero = math.floor
    else:
        roundTowardsZero = math.ceil

    return {
		'days': roundTowardsZero(time / 86400000),
		'hours': roundTowardsZero(time / 3600000) % 24,
		'minutes': roundTowardsZero(time / 60000) % 60,
		'seconds': roundTowardsZero(time / 1000) % 60,
		'milliseconds': roundTowardsZero(time) % 1000,
		'microseconds': roundTowardsZero(time * 1000) % 1000,
		'nanoseconds': roundTowardsZero(time * 1e6) % 1000
	}
