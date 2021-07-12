from hashlib import md5


def convert_to_md5(data):
    return md5(data.encode('utf-8')).hexdigest().upper()
