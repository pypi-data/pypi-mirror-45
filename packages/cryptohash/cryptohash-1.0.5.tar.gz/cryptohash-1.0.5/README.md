## Crypto Hash

> Tiny hashing module that uses the native crypto API in Python

## Demo

Demo on [Repl.it](https://repl.it/@yoginth/cryptohash)

## Screenshot

<img src="https://gitlab.com/yoginth/cryptohash/raw/master/Screenshot.png" width="550">

## Install

```
$ pip install cryptohash
```

## Usage

```python
from cryptohash import sha1

print (sha1('🤓'))
#=> d0b16946377589fbc68d8b1ca324f16e84171463
```

## API

## API

### sha1(input)
### sha224(input)
### sha256(input)
### sha384(input)
### sha512(input)

### md5(input)

Returns a `Promise<string>` with a hex-encoded hash.

*Don't use `md5` or `sha1` for anything sensitive. [They're insecure.](http://googleonlinesecurity.blogspot.no/2014/09/gradually-sunsetting-sha-1.html)*

#### input

Type: `string`

##### outputFormat

Type: `string`
Values: `hex`
Default: `hex`

## License

[MIT][license] Yoginth

[LICENSE]: https://mit.yoginth.com
