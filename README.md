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

