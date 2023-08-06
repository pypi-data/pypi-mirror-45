## Compare URLs

> Compare URLs by first normalizing them

## Demo

Demo on [Repl.it](https://repl.it/@yoginth/compareurls)

## Screenshot

<img src="https://gitlab.com/yoginth/compareurls/raw/master/Screenshot.png" width="550">

## Install

```
$ pip install compareurls
```

## Usage

```python
import compareurls

compareurls.check(
    'HTTP://yoginth.com/?username=yoginth&password=qwerty',
    'yoginth.com/?username=yoginth&password=qwerty'
)
#=> True
```

## License

[MIT][license] Yoginth

[LICENSE]: https://mit.yoginth.com
