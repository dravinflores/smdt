###############################################################################
#   File: DBLocker.py
#   Author(s): Dravin Flores
#   Date Created: 27 July, 2021
#
#   Purpose: 
#
#   Known Issues:
#
#   Workarounds:
#
#   Updates:
#
###############################################################################

import os
import sys
import uuid
import datetime
from pathlib import Path


class DBLogger:
    def __init__(self, author=None, file=None):
        self.author = author
        self.dropbox_path = Path(__file__).parents[1].resolve()
        self.logging_path = self.dropbox_path / 'DatabaseLogging'

        self.unique_identifier = str(uuid.uuid4())[0:8]
        file_name = self.unique_identifier + '.log'

        if not file:
            self.logging_file = self.logging_path / file_name
        else:
            self.logging_file = self.logging_path / file

        self.logging_path.mkdir(parents=True, exist_ok=True)

        if not self.logging_file.exists():
            self.logging_file.touch()

    def write(self, write_str, external_author=None, mode='normal'):
        current_time = datetime.datetime.now()
        time_str = current_time.isoformat(timespec='seconds', sep=' ')

        if external_author:
            message = f"{time_str}: {mode} [{external_author}] {write_str}\n"
        elif self.author:
            message = f"{time_str}: {mode} [{self.author}] {write_str}\n"
        else:
            message = f"{time_str}: {mode} {write_str}\n"

        with self.logging_file.open('a') as f:
            f.write(message)
