def toMilliseconds(foo = {
	'days': 0,
	'hours': 0,
	'minutes': 0,
	'seconds': 0,
	'milliseconds': 0,
	'microseconds': 0,
	'nanoseconds': 0
}):
    ms = 0
    for key, value in foo.items():
        if key == 'days':
            ms += value * 864e5;
        elif key == 'hours':
            ms += value * 36e5;
        elif key == 'minutes':
            ms += value * 6e4;
        elif key == 'seconds':
            ms += value * 1e3;
        elif key == 'milliseconds':
            ms += value;
        elif key == 'microseconds':
            ms += value / 1e3;
        elif key == 'nanoseconds':
            ms += value / 1e6;
        else:
            print('Undefined')

    return (int(ms))
