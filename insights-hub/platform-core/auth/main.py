# platform-core/cli/main.py

import os
import click

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


@click.group()
def platform():
    """
    Insights Hub platform CLI.

    Commands:
    - create-app: scaffold a new tenant app
    """
    pass


@platform.command()
@click.argument("name")
def create_app(name: str):
    """
    Scaffold a new tenant application.
    """
    app_dir = os.path.join("apps", name)
    os.makedirs(app_dir, exist_ok=True)

    # Minimal FastAPI app stub
    main_py = os.path.join(app_dir, "main.py")
    with open(main_py, "w", encoding="utf-8") as f:
        f.write(
            'from fastapi import FastAPI\n'
            'from platform_core.auth.middleware import AuthMiddleware\n'
            'from platform_core.config.settings import AppSettings\n'
            'from platform_core.observability.logging import get_logger\n\n'
            'app = FastAPI()\n'
            'settings = AppSettings()\n\n'
            '@app.get("/health")\n'
            'async def health():\n'
            '    return {"status": "ok", "app": settings.app_name}\n'
        )

    click.echo(f"Created app scaffold at {app_dir}")
