import uuid

def get_random_username_addon():
    addon = str(uuid.uuid4())[:8].replace('-', '').lower()
    return addon