from app import app
from flask import render_template, redirect, url_for
from app.forms import ExtractForm

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract", methods=['POST'])
def extract():
    return render_template("extract.html", form=form)

@app.route("/products")
def products():
    return redirect(url_for("product", product_id=product_id))
    return redirect(url_for())

@app.route("/product/<product_id>")
def product(product_id):
    return render_template("product.html", product_id=product_id)

@app.route("/about")
def about():
    return render_template("about.html")