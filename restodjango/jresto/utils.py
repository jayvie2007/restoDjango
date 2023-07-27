import uuid

def generate_uid():
    uid = uuid.uuid4().hex[-8:]
    return uid

def generate_fooduid():
    uid = f"food__" + uuid.uuid4().hex[-8:]
    return uid

def generate_drinkuid():
    uid = f"drink__" + uuid.uuid4().hex[-8:]
    return uid

def generate_sideuid():
    uid = f"side__" + uuid.uuid4().hex[-8:]
    return uid

