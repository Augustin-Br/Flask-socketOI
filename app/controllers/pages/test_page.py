from flask import render_template
import os

path = os.getcwd()
print("Le répertoire courant est : " + path)

def test():
    #contenue de la page: 
    fname = path + "/app/view/test_page.html"
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    #navbar:
    fname = path + "/app/view/navbar.html"
    with open(fname, 'r', encoding='utf-8') as f:
        navbar = f.read()



    return render_template('template.html', content = content, title = "SAlut la compagnie", navbar = navbar)