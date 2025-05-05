#!/usr/bin/env python3

#  Copyright (c) 2025 Daniel Itiro Tikamori. All rights reserved.
#
#  This software is proprietary, not intended for public distribution, open source, or commercial use. All rights are reserved. No part of this software may be reproduced, distributed, or transmitted in any form or by any means, electronic or mechanical, including photocopying, recording, or by any information storage or retrieval system, without the prior written permission of the copyright holder.
#
#  Permission to use, copy, modify, and distribute this software is strictly prohibited without prior written authorization from the copyright holder.
#
#  Please contact the copyright holder at echo ZnVpd3pjaHBzQG1vem1haWwuY29t | base64 -d && echo for any inquiries or requests for authorization to use the software.

import os
import re  # For regular expressions
import subprocess
import time

import git_filter_repo as gfr

# --- USER CONFIGURATION ---
SENSITIVE_PATTERNS = [
    b"your_sensitive_link_here",  # Example: Replace with your actual sensitive link as bytes
    b"a",  # Example: Add more sensitive strings/bytes here
    # b"a",  # Example: Add more sensitive strings/bytes here
    re.compile(b"email: .*@example\.com", re.IGNORECASE),  # Example: Regular expression
]
PLACEHOLDER_TEXT = b"YOUR_SENSITIVE_DATA"  # The text to replace the sensitive data with
# --------------------------


def replace_sensitive_data(blob, metadata):
    data = blob.data
    modified = False
    for pattern in SENSITIVE_PATTERNS:
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
                hex_id = blob.id.to_bytes(20, "big").hex()
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
            f = gfr.RepoFilter(settings, blob_callback=replace_sensitive_data)
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
                print(
                    "Failed to replace sensitive data after maximum retry attempts due to an unexpected error."
                )
                raise


if __name__ == "__main__":
    main()
