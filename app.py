import os
import tempfile
import pandas as pd
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, send_file, abort
)
from utils import get_product_summaries

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        product_id = request.form.get('product_id', '').strip()
        if not product_id:
            flash('Please enter a product ID', 'error')
            return redirect(url_for('extract'))
        
        opinions_path = f'app/static/opinions/{product_id}.json'
        if not os.path.exists(opinions_path):
            flash('Product not found or no opinions extracted yet.', 'error')
            return redirect(url_for('extract'))
        
        return redirect(url_for('product', product_id=product_id))
    
    return render_template('extract.html')

@app.route('/products')
def product_list():
    products = get_product_summaries()
    return render_template('product_list.html', products=products)

@app.route('/product/<product_id>')
def product(product_id):
    opinions_path = f'app/static/opinions/{product_id}.json'
    if not os.path.exists(opinions_path):
        abort(404, description="Product opinions not found.")
    
    df = pd.read_json(opinions_path)
    opinions = df.to_dict(orient='records')
    return render_template('product.html', product_id=product_id, opinions=opinions)

@app.route('/download/<product_id>/<filetype>')
def download_opinions(product_id, filetype):
    opinions_path = f'app/static/opinions/{product_id}.json'
    if not os.path.exists(opinions_path):
        abort(404, description="File not found")

    df = pd.read_json(opinions_path)

    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{filetype}') as tmp:
        filename = tmp.name
        if filetype == 'csv':
            df.to_csv(filename, index=False)
        elif filetype == 'xlsx':
            df.to_excel(filename, index=False)
        elif filetype == 'json':
            df.to_json(filename, orient='records', indent=2)
        else:
            return "Unsupported file type", 400

    response = send_file(filename, as_attachment=True)
    os.remove(filename)
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=e), 404

if __name__ == '__main__':
    app.run(debug=True)

