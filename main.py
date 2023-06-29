from flask import Flask, render_template, url_for, request, redirect, send_file, session
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
from google.oauth2 import service_account
import logging
import sys
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

# Create a custom handler that directs the log output to stderr
handler = logging.StreamHandler(stream=sys.stderr)

# Create a formatter for the log messages (optional)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the root logger
logging.getLogger().addHandler(handler)

imagePath = ""
filename = ""

logging.warning('Assigning credentials')

google_type = os.environ.get('TYPE')
google_project_id = os.environ.get('PROJECT_ID')
google_private_key_id = os.environ.get('PRIVATE_KEY_ID')

flag = os.environ.get('RANDOM_FLAG')
if flag == "string":
    google_private_key_encoded = os.environ.get('PRIVATE_KEY')
    google_private_key = google_private_key_encoded.replace('\\n', '\n')
else:
    google_private_key = os.environ.get('PRIVATE_KEY')

logging.warning(flag)
logging.warning(google_private_key)

google_client_email = os.environ.get('CLIENT_EMAIL')
google_client_id = os.environ.get('CLIENT_ID')
google_auth_uri = os.environ.get('AUTH_URI')
google_token_uri = os.environ.get('TOKEN_URI')
google_auth_provider_x509_cert_url = os.environ.get('AUTH_PROVIDER_X509_CERT_URL')
google_client_x509_cert_url = os.environ.get('CLIENT_X509_CERT_URL')
google_universe_domain = os.environ.get('UNIVERSE_DOMAIN')

credentialsJson = {
    "type": google_type,
    "project_id": google_project_id,
    "private_key_id": google_private_key_id,
    "private_key": google_private_key,
    "client_email": google_client_email,
    "client_id": google_client_id,
    "auth_uri": google_auth_uri,
    "token_uri": google_token_uri,
    "auth_provider_x509_cert_url": google_auth_provider_x509_cert_url,
    "client_x509_cert_url": google_client_x509_cert_url,
    "universe_domain": google_universe_domain
}

logging.warning('Initiating bucket connection')
logging.warning(credentialsJson)

creds = service_account.Credentials.from_service_account_info(credentialsJson)

client = storage.Client(credentials=creds, project=google_project_id)

# Iterate over the buckets and print their names
for bucket in client.list_buckets():
    print("Available buckets: " + bucket.name)

#this ugly hack gets the first bucket in the list of buckets, probably not the best way to do it
#I tried giving it a string in the .env file but it didn't work
buckets = list(client.list_buckets())
bucket = client.get_bucket(buckets[0].name)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/Any'

secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET', 'POST'])

def index():
    global imagePath
    global bucket
    global filename
    
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
        source_page = request.form["source_page"]
        
        #step 5
        businessName = request.form["businessName"]
        length = request.form["length"]
        tone = request.form["tone"]
        promotion = request.form["promotion"]
    
        if source_page == "Any.html":
            language = request.form.get("language", "Spanish")
            if language == "english":
                system_message = "You are a copywriter and you write advertising. Your responses are intended for use in Instagram posts and are of medium size"
                generate_prompt_func = generate_prompt_eng
            else:
                system_message = "Eres un copywriter y escribes publicidad. Tus respuestas están pensadas para usarse en posts de Instagram y son de tamaño mediano"
                generate_prompt_func = generate_prompt
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
               {"role": "system", "content": system_message},
                {"role": "user", "content": generate_prompt_func(keywords, description, importanceArray, businessName, length, tone, promotion)}
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
        image_prompt = generate_prompt(keywords, description, importanceArray, businessName, length, tone, promotion) + f"The image should also prominently feature these colors: "

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
            #raise Exception("Non-200 response: " + str(response.text))
            error = "Invalid prompt/promp invalido, la IA no acepta las palabras que tienes para generar la imagen/The AI generation for the image does not work with the words you used."
            return redirect(url_for("index", result=result, fileName="", imagePath=imagePath, _anchor="instaPost", source_page=source_page, language=language, error=error))
        else:
            error = False


        img_data = response.json()
        filename = str(uuid.uuid4()) + ".png"

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

        return redirect(url_for("index", result=result, fileName=destination_blob_name, imagePath=imagePath, _anchor="instaPost", source_page=source_page, language=language, error=error))

    destination_blob_name = request.args.get("fileName")
    result = request.args.get("result")
    imagePath = request.args.get("imagePath")
    language = request.args.get("language", "Spanish")
    error = request.args.get("error")

    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id = False

    return render_template('Any.html', result=result, imagePath=imagePath, fileName=destination_blob_name, language=language, user_id=user_id, error=error)
        
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
    
@app.route('/landing')
def landingPage():
    language = 'Spanish'  
    return render_template('landingPage.html', language=language)
   
@app.route('/landing_eng')
def landingPage_eng():
    language = 'english'  
    return render_template('landingPage.html', language=language)

