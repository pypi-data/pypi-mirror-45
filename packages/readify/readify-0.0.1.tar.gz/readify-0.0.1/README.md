## Readify [![pipeline status](https://gitlab.com/yoginth/readify/badges/master/pipeline.svg)](https://gitlab.com/yoginth/readify/commits/master)

> Convert Integer to Human Readable format

## Demo

Demo on [Repl.it](https://repl.it/@yoginth/readify)

## Install

```
$ pip install readify
```

## Usage

```python
from readify import readify

print(readify(1545451548515484)) 
#=> 1545.5T

print(readify(736572365, 5)) 
#=> 736.57236M
```
## API

### readify(input)

Type: `number`

### readify(input, fraction_point)

Type: `number` and `number`

Number to humanize.
Fraction Point

## License

[MIT][LICENSE] Yoginth

[LICENSE]: https://mit.yoginth.com
