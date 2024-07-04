from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Función para buscar activos
def search_assets(domain):
    url = f"http://{domain}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    assets = [{'name': tag.text, 'url': tag['href']} for tag in soup.find_all('a', href=True)]
    
    for asset in assets:
        asset['value'] = len(asset['name'])
        asset['category'] = 'link' if 'http' in asset['url'] else 'internal'
    
    return assets

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    domain = request.form['domain']
    assets = search_assets(domain)
    return render_template('results.html', domain=domain, assets=assets)

if __name__ == '__main__':
    app.run(debug=True)
