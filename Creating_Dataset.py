# First Section: Importing Libraries
import os
import requests
from bs4 import BeautifulSoup

# Second Section: Declare important variables
google_image = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&"

user_agent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}

# Third Section: Define folder names
saved_folder1 = 'sunflower'
saved_folder2 = 'marigold'


def main():
    # Create folders if they don't exist
    if not os.path.exists(saved_folder1):
        os.mkdir(saved_folder1)
    if not os.path.exists(saved_folder2):
        os.mkdir(saved_folder2)
    
    # Download images for each folder
    download_images(saved_folder1)
    download_images(saved_folder2)


# Fourth Section: Build the download function with folder parameter
def download_images(folder_name):
    data = input(f'What images would you like to download into "{folder_name}"? ')
    n_images = int(input('How many images do you want? '))

    print('searching...')

    search_url = google_image + 'q=' + data
    response = requests.get(search_url, headers=user_agent)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # Find all image elements
    results = soup.findAll('img', {'class': 'rg_i Q4LuWd'})

    # Collect image links
    count = 1
    links = []
    for result in results:
        try:
            link = result['data-src']
            links.append(link)
            count += 1
            if count > n_images:
                break
        except KeyError:
            continue

    print(f"Downloading {len(links)} images into folder '{folder_name}'...")

    # Download each image and save to the specified folder
    for i, link in enumerate(links):
        response = requests.get(link)
        image_name = f"{folder_name}/{data}{i+1}.jpg"

        with open(image_name, 'wb') as fh:
            fh.write(response.content)


# Fifth Section: Run your code
if __name__ == "__main__":
    main()
