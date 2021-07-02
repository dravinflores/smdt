import json
import sys
import os

from pathlib import Path

is_in_dropbox_directory = True
debug = True

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# We need to check if the file is being ran from dropbox or if it is being
# ran locally.
if is_in_dropbox_directory:
    DROPBOX_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(DROPBOX_DIR)
else:
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(p)

from sMDT import tube


def create_tube_json(tube_obj, save_path=Path('output')):
    if tube_obj is None:
        return

    if not save_path.exists():
        save_path.mkdir()

    file_path = save_path / f"{tube_obj.m_tube_id}.json"

    with file_path.open('a') as f:
        json.dump(tube_obj.to_dict(), f)


if __name__ == '__main__':
    if debug:
        t = tube.Tube()
        print(t.to_dict())
        create_tube_json(t)
