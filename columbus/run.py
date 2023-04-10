import typer
import uvicorn


app = typer.Typer()


@app.command()
def run():
    uvicorn.run(
        "columbus.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_includes="*.yml",
    )


if __name__ == "__main__":
    typer.run(run)
