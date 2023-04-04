
#!/usr/bin/python
#
# Copyright 2022 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
from datetime import datetime, timedelta

COMMIT_SHA: str = os.getenv('GITHUB_SHA')

HEADER: str = 'google/HEADER'

DT_TESTS: str = 'dt/types/google-publisher-tag/google-publisher-tag-tests.ts'
DT_TYPES: str = 'dt/types/google-publisher-tag/index.d.ts'

GOOGLE_TESTS: str = 'google/google-publisher-tag-tests.ts'
GOOGLE_TYPES: str = 'google/index.d.ts'


def have_tests_changed() -> bool:
    return have_files_changed(DT_TESTS, GOOGLE_TESTS)


def have_types_changed() -> bool:
    return have_files_changed(DT_TYPES, GOOGLE_TYPES)


def have_files_changed(old, new) -> str:
    return read_file_without_header(old) != read_file_without_header(new)


def read_file_without_header(file) -> str:
    with open(file) as f:
        contents = f.read()
    
    return contents[contents.find('\n\n'):]


def update() -> None:
    # Use start (Monday) of the current week as minor version, to align with GPT release notes.
    new_version: str = (datetime.today() - timedelta(days=datetime.today().weekday() % 7)).strftime('%Y%m%d')

    with open(HEADER) as input:
        header: str = input.read()

    with open(DT_TYPES, 'w') as out:
        out.write(header.replace('$VERSION', new_version))
        out.write(read_file_without_header(GOOGLE_TYPES))

    with open(DT_TESTS, 'w') as out:
        out.write(f'// Tests for Google Publisher Tag 1.{new_version}\n')
        out.write(f'// Synced from: https://github.com/googleads/google-publisher-tag-types/commit/{COMMIT_SHA}\n')
        out.write(read_file_without_header(GOOGLE_TESTS))


def main() -> None:
    tests_changed: bool = have_tests_changed()
    types_changed: bool = have_types_changed()

    if tests_changed or types_changed:
        print(f'Diff detected @ {COMMIT_SHA}, syncing changes.')
        update()
    else:
        print('No diff detected, exiting.')
        sys.exit(1)


if __name__ == '__main__':
    if COMMIT_SHA:
        main()
    else:
        print('GITHUB_SHA enironment variable not found, exiting.')
        sys.exit(1)
