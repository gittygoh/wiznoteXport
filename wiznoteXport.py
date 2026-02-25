#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

class WizNoteExporter:
    """
    Exporter for WizNote.
    """

    def __init__(self, user_id: str, password: str, api_url: str, output_folder: str):
        self.user_id = user_id
        self.password = password
        self.api_url = api_url.rstrip('/')
        self.output_folder = Path(output_folder)
        self.session = requests.Session()
        self.token: Optional[str] = None
        self.kb_server: Optional[str] = None
        self.kb_guid: Optional[str] = None

    def _make_request(self, method: str, url: str, **kwargs) -> Any:
        headers = {'X-Wiz-Token': self.token} if self.token else {}
        try:
            response = self.session.request(method, url, headers=headers, timeout=30, **kwargs)
            response.raise_for_status()
            return response.json().get('result')
        except requests.exceptions.RequestException as e:
            print(f" ✗ API request failed: {e}")
            return None
        except json.JSONDecodeError:
            print(f" ✗ Failed to decode JSON from response: {response.text}")
            return None

    def login(self) -> None:
        print("\n[*] Logging in...")
        url = f"{self.api_url}/as/user/login"
        payload = {'userId': self.user_id, 'password': self.password}
        data = self._make_request('POST', url, json=payload)
        if data and data.get('token') and data.get('kbServer') and data.get('kbGuid'):
            self.token = data['token']
            self.kb_server = data['kbServer'].rstrip('/')
            self.kb_guid = data['kbGuid']
            print(" ✓ Login successful!")
        else:
            raise Exception("Login failed. Check credentials and API URL.")

    def get_folders(self) -> List[str]:
        print("\n[*] Getting folders...")
        if not self.kb_server: raise Exception("Not logged in.")
        url = f"{self.kb_server}/ks/category/all/{self.kb_guid}"
        folders = self._make_request('GET', url)
        if folders and isinstance(folders, list):
            print(f" ✓ Found {len(folders)} folder(s)")
            for folder in folders:
                if folder!= '/': print(f" - {folder}")
            return folders
        else:
            print(" No folders found.")
            return []

    def get_notes_in_folder(self, folder_path: str) -> List[Dict[str, Any]]:
        if not self.kb_server: raise Exception("Not logged in.")
        url = f"{self.kb_server}/ks/note/list/category/{self.kb_guid}"
        params = {'category': folder_path, 'start': 0, 'count': 100, 'orderBy': 'created', 'ascending': 'desc'}
        all_notes = []
        while True:
            params['start'] = len(all_notes)
            result = self._make_request('GET', url, params=params)
            if not result or not isinstance(result, list):
                break
            all_notes.extend(result)
            if len(result) < params['count']:
                break
        return all_notes

    def download_note(self, doc_guid: str) -> Optional[str]:
        """
        Download the raw HTML content of a note.
        """
        if not self.kb_server or not self.token: raise Exception("Not logged in.")
        url = f"{self.kb_server}/ks/note/view/{self.kb_guid}/{doc_guid}"
        headers = {'X-Wiz-Token': self.token}
        try:
            response = self.session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            # FINAL FIX 2: Return the raw text content, not JSON
            return response.text
        except requests.exceptions.RequestException as e:
            # This is where the user's error message comes from.
            print(f" ✗ API request failed for note {doc_guid}: {e}")
            return None

    def sanitize_filename(self, filename: str) -> str:
        sanitized = re.sub(r'[\\/*?:"<>|]', "_", filename)
        sanitized = sanitized.strip('.')
        return sanitized[:200] or 'Untitled'

    def create_local_folder(self, folder_path: str) -> Path:
        safe_path_parts = [self.sanitize_filename(part) for part in Path(folder_path).parts if part not in ('/', '\\')]
        safe_path = Path(*safe_path_parts)
        full_path = self.output_folder / safe_path
        full_path.mkdir(parents=True, exist_ok=True)
        return full_path

    def export_note(self, note_info: Dict[str, Any], folder_path: Path) -> bool:
        doc_guid = note_info.get('docGuid')
        title = note_info.get('title', 'Untitled')

        if not doc_guid:
            print(f" ✗ Note '{title}' has no GUID, skipping.")
            return False

        try:
            # The function now returns the HTML content directly
            html_content = self.download_note(doc_guid)
            
            # If download failed or returned empty content, skip
            if not html_content:
                print(f" ✗ Failed to download content for note '{title}', skipping")
                return False

            safe_title = self.sanitize_filename(title)
            filename = f"{safe_title}.html"
            filepath = folder_path / filename
            
            counter = 1
            while filepath.exists():
                filepath = folder_path / f"{safe_title}_{counter}.html"
                counter += 1

            filepath.write_text(html_content, encoding='utf-8')
            print(f" ✓ Exported '{title}'")
            return True
        except Exception as e:
            print(f" ✗ Failed to export note '{title}': {e}")
            return False

    def export_by_folders(self, folders: List[str]) -> None:
        print(f"\n{'='*60}\nExporting Notes by Folders\n{'='*60}")
        for folder_path in sorted(folders):
            if folder_path == '/': continue
            print(f"\n[*] Processing folder: {folder_path}")
            local_folder = self.create_local_folder(folder_path)
            notes = self.get_notes_in_folder(folder_path)
            if not notes:
                print(" No notes in this folder")
                continue
            print(f" Found {len(notes)} note(s), exporting...")
            for note in notes:
                self.export_note(note, local_folder)

    def run(self) -> None:
        print(f"\n{'#'*60}\n# WizNote Export Tool\n{'#'*60}")
        self.output_folder.mkdir(parents=True, exist_ok=True)
        print(f"\n[*] Output folder: {self.output_folder.resolve()}")
        try:
            self.login()
            folders = self.get_folders()
            if folders:
                self.export_by_folders(folders)
            else:
                print("\n[!] No folders found to export")
            print(f"\n{'='*60}\nExport Complete!\n{'='*60}\n")
        except KeyboardInterrupt:
            print(f"\n\n[!] Export cancelled by user")
        except Exception as e:
            print(f"\n\n[!] Error: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='WizNote Export Tool')
    parser.add_argument('-u', '--user', required=True, help='WizNote login ID')
    parser.add_argument('-p', '--password', required=True, help='WizNote password')
    parser.add_argument('-o', '--output', required=True, help='Output folder path')
    parser.add_argument('-a', '--api_url', required=True, help='URL for the WizNote API server')
    return parser.parse_args()

def main():
    args = parse_arguments()
    exporter = WizNoteExporter(user_id=args.user, password=args.password, api_url=args.api_url, output_folder=args.output)
    exporter.run()

if __name__ == '__main__':
    main()