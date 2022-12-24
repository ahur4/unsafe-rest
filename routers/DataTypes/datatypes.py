from enum import Enum


class HashMethods(str, Enum):
    md5 = "md5"
    sha1 = "sha1"
    sha224 = "sha224"
    sha256 = "sha256"
    sha384 = "sha384"
    sha512 = "sha512"
    sha3_224 = "sha3-224"
    sha3_256 = "sha3-256"
    sha3_384 = "sha3-384"
    sha3_512 = "sha3-512"
    shake128 = "shake128"
    shake256 = "shake256"
    base16 = "base16"
    base32 = "base32"
    base64 = "base64"
    base85 = "base85"
    ascii85 = "ascii85"
    caesar = "caesar"


class Protocols(str, Enum):
    http = "http"
    socks4 = "socks4"
    socks5 = "socks5"


class Extentions(str, Enum):
    php = "php"
    asp = "asp"
    aspx = "aspx"
    js = "js"
    slash = "slash"
    cfm = "cfm"
    cgi = "cgi"
    brf = "brf"
    html = "html"