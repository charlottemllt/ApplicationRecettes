import pandas as pd
import ast

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

def main():
    ingredients = recettes_to_ingredients(['Salade César', 'Tex Mex'])
    print(ingredients)
    return 0

if __name__ == "__main__":
    main()