import requests
import os
import zipfile
import shutil
import json
from datasets import load_dataset

# Class to download the dataset from the given URL and create the dataset

class CreateImageDataset(): 
    def __init__(self, url, destination_folder, images_folder):
      self.url = url
      self.destination_folder = destination_folder
      self.images_folder = images_folder
    
    def downloader(self):
        repo_url = self.url
        destination = self.destination_folder
        # Check if the folder already exists

        if not os.path.exists(destination):
            os.makedirs(destination)

        response = requests.get(repo_url, allow_redirects=True)

        if response.status_code == 200:
            # Save the archive with a descriptive filename
            filename = f"{destination}/{repo_url.split('/')[-1]}"
            with open(filename, 'wb') as f:
                f.write(response.content)

            # Extract the archive directly within the destination folder (avoiding temporary directories)
            try:
                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    zip_ref.extractall(destination)
                print("Folder downloaded and extracted to:", destination)
            except zipfile.BadZipFile:
                print(f"Error: Downloaded file {filename} is not a valid ZIP archive.")
            except Exception as e:
                print(f"Failed to unzip archive: {e}")

        else:
            print(f"Failed to download archive. Status code: {response.status_code}")


    def create_dictionary(self):
        captions = []
        for root, _, files in os.walk(self.destination_folder):
            for filename in files:
                if filename.endswith('_Description.txt'):
                    vegetable_type = os.path.splitext(filename)[0].replace('_Description', '')
                    image_file = os.path.join(root, f"{vegetable_type}_Iconic.jpg")

                    # Combine checks and handle both file existence and destination copy in one step
                    if os.path.isfile(image_file) and not os.path.exists(os.path.join(self.images_folder, os.path.basename(image_file))):
                        # Create destination folder if necessary
                        os.makedirs(self.images_folder, exist_ok=True)
                        shutil.copy(image_file, self.images_folder)

                    with open(os.path.join(root, filename), 'r') as f:
                        description_text = f.read()

                    captions.append({
                        "file_name": os.path.basename(image_file),
                        "text": description_text
                    })

        return captions
    

    def create_dataset(self, captions):
        with open(self.images_folder + "/metadata.jsonl", 'w') as f:
            for item in captions:
                f.write(json.dumps(item) + "\n")
        
        dataset = load_dataset("imagefolder", data_dir=self.images_folder, split="train")
        print("Dataset created successfully")
        print("Dataset info: ", dataset)
        return dataset
