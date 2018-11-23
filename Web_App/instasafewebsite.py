from flask import Flask, render_template, flash, redirect, url_for
from forms import LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = 'e3e78f4328134a6308fa595609ea174e'

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    form = LoginForm()
    if(form.validate_on_submit()):
        if(form.username.data == "instasafeadmin12" and form.password.data == "shootingsarebad!"):
            flash(f"Successfully Logged In {form.username.data}", "success")
            return redirect(url_for("instasafe"))
        else:
            flash("Incorrect Login Info")
    return render_template("home.htm", form=form)

@app.route("/instasafe-logged-in-successfully?=0508436b60727130275c01c80f493267")
def instasafe():
    return render_template("instasafe.htm")

if(__name__ == "__main__"):
    app.run(debug=True)
