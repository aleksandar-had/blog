import os
import click


# the variable current_app can only be used during the handling of a request
# it doesn't work with cli commands since they are registered at start up
# to work around that -> move the custom cli commands inside a function
# the register() function then takes the app instance as an argument
def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    def update():
        """Update all languages."""
        if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
            raise RuntimeError("extract command failed")
        if os.system("pybabel update -i messages.pot -d app/translations"):
            raise RuntimeError("update command failed")
        os.remove("messages.pot")

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system("pybabel compile -d app/translations"):
            raise RuntimeError("compile command failed")

    @translate.command()
    @click.argument("lang")
    def init(lang):
        """Initialize a new language"""
        if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
            raise RuntimeError("extract command failed")
        if os.system(
            "pybabel init -i messages.pot -f app/translations -l " + lang
        ):
            raise RuntimeError("init command failed")
        os.remove("messages.pot")
