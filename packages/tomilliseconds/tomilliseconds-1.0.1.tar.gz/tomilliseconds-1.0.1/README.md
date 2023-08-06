## Compare URLs

> Convert an object of time properties to milliseconds: {'seconds': 10} → 10000

## Demo

Demo on [Repl.it](https://repl.it/@yoginth/tomilliseconds)

## Screenshot

<img src="https://gitlab.com/yoginth/tomilliseconds/raw/master/Screenshot.png" width="550">

## Install

```
$ pip install tomilliseconds
```

## Usage

```python
from tomilliseconds import toMilliseconds

toMilliseconds({
	'days': 28,
	'hours': 8,
	'minutes': 30,
	'seconds': 50,
	'milliseconds': 1
})

#=> 2449850001
```

## API

### toMilliseconds(input)

#### input

Type: `Dictionary`

Specify an object with any of the following properties:

- `days`
- `hours`
- `minutes`
- `seconds`
- `milliseconds`
- `microseconds`
- `nanoseconds`

## Thanks

- [Sindresorhus's to-milliseconds](https://github.com/sindresorhus/to-milliseconds)

## License

[MIT][license] Yoginth

[LICENSE]: https://mit.yoginth.com
