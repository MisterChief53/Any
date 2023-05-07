![Any Landing Page](https://i.imgur.com/RVedPSV.png)
# ANY
<table>
<tr>
<td>
 ANY es pagina web para diseñar el anuncio que quieras, sin importar quien seas.
</td>
</tr>
</table>


## Demo
Here is a working live demo :  https://any-lime.vercel.app/
For this demo, the display of image generation has been disabled, since we 
rely on writing to disk to save the images, and vercel only provides us with 
a write-only environment.

## Installation
Installing the app is very simple. All is needed is to pip install the dependencies listed
on requirements.txt, and set up the following enviromnet variables:
```
FLASK_APP=app
FLASK_ENV=development

# Once you add your API key below, make sure to not share it with anyone! The API key should remain private.
OPENAI_API_KEY=YOUR_API_KEY
STABILITY_API_KEY=YOUR_API_KEY
```


## Built with 

- [OpenAI](https://developers.google.com/chart/interactive/docs/quick_start) - Generación del texto de respuesta.
- [Bootstrap](http://getbootstrap.com/) - Amplia lista de componentes y complementos de Javascript incluidos.
- [Flask](https://flask.palletsprojects.com/en/2.3.x/) - Framework web minimalista en Python.
- [DreamStudio](https://dreamstudio.com/api/) - Generación de imagenes mediante un prompt.


## Team


[Marco Antonio Lopez Arriaga ](https://github.com/marcoantonnlopez) | [Emmauel Florencio Trujillo](https://github.com/EmmanuelFlorencioT) | 
[Jose Neftali Limon Ortiz ](https://github.com/NeftaliLimonOrtiz) | [Angel Yahir Loredo Lopez](https://github.com/MisterChief53)
