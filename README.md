# The Engineering Toolkit

Welcome to my personal repository of scripts, tools, and configurations that help solve common engineering issues and automate tasks.

## Overview

This repository is a collection of utilities I've developed or found useful in my engineering work. It's organized by language and category to make it easy to find the right tool for the job.

## Repository Structure

- `scripts/`: Contains executable scripts organized by task.
  - `git-utilities/`: Scripts for Git-related tasks.
    - `sensitive-data-eliminator.py`
    - `email-replacer.py`
    - `...`
  - `aws-automation/`: Scripts for AWS automation.
    - `ec2-start-instance.py`
    - `s3-upload-file.sh`
    - `...`
  - `network-management/`: Scripts for network tasks.
    - `check-connectivity.py`
    - `port-scanner.sh`
    - `...`
  - `...`
- `tools/`: Contains any standalone tools or binaries.
- `configurations/`: Holds configuration files.
- `documentation/`: For more detailed documentation.
- `examples/`: Example usage scenarios and data.
- `README.md`: The main documentation file.

## Contents

- [Scripts](#scripts)
- [Tools](#tools)
- [Configurations](#configurations)
- [Contributing](#contributing)
- [License](#license)

## Scripts

This directory (`scripts/`) contains various utilities organized by the tasks they perform.

### Git Utilities (`git-utilities/`)

Scripts for managing Git repositories and history.

- [`sensitive-data-eliminator.py`](scripts/git-utilities/sensitive-data-eliminator.py): A general-purpose script to find and replace sensitive data in Git history. [More details](scripts/git-utilities/sensitive-data-eliminator.py).
- [`email-replacer.py`](scripts/git-utilities/email-replacer.py): A script to replace a specific email address in Git commit history. [More details](scripts/git-utilities/email-replacer.py).
- [`...`](scripts/git-utilities/) (Add links and descriptions for other Git-related scripts)

### AWS Automation (`aws-automation/`)

Scripts for automating tasks on Amazon Web Services.

- [`ec2-start-instance.py`](scripts/aws-automation/ec2-start-instance.py): A script to start an EC2 instance.
- [`s3-upload-file.sh`](scripts/aws-automation/s3-upload-file.sh): A Bash script to upload a file to S3.
- [`...`](scripts/aws-automation/)

### Network Management (`network-management/`)

Scripts for network-related tasks.

- [`check-connectivity.py`](scripts/network-management/check-connectivity.py): A script to check network connectivity to a host.
- [`port-scanner.sh`](scripts/network-management/port-scanner.sh): A Bash script to scan ports on a target.
- [`...`](scripts/network-management/)

### File Processing (`file-processing/`)

Scripts for manipulating and processing files.

- [`csv-to-json.py`](scripts/file-processing/csv-to-json.py): A Python script to convert CSV files to JSON.
- [`log-analyzer.sh`](scripts/file-processing/log-analyzer.sh): A Bash script to analyze log files.
- [`...`](scripts/file-processing/)

### System Administration (`system-administration/`)

Scripts for managing local or remote systems.

- [`disk-space-monitor.py`](scripts/system-administration/disk-space-monitor.py): A Python script to monitor disk space.
- [`process-management.sh`](scripts/system-administration/process-management.sh): A Bash script for managing processes.
- [`...`](scripts/system-administration/)

## Tools

This directory (`tools/`) contains any compiled binaries or standalone tools that I find useful.

- [`...`](tools/)

## Configurations

The `configurations/` directory holds configuration files for various applications or services.

- [`...`](configurations/)

## Contributing

If you find these scripts or tools useful and have suggestions or improvements, feel free to open a pull request or submit an issue.

## License

This repository is licensed under proprietary license. See the [LICENSE](LICENSE) file for details.