@app.route('/Any')
def Any():
    language = 'Spanish'  
    return render_template('Any.html', language=language)

@app.route('/Any_eng')
def Any_eng():
    language = 'english'  
    return render_template('Any.html', language=language)


@app.route('/iniciaSesion')
def iniciaSesion():
    language = 'Spanish'  
    return render_template('logIn.html', language=language)

@app.route('/logIn')
def logIn():
    language = 'english'  
    return render_template('logIn.html', language=language)

@app.route('/registro')
def registro():
    language = 'Spanish'  
    return render_template('registro.html', language=language)

@app.route('/signUp')
def signUp():
    language = 'english' 
    return render_template('registro.html', language=language)

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username or email already exists in the database
        existing_user = Users.query.filter(
            (Users.username == username) | (Users.email == email)
        ).first()
        if existing_user:
            return 'Username or email already exists'

        new_user = Users(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        #logic for session saving
        user_id = username
        session['user_id'] = user_id

        return redirect(url_for('index'))

    return render_template('signUp.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    #error_message = None
    if request.method == 'POST':
        error_message = False
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        user = Users.query.filter(
            (Users.username == username_or_email) | (Users.email == username_or_email)
        ).first()

        if user and user.check_password(password):
            #return 'Login successful'
            user_id = username_or_email
            session['user_id'] = user_id

            return redirect(url_for('index'))
        else:
            error_message = True
            return redirect(url_for('login', error_message=error_message))

    error_message = request.args.get("error_message")
    return render_template('logIn.html', error_message=error_message)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('Any.html')


def generate_prompt(keywords, description, importanceArray, businessName, length, tone, promotion):
    keyword_list = ""
    for keyword in keywords:
        print(keyword)
        keyword_list = keyword_list + f" {keyword},"
    print(f"Keyword list: {keyword_list}")

    true_indices = [i for i in range(len(importanceArray)) if importanceArray[i]]
    enfasis = ""
    for i in true_indices:
        enfasis = enfasis + f" {keywords[i]},"


    prompt = f"""Necesito un {length} anuncio para una empresa que tiene que ver con los siguientes conceptos: {keyword_list}. 
    De esos mismos conceptos, quiero que hagas enfasis en: {enfasis}.
    Breve descripcion de mi empresa: {description}.
    El nombre de mi empresa es: {businessName}.
    El tono para este anuncio debe ser {tone}.
    Si tenemos una promocion, eso significa que los siguientes parentesis van a tener caracteres entre ellos: ({promotion}). Si tenemos una promocion, porfavor ponla en el anuncio.
    El anuncio publicitario idealmente tiene que ser apto para mostrarse tanto en redes sociales como en algun billboard. 
    Despues de mandarme el parrafo, necesito que me generes unos hashtags que tengan que ver con lo que dice el anuncio. 
    Estos hashtags van a estar en una sola linea, separados por espacios.
    Solamente quiero que pongas los hastags despues del parrafo del anuncio, sin ninguna otra oracion.
    Quiero que mi publicidad siga las tecnicas de venta AIDA, para generar el mayor numero de ventas posibles.
    No quiero frases indicando cada seccion de tu respuesta, esto significa, que tu respuesta no va a contener cosas como \"Hashtags sugeridos:\" o \"Anuncio:\"."""

    print(f"Prompt: {prompt}")

    return prompt

def generate_prompt_eng(keywords, description, importanceArray, businessName, length, tone, promotion):
    keyword_list = ""
    for keyword in keywords:
        print(keyword)
        keyword_list = keyword_list + f" {keyword},"
    print(f"Keyword list: {keyword_list}")

    true_indices = [i for i in range(len(importanceArray)) if importanceArray[i]]
    enfasis = ""
    for i in true_indices:
        enfasis = enfasis + f" {keywords[i]},"

    prompt = f"""I need a {length} advertisement for a company related to the following concepts: {keyword_list}.
    Out of these concepts, I want you to emphasize: {enfasis}.
    Brief description of my company: {description}.
    The name of my business is: {businessName}.
    The tone of this ad should be {tone}.
    If we are holding a promotion, that means that the following parenthesis will have characters between them: ({promotion}). If we do have a promotion, please also advertise it. 
    The advertisement should ideally be suitable for display on both social media and a billboard.
    After you send me the paragraph, I need you to generate some hashtags that are relevant to the content of the advertisement.
    These hashtags should be in a single line, separated by spaces.
    I only want you to place the hashtags after the advertisement paragraph, without any other sentences.
    I want my advertisement to follow the AIDA sales techniques to generate the highest possible number of sales.
    I don't want phrases indicating each section of your response. This means that your response should not contain things like "Suggested hashtags:" or "Advertisement:"."""

    print(f"Prompt: {prompt}")

    return prompt

if __name__ == "__main__":
    app.run(debug=True)

