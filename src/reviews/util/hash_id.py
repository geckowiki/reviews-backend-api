from uuid import UUID

from hashids import Hashids

from app.settings import settings


def to_base_(n, base):
    digs = "0123456789abcdefghijklmnopqrstuvwxyz"
    tmp = []
    while n:
        n, i = divmod(n, base)
        tmp.append(digs[i])
    return "".join(tmp[::-1])


def change(s, from_base, to_base):
    if to_base < 2 or to_base > 36 or from_base < 2 or from_base > 36:
        raise ValueError("bases must be between 2 and 36")
    try:
        return to_base_(int(s, from_base), to_base)
    except ValueError:
        try:
            n = int("".join([ch for ch in s if ch.isdigit()]), from_base)
            return to_base_(n, to_base)
        except ValueError:
            return 0


def convert_uuid_to_hashid(id: UUID):
    hypenless_id = str(id).replace("-", "")
    hash_int = int(change(hypenless_id, 11, 10))
    hashids = Hashids(salt=settings.SECRET_KEY)
    return hashids.encode(hash_int)
