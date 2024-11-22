from flask import Flask, request, jsonify, url_for
from wordcloud import WordCloud
import os
import matplotlib.pyplot as plt
from io import BytesIO
import random
import string

app = Flask(__name__)

# Diretório onde as imagens geradas serão salvas
IMAGE_FOLDER = 'static/wordcloud_images'
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Função para gerar nome único para a imagem
def generate_random_filename():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '.png'

@app.route('/generate_wordcloud', methods=['POST'])
def generate_wordcloud():
    # Recebe o texto via JSON
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Texto não fornecido"}), 400

    # Gera a nuvem de palavras
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    # Cria um nome de arquivo único para a imagem
    filename = generate_random_filename()

    # Salva a imagem no diretório estático
    image_path = os.path.join(IMAGE_FOLDER, filename)
    wordcloud.to_file(image_path)

    # Gera a URL para acessar a imagem
    image_url = url_for('static', filename=f'wordcloud_images/{filename}')

    # Retorna o link da imagem gerada
    return jsonify({"image_url": image_url})

if __name__ == '__main__':
    app.run(debug=True)
