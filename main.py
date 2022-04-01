from flask import Flask, request, url_for, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/log-in')
def Log_in():
    return render_template('log_in.html')

@app.route('/sing-in')
def Sing_in():
    return render_template('sing_in.html')


if __name__ == "__main__":
    app.run(debug=True)