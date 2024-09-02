# What is this?

A quick and simple service for getting pictures of whatever-you-want
for use as placeholders in your designs or code. Just put your image
size (width & height) after the URL and you'll get a placeholder.

Similar URL API as [Placekitten](http://placekitten.com).

There is also a bookmarklet service which works the same as
[Horse_ebookmarklet](http://www.heyben.com/horse_ebookmarklet/).

## Installation

For local development builds, not suitable for production:

1. Go to the code: `cd path/to/holder`
1. Create and activate a virtualenv.
1. Get dependencies in place: `pip install -r requirements.txt`
1. Set up a collection of images.
   a. Create the directory `./images`.
   b. Get some images, from [Unsplash](https://unsplash.com) or similar.
   c. Place images in image directory.
1. Start the app: `flask run .`
1. Go to [http://localhost:5000](http://localhost:5000) in your web browser.
1. Done!

### Run as Container

The most easy and portable way to use this is to use Docker or Podman.
In this build, waitress is used for production readyness. Port 5099 is
instead used.

    podman build .
    podman run -it -p 5099:5099 -v ./images:/app/images <container id>

If you wish to embed images in container as well, use alternate
Containerfile.

    podman build -f Containerfile.aio --build-arg images=./images .
    podman run -it -p 5099:5099 <container id>

## Example calls

    # generates an image, 200px wide and 300px tall
    http://localhost:5000/200/300

    # generates an image in grayscale, 200px wide and 300px tall
    http://localhost:5000/g/200/300
