from default import hashlib, random, settings, string, time


def _sha512(source: str):
    sha512 = hashlib.sha512()
    sha512.update(source)
    return sha512.hexdigest()


def _md5(source: str):
    md5 = hashlib.md5()
    md5.update(source)
    return md5.hexdigest()


def _sha1(source: str):
    sha1 = hashlib.sha1()
    sha1.update(source)
    return sha1.hexdigest()


def _sha224(source: str):
    sha224 = hashlib.sha224()
    sha224.update(source)
    return sha224.hexdigest()


def _sha256(source: str):
    sha256 = hashlib.sha256()
    sha256.update(source)
    return sha256.hexdigest()


def _sha384(source: str):
    sha384 = hashlib.sha384()
    sha384.update(source)
    return sha384.hexdigest()


def _pbkdf2_hmac(source: str):
    pbkdf2_hmac = hashlib.pbkdf2_hmac()
    pbkdf2_hmac.update(source)
    return pbkdf2_hmac.hexdigest()


def gen(source: str):
    if settings.gen_method == "md5":
        return _md5(source)
    elif settings.gen_method == "sha512":
        return _sha512(source)
    elif settings.gen_method == "sha384":
        return _sha384(source)
    elif settings.gen_method == "sha256":
        return _sha256(source)
    elif settings.gen_method == "sha1":
        return _sha1(source)
    elif settings.gen_method == "sha224":
        return _sha224(source)
    elif settings.gen_method == "pbkdf2_hmac":
        return _pbkdf2_hmac(source)


def simple_gen(length: int):
    random.seed(time.time_ns())
    return ''.join(random.sample(
        string.ascii_letters + string.digits, length))
