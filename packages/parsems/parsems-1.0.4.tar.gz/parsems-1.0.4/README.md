## Parse ms

> Parse milliseconds into a Dictionary

## Demo

Demo on [Repl.it](https://repl.it/@yoginth/parsems)

## Screenshot

<img src="https://gitlab.com/yoginth/parsems/raw/master/Screenshot.png" width="550">

## Install

```
$ pip install parsems
```

## Usage

```python
from parsems import parseMs

parseMs(2449850001)

"""
{
	'days': 28,
	'hours': 8,
	'minutes': 30,
	'seconds': 50,
	'milliseconds': 1,
	'microseconds': 0,
	'nanoseconds': 0
}
"""
```

## Thanks

- [Sindresorhus's parse-ms](https://github.com/sindresorhus/parse-ms)

## License

[MIT][license] Yoginth

[LICENSE]: https://mit.yoginth.com
