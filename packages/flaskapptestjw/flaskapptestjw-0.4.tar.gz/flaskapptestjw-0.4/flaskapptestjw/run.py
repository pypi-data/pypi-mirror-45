from flask import Flask, request, render_template,redirect, Response


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def run():
    app.run(host='0.0.0.0', port=3456)

if __name__ == '__main__':
    run()