from flask import render_template

def rule():
    navbar = render_template("layout/navbar.html")

    content = render_template("pages/rule_page.html")

    return render_template("template.html", title="Accueil", navbar = navbar, content = content)


