from os.path import exists
from os import remove
import sys
import json

SECRET_STORAGE = './tokens.json'
DEFAULT_DICT = {
    'tokens': []
}

def check_for_existing_secret() -> dict:
    if not exists(SECRET_STORAGE):
        with open(SECRET_STORAGE, 'w+') as f:
            print('Created default secret file with empty content')
            f.write(json.dumps(DEFAULT_DICT, indent=4))
            f.close()
        return DEFAULT_DICT
    else:
        with open(SECRET_STORAGE, 'r+') as storage:
            data = json.load(storage)
            storage.close()
        if data['tokens'] is None:
            remove(SECRET_STORAGE)
            return check_for_existing_secret()
        return data

def exists_in_secret(secret: str) -> bool:
    raw_file = check_for_existing_secret()
    return secret in raw_file['tokens']

def store_secret(secret: str):
    raw_file = check_for_existing_secret()
    if secret in raw_file['tokens']:
        print('Secret already exists')
        return
    raw_file['tokens'].append(secret)
    with open(SECRET_STORAGE, 'w+') as f:
        f.write(json.dumps(raw_file, indent=4))
        f.close()
    print('Wrote new Secret')

if __name__ == '__main__':
    store_secret(sys.argv[1])
