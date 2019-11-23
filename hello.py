from flask import Flask, render_template

app = Flask(__name__)
@app.route('/Hello')
def hello():
    """ info from db """
    return "Hello world!"


@app.route('/Goodbye')
def see_ya():
    return "See you later!"


@app.route('/sample_template')
def template_demo():
    return render_template('parameters.html',
                           my_header="My Stevens Repository",
                           my_param="My custom parameter")
app.run(debug=True)

