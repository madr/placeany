import os
import random
from io import BytesIO

from flask import Flask, Response, render_template, request, send_file
from flask_caching import Cache
from PIL import Image, ImageOps

app = Flask(__name__)

GREY = "G"
COLOR = "RGB"
IMAGE_DIR = "./images"

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})

app = Flask(__name__)
cache.init_app(app)


@cache.memoize(1)
def get_cropped_image(x, y, s, grey=False, retries=0):
    """crops a random image from collection"""
    if retries > 10:
        return None
    options = os.listdir(IMAGE_DIR)
    try:
        selection = list(
            filter(
                lambda i: i in range(0, len(options)),
                map(int, s),
            )
        )
    except ValueError:
        return None
    match len(selection):
        case 0:
            im_src = random.choice(options)
        case 1:
            im_src = options[selection[0]]
        case _:
            im_src = options[random.choice(selection)]
    im = Image.open(f"{IMAGE_DIR}/{im_src}")
    out = BytesIO()
    max_x, max_y = im.size
    if x > max_x and y > max_y:
        return get_cropped_image(x, y, grey, retries + 1)
    im = ImageOps.fit(im, (x, y))
    if grey:
        im = ImageOps.grayscale(im)
    im.save(out, "WEBP", quality=80)
    out.seek(0)
    return out


def make_response(x, y, s, color_mode=COLOR):
    im = get_cropped_image(x, y, s, color_mode == GREY)
    if not im:
        return Response(status=401)
    return send_file(im, mimetype="image/webp")


@app.route("/")
def hello():
    u = request.host
    return render_template("index.html", url=u)


@app.route("/bookmarklet")
def bookmarklet():
    u = request.host
    return render_template("bookmarklet.html", url=u)


@app.route("/images")
def collection():
    c = len(os.listdir(IMAGE_DIR))
    return render_template("list.html", count=c)


@app.route("/<int:x>/<int:y>")
def generate(x, y):
    return make_response(x, y, request.args.getlist("image"), COLOR)


@app.route("/g/<int:x>/<int:y>")
def generate_grey(x, y):
    return make_response(x, y, request.args.getlist("image"), GREY)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
