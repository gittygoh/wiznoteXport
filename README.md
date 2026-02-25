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
| `-a`, `--api_url` | `SERVER_URL`  | Yes      | The full URL for your WizNote API server. For the official cloud service, this is typically `https://as.wiz.cn`. For private servers, this will be your server's address (e.g., `http://192.168.1.100:7890`). |

## Examples

Here are several examples demonstrating how to use the script in different scenarios.

### 1. Basic Cloud Export

This is the most common use case for exporting from the official WizNote cloud service. It saves the notes to a `wiz-backup` folder in the current directory.
```
python wiz_export.py -u "my.email@example.com" -p "MySecretPassword123" -o "./wiz-backup" -a "https://as.wiz.cn"
```

### 2. Export from a Private, Self-Hosted Server

If you are running your own WizNote server on your local network, you need to point the script to its local IP address. This example saves the backup to a specific directory on a Windows machine.
```
python wiz_export.py --user "admin" --password "private_server_pass" --output "C:\Backups\WizNote" --api_url "http://192.168.1.50"
```

### 3. Saving to a Mounted Drive on Linux

This example shows how to export notes to an external USB drive or network share that has been mounted to the file system on a Linux machine.
```
python wiz_export.py -u "user@mydomain.com" -p "password" -o "/media/usb-drive/MyWizNotes" -a "http://my-wiz-server.local"
```

### 4. Backing up to a "Notes" Folder in your Home Directory

This example uses a relative path (`~/Documents/Notes`) to save the export into a `Notes` folder located inside your user's `Documents` directory. The `~` symbol is automatically expanded by the shell to your home directory.
```
python wiz_export.py -u "my.email@example.com" -p "MyP@ssw0rd" -o "~/Documents/Notes" -a "https://as.wiz.cn"
```

### 5. Simple Export to the Current Folder

By using `.` as the output path, this command tells the script to create the backup folders and files directly inside the directory where you are currently running the command.
```
python wiz_export.py -u "user@work.com" -p "P@ssw0rd!" -o "." -a "https://as.wiz.cn"
```

