from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import sys
import pandas as pd
import ast

url_df = "https://raw.githubusercontent.com/charlottemllt/ApplicationRecettes/main/Ingredients%20recettes.csv"
df_recettes = pd.read_csv(url_df, delimiter=';')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        num = request.form.get('num')
        session["num"] = num
        return redirect(url_for("choix_recettes"))
    return render_template("index.html")

@app.route('/choix_recettes', methods=['GET', 'POST'])
def choix_recettes():
    if request.method == 'POST':
        for index in range(int(session["num"])):
            num_str = 'recipe' + str(index)
            num = request.form.get(num_str)
            print(num_str, num)
            session[num_str] = num
        return redirect(url_for("liste_de_courses"))
    return render_template("choix_recettes.html",
                           recipes=df_recettes["Nom de la recette"],
                           nombre_recettes=list(range(int(session["num"]))))

#recettes_to_ingredients(['Salade César', 'Tex Mex'])
@app.route('/liste_de_courses', methods=['GET', 'POST'])
def liste_de_courses():
    liste_recettes = [session['recipe' + str(index)] for index in range(int(session["num"]))]
    return render_template("liste_de_courses.html",
                           liste=recettes_to_ingredients(liste_recettes))

@app.route('/<int:ID_recette>', methods=["POST", "GET"])
def display_ingredients(ID_recette):
    info_recette = df_recettes[df_recettes["ID recette"] == ID_recette]
    nom_recette = info_recette["Nom de la recette"].values[0]
    ingredients = ast.literal_eval('{' + str(info_recette["Ingrédients"].values[0]) + '}')
    return render_template("fiche_recette.html", recipe_name=nom_recette, ingredients=ingredients)



@app.route('/input', methods=['GET', 'POST'])
def inputNum():
    if request.method == 'POST':
        num1 = request.form.get('num1')
        session["num1"] = num1
        num2 = request.form.get('num2')
        session["num2"] = num2
        return redirect(url_for("results"))
    return render_template("inputNum.html")

@app.route('/results')
def results():
    if "num1" and "num2" in session:
        num1 = session["num1"]
        num2 = session["num2"]
        old_stdout = sys.stdout
        log_file = open("message.log", "w")
        sys.stdout = log_file
        addNum(num1, num2)
        sys.stdout = old_stdout
        log_file.close()
        with open("message.log", "r") as f:
            content = f.read()
        return app.response_class(content, mimetype='text/plain')
    else:
        return redirect(url_for('inputNum'))

def recettes_to_ingredients(recettes: list):
    ingredients = {}
    df_recettes = pd.read_csv("Ingredients recettes.csv", delimiter=';')
    for recette in recettes:
        liste_ing = ast.literal_eval('{' + str(df_recettes[df_recettes["Nom de la recette"] == recette]["Ingrédients"].values[0]) + '}')
        for key in liste_ing:
            if key in ingredients.keys():
                ingredients[key] = ingredients[key] + liste_ing[key]
            else:
                ingredients[key] = liste_ing[key]
    return ingredients

def addNum(num1, num2):
    num1 = int(num1)
    num2 = int(num2)
    sum = num1 + num2
    print(sum)



if __name__ == '__main__':
    app.run(debug=True)