import zipfile
from pathlib import Path

def extract_zip_files(directory, output_path):
    p = Path(directory)
    for f in p.glob('*.zip'):
        
        with zipfile.ZipFile(f, 'r', metadata_encoding='UTF-8') as archive:
            print(archive.namelist())
            # archive.extractall(path=output_path)
            print(f"Extracted contents from '{f.name}' to '{output_path}' directory.")

if __name__ == '__main__':
    extract_zip_files('./docs', './nuzipped')