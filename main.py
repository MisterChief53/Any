from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('Any.html')

@app.route('/landingPage')
def landingPage():
    return render_template('landingPage.html')

if __name__ == "__main__":
    app.run(debug=True)

