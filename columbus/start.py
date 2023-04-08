import typer
import os

app = typer.Typer()

MODELS_NAME = "models.py"


MAIN_CONFIG_NAME = "main.yml"




@app.command()
def start():
    if not os.path.exists(MAIN_CONFIG_NAME):
        with open(MAIN_CONFIG_NAME, "w") as f:
            f.write(
                """\
models: models.py
database:
APIs:
  hello_world:
    table:
    methods: [GET]
            
    """
            )

    if not os.path.exists(MODELS_NAME):
        with open(MODELS_NAME, "w") as f:
            f.write(
                """\
import sqlalchemy
   
    """
            )


if __name__ == "__main__":
    typer.run(start)