#!/usr/bin/env python3

#  Copyright (c) 2025 Daniel Itiro Tikamori. All rights reserved.
#
#  This software is proprietary, not intended for public distribution, open source, or commercial use. All rights are reserved. No part of this software may be reproduced, distributed, or transmitted in any form or by any means, electronic or mechanical, including photocopying, recording, or by any information storage or retrieval system, without the prior written permission of the copyright holder.
#
#  Permission to use, copy, modify, and distribute this software is strictly prohibited without prior written authorization from the copyright holder.
#
#  Please contact the copyright holder at echo ZnVpd3pjaHBzQG1vem1haWwuY29t | base64 -d && echo for any inquiries or requests for authorization to use the software.

import git_filter_repo as gfr
import time
import os
import subprocess
import re
from dotenv import load_dotenv

# --- USER CONFIGURATION ---
ENV_FILE = '.env_sensitive'  # Name of the .env file containing sensitive patterns
PLACEHOLDER_TEXT = b'REDACTED_SENSITIVE_DATA'
# --------------------------

def load_sensitive_patterns(env_file):
    load_dotenv(dotenv_path=env_file)
    patterns = []
    index = 1
    while True:
        key = f'SENSITIVE_PATTERN_{index}'
        pattern = os.getenv(key)
        if pattern is None:
            break
        # Decide if the pattern is a regex or a plain byte string
        if os.getenv(f'SENSITIVE_PATTERN_{index}_REGEX', '').lower() == 'true':
            try:
                patterns.append(re.compile(pattern.encode('utf-8'), re.IGNORECASE))
                print(f"Loaded regex pattern {index}: {pattern}")
            except re.error as e:
                print(f"Error compiling regex pattern {index} '{pattern}': {e}")
        else:
            patterns.append(pattern.encode('utf-8'))
            print(f"Loaded string pattern {index}: {pattern}")
        index += 1
    return patterns

def replace_sensitive_data(blob, metadata, sensitive_patterns):
    data = blob.data
    modified = False
    for pattern in sensitive_patterns:
        if isinstance(pattern, bytes):
            if pattern in data:
                old_data = data
                data = data.replace(pattern, PLACEHOLDER_TEXT)
                if data != old_data:
                    modified = True
        elif isinstance(pattern, re.Pattern):
            old_data = data
            data, num_replaced = re.subn(pattern, PLACEHOLDER_TEXT, data)
            if num_replaced > 0:
                modified = True

    if modified:
        blob.data = data
        try:
            hex_id = blob.id.hex()
        except AttributeError:
            try:
                hex_id = blob.id.to_bytes(20, 'big').hex()
            except AttributeError:
                hex_id = str(blob.id)
        print(f"Replaced sensitive data in blob: {hex_id}")
        return True
    return False

def run_git_command(command):
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e.stderr}")
        return False

def main():
    sensitive_patterns = load_sensitive_patterns(ENV_FILE)
    if not sensitive_patterns:
        print(f"No sensitive patterns found in '{ENV_FILE}'. Exiting.")
        return

    settings = gfr.FilteringOptions.default_options()
    settings.force = True

    cache_dir = os.path.expanduser("~/.cache/git-filter-repo")
    if os.path.exists(cache_dir):
        print(f"Clearing git-filter-repo cache: {cache_dir}")
        import shutil
        try:
            shutil.rmtree(cache_dir)
        except OSError as e:
            print(f"Error clearing cache: {e}")

    print("Expiring git reflog entries...")
    if not run_git_command("git reflog expire --expire=now --all"):
        print("Failed to run git reflog.")
        return

    print("Running git garbage collection...")
    if not run_git_command("git gc --prune=now --aggressive"):
        print("Failed to run git gc.")
        return

    max_retries = 3
    for attempt in range(max_retries):
        try:
            print("Starting git-filter-repo to replace sensitive data...")
            f = gfr.RepoFilter(settings, blob_callback=lambda blob, metadata: replace_sensitive_data(blob, metadata, sensitive_patterns))
            f.run()
            print("Successfully replaced sensitive data in the commit history.")
            break  # Exit loop if successful
        except AssertionError as e:
            print(f"git-filter-repo failed with AssertionError: {e}")
            if attempt < max_retries - 1:
                print(f"Retry attempt {attempt + 1} of {max_retries}...")
                time.sleep(2)
            else:
                print("Failed to replace sensitive data after maximum retry attempts.")
                raise
        except PermissionError as e:
            print(f"git-filter-repo failed with PermissionError: {e}")
            if attempt < max_retries - 1:
                print(f"Retry attempt {attempt + 1} of {max_retries}...")
                time.sleep(2)
            else:
                print("Failed to replace sensitive data after maximum retry attempts.")
                raise
        except Exception as e:
            print(f"An unexpected error occurred during git-filter-repo: {e}")
            if attempt < max_retries - 1:
                print(f"Retry attempt {attempt + 1} of {max_retries}...")
                time.sleep(2)
            else:
                print("Failed to replace sensitive data after maximum retry attempts due to an unexpected error.")
                raise

if __name__ == '__main__':
    main()