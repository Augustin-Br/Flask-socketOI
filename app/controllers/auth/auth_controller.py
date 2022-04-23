from flask import session, render_template

def auth():
    #check session exist or not to apply modification of navbar

    if not session.get('username'):
        #session not existing
        content = """
                <button type="button" class="btn btn-outline-light">Connectez-vous !</button>
            """
    else:
        #session existing
        content = """
                <button type="button" class="btn btn-outline-light">Mon compte</button>
        """


    return render_template("layout/navbar.html", content=content)