## Has Emoji

> Check whether a string or character has any emoji

## Screenshot

<img src="https://gitlab.com/yoginth/hasemoji/raw/master/Screenshot.png" width="550">

## Install

```
$ pip install hasemoji
```

## Usage

```python
import hasemoji

print(hasemoji.char('😃'))
#=> True

print(hasemoji.string('I 💖 emoji'))
#=> True

print(hasemoji.char('I'))
#=> False

print(hasemoji.string('I love emoji'))
#=> False
```

## License

[MIT][license] Yoginth

[LICENSE]: https://mit.yoginth.com
