# Autify backend take home test

This is a command-line web page downloader.

## Running

This requires Docker to be able to run.

```
docker build . -t autify-fetch
docker run -it autify-fetch
./fetch.py <arguments>
```

This will run the downloader inside a Dockerized container.

## Libraries used

This uses the `requests` library for downloading pages, and `beautifulsoup4` for parsing html of a page.

## Options

* The `-m` or `--metadata` option will display metadata associated with the site (number of images, number of links, download timestamp).

* The `-s` or `--save_assets` option will download associated assets (CSS stylesheets, JS scripts, images) into a directory, and also rewrite the associated `link`/`script`/`img` tags to point to this directory.
