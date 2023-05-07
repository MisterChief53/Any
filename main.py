from flask import Flask, render_template, url_for, request, redirect
import openai
import os
from dotenv import load_dotenv
load_dotenv()
importanceArray = [False, False, False, False]

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST' and request.form.get('form_name') == 'keywordsForm':
        keywords = []
        keywords.append(request.form["keyword1"])
        keywords.append(request.form["keyword2"])
        keywords.append(request.form["keyword3"])
        keywords.append(request.form["keyword4"])

        description = request.form["Description"]
        '''
        
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
        '''

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un copywriter y escribes publicidad. Tus respuestas estan pensadas para usarse en posts de instagram, y son de mediano tamaño"},
                {"role": "user", "content": generate_prompt(keywords, description, importanceArray)}
                ],
            temperature = 0.6,
            #max_tokens = 3000
            max_tokens = 0
        )
        result = response.choices[0].message.content
        result = result.replace("Hashtags sugeridos:", "")
        result = result.replace("Anuncio:", "")
        print(result)
        return redirect(url_for("index", result=result, _anchor="instaPost"))
        
    
    result = request.args.get("result")
    return render_template('Any.html', result=result)

@app.route('/importance_endpoint', methods=['POST'])
def importance_endpoint():

    try:
        data = request.get_json()
        importance = data['importance']
        id = data['id']
        if id == 'c1' and importance == True:
            importanceArray[0] = True
        elif id == 'c1' and importance == False:
            importanceArray[0] = False
        elif id == 'c2' and importance == True:
            importanceArray[1] = True
        elif id == 'c2' and importance == False:
            importanceArray[1] = False
        elif id == 'c3' and importance == True:
            importanceArray[2] = True
        elif id == 'c3' and importance == False:
            importanceArray[2] = False
        elif id == 'c4' and importance == True:
            importanceArray[3] = True
        elif id == 'c4' and importance == False:
            importanceArray[3] = False
        return {'success': True}
    except Exception as e:
        print(e)
        return {'success': False}
    '''
    data = request.get_json()
    importance = data['importance']
    id = data['id']
    if(id == 'c1' and importance == True):
        importanceArray[0] = True
    elif(id == 'c1' and importance == False):
        importanceArray[0] = False
    elif(id == 'c2' and importance == True):
        importanceArray[1] = True
    elif(id == 'c2' and importance == False):
        importanceArray[1] = False
    elif(id == 'c3' and importance == True):
        importanceArray[2] = True
    elif(id == 'c3' and importance == False):
        importanceArray[2] = False
    elif(id == 'c4' and importance == True):
        importanceArray[3] = True
    elif(id == 'c4' and importance == False):
        importanceArray[3] = False\
    '''


@app.route('/landingPage')
def landingPage():
    return render_template('landingPage.html')

def generate_prompt(keywords, description, importanceArray):
    keyword_list = ""
    for keyword in keywords:
        print(keyword)
        keyword_list = keyword_list + f" {keyword},"
    print(f"Keyword list: {keyword_list}")

    true_indices = [i for i in range(len(importanceArray)) if importanceArray[i]]
    enfasis = ""
    for i in true_indices:
        enfasis = enfasis + f" {keywords[i]},"

    '''
    enfasis = ""
    for i in importanceArray:
        if i == True:
            enfasis = enfasis + f" {keywords[i.index]},"
        elif i == False:
            print(f"{i} is False")
    '''

    prompt = f"""Necesito un anuncio para una empresa que tiene que ver con los siguientes conceptos: {keyword_list}. 
    De esos mismos conceptos, quiero que hagas enfasis en: {enfasis}.
    Breve descripcion de mi empresa: {description}.
    El anuncio publicitario idealmente tiene que ser apto para mostrarse tanto en redes sociales como en algun billboard. 
    Despues de mandarme el parrafo, necesito que me generes unos hashtags que tengan que ver con lo que dice el anuncio. 
    Estos hashtags van a estar en una sola linea, separados por espacios.
    Solamente quiero que pongas los hastags despues del parrafo del anuncio, sin ninguna otra oracion.
    Quiero que mi publicidad siga las tecnicas de venta AIDA, para generar el mayor numero de ventas posibles.
    No quiero frases indicando cada seccion de tu respuesta, esto significa, que tu respuesta no va a contener cosas como \"Hashtags sugeridos:\" o \"Anuncio:\"."""

    print(f"Prompt: {prompt}")

    return prompt

if __name__ == "__main__":
    app.run(debug=True)

