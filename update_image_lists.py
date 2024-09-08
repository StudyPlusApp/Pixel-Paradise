import os
import json
import requests
from github import Github

# GitHub repository details
REPO_OWNER = "StudyPlusApp"
REPO_NAME = "Pixel-Paradise"
GITHUB_TOKEN = os.environ['IMAGELIST']

# Categories and their corresponding directories
CATEGORIES = {
    "space": "Space",
    "nature": "Nature",
    "aesthetic": "Aesthetic",
    "vapourwave": "VapourWave"
}

def get_image_urls(repo, category):
    contents = repo.get_contents(f"assets/category/{CATEGORIES[category]}")
    image_urls = []
    for content in contents:
        if content.type == "file" and content.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_urls.append(content.download_url)
    return image_urls

def update_json_file(repo, category, image_urls):
    file_path = f"assets/category/{category}_images.json"
    json_content = json.dumps(image_urls, indent=2)
    
    try:
        contents = repo.get_contents(file_path)
        repo.update_file(file_path, f"Update {category} image list", json_content, contents.sha)
        print(f"Updated {file_path}")
    except:
        repo.create_file(file_path, f"Create {category} image list", json_content)
        print(f"Created {file_path}")

def main():
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

    for category in CATEGORIES:
        image_urls = get_image_urls(repo, category)
        update_json_file(repo, category, image_urls)

if __name__ == "__main__":
    main()
