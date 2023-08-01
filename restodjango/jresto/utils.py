import uuid

def generate_uid():
    uid = uuid.uuid4().hex[-8:]
    return uid
