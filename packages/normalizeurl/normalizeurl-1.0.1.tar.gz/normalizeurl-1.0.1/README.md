## URL Normalize

> Normalize a URL

## Screenshot

<img src="https://gitlab.com/yoginth/normalizeurl/raw/master/Screenshot.png" width="550">

## Install

```
$ pip install normalizeurl
```

## Usage

```python
from normalizeurl import normalize

print(normalize('yoginth.com'))
#=> http://yoginth.com/

print(normalize('HTTP://mail.yoginth.com:80/?username=yoginth'))
#=> http://mail.yoginth.com/?username=yoginth
```

## License

[MIT][license] Yoginth

[LICENSE]: https://mit.yoginth.com
