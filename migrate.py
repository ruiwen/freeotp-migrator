#!/usr/bin/env python3

# Code largely based off https://gitlab.com/stavros/freeotp-to-andotp-migrator/
# otpauth:// URI construction based off https://github.com/google/google-authenticator/wiki/Key-Uri-Format

import base64
import json
import sys
import xml.etree.ElementTree
from urllib.parse import urlencode, quote

import pyqrcode


# Ref: https://gitlab.com/stavros/freeotp-to-andotp-migrator/blob/master/freeotp_migrate.py
def read_tokens(filename):
    e = xml.etree.ElementTree.parse(filename).getroot()
    for item in e.findall("string"):
        if item.get("name") == "tokenOrder":
            continue
        token = json.loads(item.text)
        token["secret"] = base64.b32encode(
            bytes(x & 0xff for x in token["secret"])
        ).decode("utf8")

        issuer = token.get("issuerAlt") or \
            token.get("issuerExt") or \
            token.get("issuerInt")
        label = token.get("label") or token.get("labelAlt")

        if label and issuer:
            token_label = "%s:%s" % (issuer, label)
        else:
            token_label = label or issuer

        yield {
            "algorithm": token["algo"],
            "secret": token["secret"],
            "digits": token["digits"],
            "type": token["type"],
            "period": token["period"],
            "label": token_label,
            "issuer": issuer
        }

def make_qrcode(code):
    uri = "otpauth://{type}/{label}?{qs}".format(type=code['type'].lower(), label=quote(code['label']), qs=urlencode(code))

    return pyqrcode.create(uri)

def main():
    if sys.version_info.major < 3:
        print("This script requires Python 3.")
        sys.exit(1)

    if len(sys.argv) != 2:
        print("Usage: ./freeotp_migrate.py <filename>")
        sys.exit(1)

    # Dump the tokens.
    output = json.dumps(
        list(read_tokens(sys.argv[1])),
        sort_keys=True,
        indent=2,
        separators=(',', ': ')
    )

    print(output)


if __name__ == "__main__":
    main()
