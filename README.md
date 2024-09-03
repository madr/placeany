# Placeany

A quick and simple service for getting pictures of whatever-you-want
for use as placeholders in your designs or code. Just put your image
size (width & height) after the URL and you'll get a placeholder.

There is also a bookmarklet service which enhances sites with many images.

Inspirations:

- https://web.archive.org/web/20110504042732/http://placekitten.com/
- https://web.archive.org/web/20120223050454/http://www.heyben.com/horse_ebookmarklet/.

## Example calls

Generates an image, 200px wide and 300px tall:  
http://localhost:8080/200/300

Generates an image in grayscale, 200px wide and 300px tall:  
http://localhost:8080/g/200/300

## Installation

First, create an image collection.

1. Create the directory `./images`.
1. Get some images, from [Unsplash](https://unsplash.com) or similar.
1. Place images in image directory.

### Run as local web server

1. Go to the code: `cd path/to/holder`. Copy `images` folder to it.
1. Create and activate a virtualenv.
1. Get dependencies in place: `pip install -r requirements.txt`
1. Start the app: `waitress-serve wsgi:app`
1. Go to [http://localhost:8080](http://localhost:8080) in your web browser.
1. Done!

### Run as Container

The most easy and portable way to use this is to use Docker or Podman.
In this build, waitress is used for production readyness. Port 5099 is
instead used.

    podman build .
    podman run -it -p 8080:8080 -v ./images:/app/images <container id>

If you wish to embed images in container as well, use alternate
Containerfile.

    podman build -f Containerfile.aio --build-arg images=./images .
    podman run -it -p 8080:8080 <container id>

### Run behind reverse proxy

A reverse proxy in front of placeany is recommended. An example
Caddyfile is available to make https "just work", but Nginx+certbot
will be equally fine.

## Podman tip: generate systemd files

Make sure to enable lingering user processes.

    loginctl enable-linger $USER

Then, create and change directory to systemd.

    mkdir -p .config/systemd/user
    cd .config/systemd/user

Now, generate the systemd user service.

    podman generate systemd --new -f -n placeany

Your container can now be enabled and started.
