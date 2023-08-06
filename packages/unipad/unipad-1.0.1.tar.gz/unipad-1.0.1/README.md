## Uni Pad

> 🦄 Left pad a string with Unicorns

## Screenshot

<img src="https://gitlab.com/yoginth/unipad/raw/master/Screenshot.png" width="550">

## Install

```
$ pip install unipad
```

## Usage

```python
import unipad

unipad.pad('yoginth', 10)
#=> 🦄🦄🦄yoginth
```

## API

### unipad.pad(input, length)

Pads `input` with unicorns on the left side if it's shorter than `length`. Padding unicorns are truncated if they exceed `length`.

#### input

Type: `string`

String to pad.

#### length

Type: `number`<br>
Default: `0`

Padding length.

## License

[MIT][license] Yoginth

[LICENSE]: https://mit.yoginth.com
