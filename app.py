from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/buy')
def buy():
    return render_template("buy.html")


@app.route('/payment')
def payment():
     return render_template("Payment.html")



@app.route('/pathorepo')
def pathorepo():
     return render_template("Pathorepo.html")
 
 
@app.route('/bookanappointment')
def bookanappointment():
    return render_template("bookanappointment.html")



if __name__ == '__main__':
    app.run(debug=True)
