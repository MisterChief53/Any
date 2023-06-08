from flask import Flask, render_template, url_for, request, redirect, send_file
import openai
import os
from dotenv import load_dotenv
import base64
import requests
load_dotenv()
importanceArray = [False, False, False, False]
#imagePath = "./static/img/img_resultado/response_num0.png"
import uuid
from google.cloud import storage

imagePath = ""
filename = ""

credentialsFile = os.environ['GOOGLE_APPLICATION_CREDENTIALS_JSON']
relative_credentials_path = './credentials/' + credentialsFile
absolute_credentials_path = os.path.abspath(relative_credentials_path)
bucket_name = os.environ.get('STORAGE_BUCKET_NAME')
client = storage.Client.from_service_account_json(absolute_credentials_path)

# Iterate over the buckets and print their names
for bucket in client.list_buckets():
    print("Available buckets: " + bucket.name)

#bucket = client.get_bucket(bucket_name)
#this ugly hack gets the first bucket in the list of buckets, probably not the best way to do it
#I tried giving it a string in the .env file but it didn't work
buckets = list(client.list_buckets())
bucket = client.get_bucket(buckets[0].name)


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET', 'POST'])

def index():
    global imagePath
    global bucket
    global bucket_name
    global filename
    #filename = 'a'
    if request.method == 'POST' and request.form.get('form_name') == 'keywordsForm':
        keywords = []
        keywords.append(request.form["keyword1"])
        keywords.append(request.form["keyword2"])
        keywords.append(request.form["keyword3"])
        keywords.append(request.form["keyword4"])

        colors = []
        colors.append(request.form["color1"])
        colors.append(request.form["color2"])
        colors.append(request.form["color3"])

        description = request.form["Description"]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un copywriter y escribes publicidad. Tus respuestas estan pensadas para usarse en posts de instagram, y son de mediano tamaño"},
                {"role": "user", "content": generate_prompt(keywords, description, importanceArray)}
                ],
            temperature = 0.6,
            #max_tokens = 3000
            max_tokens = 3000
        )
        result = response.choices[0].message.content
        result = result.replace("Hashtags sugeridos:", "")
        result = result.replace("Anuncio:", "")
        print(result)

        #### Dream Studio Part ####
        engine_id = "stable-diffusion-v1-5"
        stability_url = f"https://api.stability.ai/v1/generation/{engine_id}/text-to-image"
        stability_api_key = os.getenv("STABILITY_API_KEY")

        color_list = ""
        for color in colors:
            print(color)
            color_list = color_list + f" {color},"
        image_prompt = generate_prompt(keywords, description, importanceArray) + f"The image should also prominently feature these colors: "

        response = requests.post(
            stability_url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {stability_api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": f"{image_prompt}"
                    }
                ],
                "cfg_scale": 7, #How strictly the image fits the prompt
                "clip_guidance_preset": "FAST_BLUE",
                "height": 512,
                "width": 512,
                "samples": 1, #How many Images will it return
                "steps": 30,
            },
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        img_data = response.json()
        filename = str(uuid.uuid4()) + ".png"
        '''
        if 'VERCEL' in os.environ:
            imagePath = ""
        else:
            imagePath = "img/img_resultado/" + filename

        
        for i, image in enumerate(img_data["artifacts"]):
            if 'VERCEL' in os.environ:
                print("Vercel detected, no img")
            else:
                with open("static/" + imagePath, "w+b") as f:
                    f.write(base64.b64decode(image["base64"]))
        '''

        destination_blob_name = "img/img_resultado/" + filename

        #upload the image to the bucket
        blob = bucket.blob(destination_blob_name)
        blob.metadata = {'Content-Disposition' : f'attachment; filename="{filename}"'} 
        #blob.metadata['Content-Disposition'] = f'attachment; filename="{filename}"'
        blob.upload_from_string(base64.b64decode(img_data["artifacts"][0]["base64"]), content_type="image/png")
        blob.make_public()
        #set image path to the url of the image in the bucket
        imagePath = blob.public_url
        
        print(f"filename to send to frontend: {filename}")

        return redirect(url_for("index", result=result, fileName=destination_blob_name, imagePath=imagePath, _anchor="instaPost"))
        
    destination_blob_name = request.args.get("fileName")
    result = request.args.get("result")
    imagePath = request.args.get("imagePath")
    return render_template('Any.html', result=result, imagePath=imagePath, fileName=destination_blob_name)

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


@app.route('/landingPage')
def landingPage():
    return render_template('landingPage.html')

@app.route('/delete_image', methods=['POST'])
def delete_image():
    global bucket
    # Retrieve the filename from the request
    filename = request.form.get('filename')

    # Perform the deletion logic here
    # Delete the file from your Google Cloud Storage bucket using the provided filename
    print(filename)
    print("Filename ^")
    blob = bucket.blob(filename)
    blob.delete()
    print("image deleteddddd")

    return 'Image deleted successfully'

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

