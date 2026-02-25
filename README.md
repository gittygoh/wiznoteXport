# wiznoteXport - A WizNote Export Tool

A command-line utility to export all notes from a self-hosted or cloud WizNote account into local HTML files. This script preserves the folder structure and can also export notes organized by tags.

## Description

This tool connects to a specified WizNote server, authenticates with your user credentials, and systematically downloads all of your notes. It is designed to create a complete, readable, and offline backup of your data.

### Features

-   **Full Account Backup**: Downloads all notes from your account.
-   **Preserves Folder Structure**: Recreates your WizNote folder hierarchy on your local disk.
-   **Saves as HTML**: Each note is saved as a standard HTML file, viewable in any web browser.
-   **Handles Naming Conflicts**: Automatically renames files to avoid overwriting notes with the same title.
-   **Sanitizes Filenames**: Removes characters that are incompatible with most file systems, ensuring a smooth export.
-   **Supports Self-Hosted Servers**: Works with both the official WizNote cloud service and private, self-hosted instances by allowing you to specify a custom API server URL.

## Usage

To run the script, you must provide your login credentials, the output directory, and the API server URL via the command line.

### Parameters

| Flag            | Parameter     | Required | Description                                                                                             |
| --------------- | ------------- | -------- | ------------------------------------------------------------------------------------------------------- |
| `-u`, `--user`  | `USER_ID`     | Yes      | Your WizNote login ID (usually your email address or username).                                         |
| `-p`, `--password`| `PASSWORD`    | Yes      | Your WizNote account password.                                                                          |
| `-o`, `--output`  | `FOLDER_PATH` | Yes      | The local path where the exported notes and folders will be saved. The directory will be created if it does not exist. |
| `-a`, `--api_url` | `SERVER_URL`  | Yes      | The full URL for your WizNote API server. For the official cloud service, this is typically `https://as.wiz.cn`. For private servers, this will be your server's address (e.g., `http://192.168.1.100`). |

## Examples

Here are several examples demonstrating how to use the script in different scenarios.

### 1. Basic Cloud Export

This is the most common use case for exporting from the official WizNote cloud service. It saves the notes to a `wiz-backup` folder in the current directory.
