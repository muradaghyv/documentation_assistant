import requests
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
        
        # print(f"Downloading Python {version} documentation from {base_url}...")
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
            
            # print(f"Downloaded Python documentation to {zip_path}")
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
        
        # print(f"Downloading Django {version} documentation...")
        
        # First, get the index page to find all .txt files
        cert_path = "/home/murad/anaconda3/envs/rag/ssl/cacert.pem"
        response = requests.get(f'https://raw.githubusercontent.com/django/django/refs/heads/stable/{version}.x/docs/contents.txt', verify=cert_path)

        if response.status_code == 200:
            for line in response.text.split("\n"):
                line = line.strip()
                new_url = f"https://raw.githubusercontent.com/django/django/refs/heads/stable/4.2.x/docs/{line}.txt"

                response = requests.get(new_url, verify=cert_path)

                if response.status_code == 200:
                    if "/" in line:
                        folder_name = new_url.split("/")[-2].strip()
                        file_name = new_url.split("/")[-1].strip()
                        file_url = f"{output_dir}/{folder_name}_{file_name}"
                    else:
                        file_name = new_url.split("/")[-1].strip()
                        file_url = f"{output_dir}/{file_name}"

                    with open(file_url, "w") as f:
                        f.write(response.text)
                    
                    for new_line in response.text.split("\n"):
                        fold = new_url.split("/")[:-1]
                        fold = "/".join(fold)
                        filee = new_line.strip()
                        url_1 = f"{fold}/{filee}.txt"
                        new_response = requests.get(url_1, verify=cert_path)
                        if new_response.status_code == 200:
                            new_file_name = url_1.split("/")[-1].strip()
                            new_file_url = f"{output_dir}/{new_file_name}"

                            with open(new_file_url, "w") as f:
                                f.write(new_response.text)
