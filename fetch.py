#!/usr/local/bin/python3

import argparse
from bs4 import BeautifulSoup
from datetime import datetime
import os
import requests
from urllib.parse import urljoin, urlparse

def parse_args():
    parser = argparse.ArgumentParser(description="Downloads a given set of URLs")
    parser.add_argument("-m", "--metadata", action="store_true")
    parser.add_argument("-s", "--save_assets", action="store_true")
    parser.add_argument("urls", nargs="*")
    return parser.parse_args()

def display_metadata(site: str, soup: BeautifulSoup):
    num_links = len(soup.find_all("a"))
    num_images = len(soup.find_all("img"))
    now = datetime.now()
    print(f"site: {site}")
    print(f"num_links: {num_links}")
    print(f"images: {num_images}")
    print(f"last_fetch: {datetime.isoformat(now)}")
    print("")

def download_assets(base_url: str, soup: BeautifulSoup, assets_dir: str):

    def download_and_rewrite(tag, field: str):
        try:
            tag_url = urljoin(base_url, tag.get(field))

            parsed_tag_url = urlparse(tag_url)
            tag_filename = parsed_tag_url.path
            tag_filename = tag_filename.replace("/", "_")
            tag_path = os.path.join(assets_dir, tag_filename)

            r = requests.get(tag_url)
            with open(tag_path, "wb") as f:
                f.write(r.content)
            tag[field] = tag_path

        except Exception as e:
            print(f"Could not download url {tag_url}: {e}")

    # Images.
    for img in soup.find_all("img"):
        if img.has_attr("src"):
            download_and_rewrite(img, "src")

    # JS.
    for script in soup.find_all("script"):
        if script.has_attr("src"):
            download_and_rewrite(script, "src")

    # CSS.
    for link in soup.find_all("link"):
        if link.has_attr("rel") and link.get("rel") == "stylesheet" and link.has_attr("href"):
            download_and_rewrite(link, "href")

def download_url(url: str, show_metadata: bool, save_assets: bool):
    try:
        r = requests.get(url)
    except Exception as e:
        print(f"Could not download url {url}: {e}")
        return
    if r.status_code != 200:
        print(f"Received status code {r.status_code} for url {url}")
        return

    soup = BeautifulSoup(r.text, features="html.parser")
    parsed_url = urlparse(url)
    
    if show_metadata:
        display_metadata(parsed_url.netloc + parsed_url.path, soup)

    # We replace slashes with underscores, to avoid strange directory traversal attacks.
    file_name = parsed_url.netloc + parsed_url.path
    file_name = file_name.replace("/", "_")

    if save_assets:
        assets_dir = file_name + "_assets"
        os.makedirs(assets_dir, exist_ok=True)
        download_assets(url, soup, assets_dir)

    if not file_name.endswith(".html"):
        file_name += ".html"

    with open(file_name, "w") as f:
        f.write(str(soup))

if __name__ == "__main__":
    args = parse_args()
    for url in args.urls:
        download_url(url, show_metadata=args.metadata, save_assets=args.save_assets)
