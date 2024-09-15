import os
import random
from io import BytesIO

from flask import Flask, Response, render_template, request, send_file
from flask_caching import Cache
from PIL import Image, ImageOps

app = Flask(__name__)

GREY = "G"
COLOR = "RGB"

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})

app = Flask(__name__)
cache.init_app(app)


def get_cropped_image(x, y, grey=False, retries=0):
    """crops a random image from collection"""
    if retries > 10:
        return None
    options = os.listdir("./images")
    try:
        selection = list(
            filter(
                lambda i: i in range(0, len(options)),
                map(int, request.args.getlist("image")),
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
    im = Image.open(f"images/{im_src}")
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


def make_response(x, y, color_mode=COLOR):
    im = get_cropped_image(x, y, color_mode == GREY)
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


@app.route("/<int:x>/<int:y>")
@cache.cached(1)
def generate(x, y):
    return make_response(x, y, COLOR)


@app.route("/g/<int:x>/<int:y>")
@cache.cached(1)
def generate_grey(x, y):
    return make_response(x, y, GREY)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
