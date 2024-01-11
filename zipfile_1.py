import os
import zipfile
 
def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".zip"):
                print(file)
                ziph.write(os.path.join(root, file))
 
if __name__ == '__main__':
    with zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir('docs/', zipf)