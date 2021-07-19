#!/usr/local/bin/python3

import argparse
from bs4 import BeautifulSoup
from datetime import datetime
import os
import requests
from urllib.parse import urlparse

def parse_args():
    parser = argparse.ArgumentParser(description="Downloads a given set of URLs")
    parser.add_argument("-m", "--metadata", action="store_true")
    parser.add_argument("urls", nargs="*")
    return parser.parse_args()

def display_metadata(site: str, html: str):
    soup = BeautifulSoup(html, features="html.parser")
    num_links = len(soup.find_all("a"))
    num_images = len(soup.find_all("img"))
    now = datetime.now()
    print(f"site: {site}")
    print(f"num_links: {num_links}")
    print(f"images: {num_images}")
    print(f"last_fetch: {datetime.isoformat(now)}")

def download_url(url: str, show_metadata: bool):
    try:
        r = requests.get(url)
    except Exception as e:
        print(f"Could not download url {url}: {e}")
        return
    if r.status_code != 200:
        print(f"Received status code {r.status_code} for url {url}")
        return

    parsed_url = urlparse(url)
    # TODO(zhan-xiong): handle parsed url path.
    file_name = parsed_url.netloc
    if not file_name.endswith(".html"):
        file_name += ".html"
    with open(file_name, "w") as f:
        f.write(r.text)

    if show_metadata:
        display_metadata(parsed_url.netloc, r.text)

if __name__ == "__main__":
    args = parse_args()
    for url in args.urls:
        download_url(url, show_metadata=args.metadata)
