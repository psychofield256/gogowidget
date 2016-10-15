__all__ = ['build_update_package', 'compare_metadata',
           'load_hashes', 'create_hashes']

def build_update_package(directory:str):
    """
    Return (metadata with hashes, complete).

    example:
    directory:
    -subdir
    --file

    result:
    metadata:
    {
        'directories': [
            'subdir',
        ],
        'files': {
            'subdir/file': hash,
        }
    }
    total:
    {
        'directories': [
            'subdir',
        ],
        'files': {
            'subdir/file': base64 encoded,
        }
    }
    """
    total = {
        'directories': [],
        'files': {},
    }
    metadata = {
        'directories': [],
        'files': {},
    }
    with cd(directory):
        for root, dirs, files in os.walk('.'):
            total['directories'].append(root)
            metadata['directories'].append(root)
            for filename in files:
                fullname = os.path.join(root, filename)
                with open(fullname, 'rb') as f:
                    content = f.read()
                    hashed = hashlib.sha224(content)
                    metadata['files'][fullname] = hashed.hexdigest()
                    total['files'][fullname] = base64.b64encode(content)
        # metadata and total are not serialized + compressed
        # because they may be parsed
        return (metadata, total)




def compare_metadatas(server, client, full_package):
    """Return the differences between the server and client versions.

    Warning: the result may contain a 'del' and a 'add' sections."""

    result = {
        'add': {
            'files': {},
            'directories': []
        },
        'del': {
            'files': [],
            'directories': []
        }
    }

    # list the missing directories
    for d in server['directories']:
        if d not in client['directories']:
            result['add']['directories'].append(d)
    # list the directories to remove
    for d in client['directories']:
        if d not in server['directories']:
            result['del']['directories'].append(d)

    # list the files to add
    # fn = filename, fc = filecontent
    for fn, fc in server['files'].items():
        # if the file is not here or is different
        if client['files'].get(fn) != fc:
            result['add']['files'][fn] = fc

    # list the files to delete
    for fn in client['files']:
        # if the file is not here
        if not server['files'].get(fn, False):
            result['del']['files'].append(fn)

    return result


import bz2
import hashlib
import json
import os

from utils.storage import compress, decompress

def load_hashes(instream):
    return json.loads(decompress(instream.read()))
    # return json.loads(bz2.decompress(instream.read()))

def create_hashes():
    total = {
        'directories': [],
        'files': {},
    }
    for root, _dirs, files in os.walk('.'):
        total['directories'].append(root)
        for filename in files:
            fullname = os.path.join(root, filename)
            with open(fullname, 'rb') as f:
                hashed = hashlib.sha224(f.read()).hexdigest()
                total['files'][fullname] = hashed
    total = compress(json.dumps(total).encode())
    # total = bz2.compress(json.dumps(total).encode())
    return total
