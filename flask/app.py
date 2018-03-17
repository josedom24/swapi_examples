from flask import Flask, url_for, request, render_template
app = Flask(__name__)   

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/peliculas/')
def peliculas():
    
    return 'Lista de artículos'	

if __name__ == '__main__':
    app.run()
