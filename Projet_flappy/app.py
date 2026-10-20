from flask import Flask, render_template
import subprocess
import sys
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jeu')
def jeu():
    return render_template('jeu.html')

@app.route('/classement')
def classement():
    return render_template('classement.html')

@app.route('/lancer')
def lancer():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, 'main.py')
    subprocess.Popen([sys.executable, main_script], cwd=script_dir)
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)