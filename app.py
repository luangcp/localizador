from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para receber a localização
@app.route('/coletar_localizacao', methods=['POST'])
def coletar_localizacao():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    timestamp = datetime.datetime.now().isoformat()

    # Aqui você pode salvar em um arquivo, banco de dados, etc.
    with open("localizacoes.txt", "a") as f:
        f.write(f"{timestamp} - LAT: {latitude}, LNG: {longitude}\n")

    print(f"Localização recebida: {latitude}, {longitude}")
    return {"status": "sucesso"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
