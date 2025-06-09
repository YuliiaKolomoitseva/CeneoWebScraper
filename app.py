from flask import render_template
from utils import get_product_summaries

# @app.route("/products")
# def product_list():
#     products = get_product_summaries()
#     return render_template("product_list.html", products=products)

# from flask import send_file
# import pandas as pd

@app.route("/download/<product_id>/<filetype>")
def download_opinions(product_id, filetype):
    path = f"app/static/opinions/{product_id}.json"
    df = pd.read_json(path)

    if filetype == "csv":
        filename = f"{product_id}.csv"
        df.to_csv(filename, index=False)
    elif filetype == "xlsx":
        filename = f"{product_id}.xlsx"
        df.to_excel(filename, index=False)
    elif filetype == "json":
        filename = f"{product_id}.json"
        df.to_json(filename, orient="records", indent=2)
    else:
        return "Unsupported file type", 400

    return send_file(filename, as_attachment=True)
