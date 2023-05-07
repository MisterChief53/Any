from flask import Flask, render_template, url_for, request, redirect
import openai
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET', 'POST'])


#def index():
#    return render_template('Any.html')

def index():
    if request.method == 'POST' and request.form.get('form_name') == 'keywordsForm':
        keywords = []
        keywords.append(request.form["keyword1"])
        keywords.append(request.form["keyword2"])
        keywords.append(request.form["keyword3"])
        keywords.append(request.form["keyword4"])

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt = generate_prompt(keywords),
            temperature = 0.6,
            max_tokens = 0,
            stop=None
            #max_tokens = 16
        )
        print(response.choices[0].text)
        return redirect(url_for("index", result=response.choices[0].text))
    
    result = request.args.get("result")
    return render_template('tests.html', result=result)

@app.route('/landingPage')
def landingPage():
    return render_template('landingPage.html')

def generate_prompt(keywords):
    prompt = f"""Necesito un anuncio para una empresa que tiene que ver con los siguientes conceptos: {keywords[0]}, {keywords[1]}, {keywords[2]}, {keywords[3]}.
    El anuncio publicitario idealmente tiene que ser apto para mostrarse tanto en redes sociales como en algun billboard. 
    Despues de mandarme el parrafo, necesito que me generes unos hashtags que tengan que ver con lo que dice el anuncio. 
    Estos hashtags van a estar en una sola linea, separados por espacios.
    Solamente quiero que pongas los hastags despues del parrafo del anuncio, sin ninguna otra oracion.
    No quiero frases indicando cada seccion de tu respuesta, esto significa, que tu respuesta no va a contener cosas como \"Hashtags sugeridos:\" o \"Auncio:\"."""

    return prompt

if __name__ == "__main__":
    app.run(debug=True)

