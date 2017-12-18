
I was using [FreeOTP](https://play.google.com/store/apps/details?id=org.fedorahosted.freeotp) for my 2FA tokens, until I discovered recently that they pushed an [update that prevented users from backing up their own tokens](https://github.com/freeotp/freeotp-android/issues/20#issuecomment-344251241).

Needed a quick way to extract/backup my tokens from FreeOTP, to started cobbling some scripts together


## Extracting tokens from FreeOTP

_You'll need a rooted phone and `adb` access for this._

First, extract the tokens from the phone

```shell
$ adb shell
$ su
# cat /data/data/org.fedorahosted.freeotp/shared_prefs/tokens.xml
< token data>
```

Ref: https://github.com/freeotp/freeotp-android/issues/20#issuecomment-339366788

Either copy-paste the token data into a separate file, or `cp` it to a more accessible location in your phone's storage, eg. `/sdcard`, and then `adb pull` it from the phone to your local machine.

## Extracting token data

Assuming your token data is in `tokens.xml`,

```python
$ python migrate.py tokens.xml
[
  {
    "algorithm": "SHA1",
    "secret": "BASE62SECRETDATA==",
    "digits": 6,
    "type": "TOTP",
    "period": 30,
    "label": "Issuer:Account",
    "issuer": "Issuer"
  },
  {
    "algorithm": "SHA1",
    "secret": "TOPSECRETHUNTER2==",
    "digits": 6,
    "type": "TOTP",
    "period": 30,
    "label": "Issuer2:Account",
    "issuer": "Issuer2"
  },
  ...
]
```

Simply running the script from the console will output JSON that you can pipe to a file for safekeeping.

If you'd like to generate QR codes that can be scanned, you can do it like so

```
$ python
>>> import migrate
>>> codes = list(migrate.read_tokens('tokens.xml'))
>>> qr = pyqrcode.create(codes[0])
>>> print(qr.terminal())
< ... mass of qrcode data ...>
```


