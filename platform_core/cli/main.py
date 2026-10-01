import typer
from platform_core.observability.logging import get_logger

logger = get_logger("cli")

cli = typer.Typer()

@cli.command()
def hello(name: str):
    logger.info(f"Hello {name}")
    print(f"Hello {name}")

if __name__ == "__main__":
    cli()
