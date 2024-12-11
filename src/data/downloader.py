import os
import requests
from pathlib import Path
from typing import Optional
from bs4 import BeautifulSoup
from tqdm import tqdm
from ..utils.file_utils import create_directory, get_data_directory

class DocumentationDownloader:  
    def __init__(self):
        self.data_dir = get_data_directory() / 'raw'
        create_directory(self.data_dir)

    def download_python_docs(self, version: str = "3.10") -> None:
        """
        Download Python documentation in HTML format.
        Args:
            version: Python version to download documentation for.
        """
        version = str(version)
        # Output directory
        output_dir = self.data_dir / "python_docs"
        create_directory(output_dir)
        
        # Correct Python docs URL
        # Adjust this URL if the structure changes for other versions.
        base_url = f'https://docs.python.org/{version}/archives/python-{version}.12-docs-html.zip'
        
        print(f"Downloading Python {version} documentation from {base_url}...")
        response = requests.get(base_url, stream=True)
        
        if response.status_code == 200:
            zip_path = output_dir / f'python-{version}-docs.zip'
            
            # Download with progress bar
            total_size = int(response.headers.get('content-length', 0))
            with open(zip_path, 'wb') as f, tqdm(
                total=total_size,
                unit='iB',
                unit_scale=True,
                desc="Downloading"
            ) as pbar:
                for data in response.iter_content(chunk_size=1024):
                    size = f.write(data)
                    pbar.update(size)
            
            print(f"Downloaded Python documentation to {zip_path}")
        else:
            print(f"Failed to download Python documentation. Status code: {response.status_code}")

    def download_django_docs(self, version: str = "4.2") -> None:
        """
        Download Django documentation from GitHub.
        Args:
            version: Django version to download documentation for
        """
        version = str(version)

        output_dir = self.data_dir / 'django_docs'
        create_directory(output_dir)
        
        # Django docs GitHub URL
        base_url = f'https://github.com/django/django/tree/stable/{version}.x/docs/'
        
        print(f"Downloading Django {version} documentation...")
        
        # First, get the index page to find all .txt files
        cert_path = "/home/murad/anaconda3/envs/rag/ssl/cert.pem"
        response = requests.get(f'{base_url}contents.txt', verify=cert_path)
        
        if response.status_code == 200:
            # Parse and download each .txt file
            for line in response.text.split('\n'):
                if line.endswith('.txt'):
                    file_name = line.strip()
                    file_url = f'{base_url}{file_name}'
                    
                    response = requests.get(file_url)
                    if response.status_code == 200:
                        file_path = output_dir / file_name
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        print(f"Downloaded {file_name}")
                    else:
                        print(f"Failed to download {file_name}")
        else:
            print(f"Failed to access Django documentation. Status code: {response.status_code}")

def main():
    """Main function to download all documentation."""
    downloader = DocumentationDownloader()
    # downloader.download_python_docs()
    downloader.download_django_docs()

if __name__ == "__main__":
    main()
