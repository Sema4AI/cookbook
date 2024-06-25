# Dropbox client

This package provides a set of actions for working with Dropbox assets. It provides the following actions:

| Action                    | Description                                           |
|---------------------------|-------------------------------------------------------|
| `create_directory`        | Create a remote directory using a full path.          |
| `delete_file`             | Delete a remote file or folder.                       |
| `download_file`           | Download a remote file to a local path.               |
| `get_file_contents`       | Fetch remote file contents. Supports text only.       |
| `list_files`              | List remote files in a directory.                     |
| `put_file_contents`       | Write file contents to a remote path. Supports text only. |
| `upload_file`             | Upload a local file to a remote path.                 |

## Authentication

Currently these actions require a secret that provides the access token for a pre-authenticated Dropbox account.

OAuth will be included in a subsequent addition.
