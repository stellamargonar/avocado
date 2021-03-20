from datetime import datetime

import click
from flask import Flask, request
from flask.cli import with_appcontext

from server import settings
from server.helpers import telegram
from server.helpers.db import DBHelper


def init_app(app):
    app.teardown_appcontext(DBHelper.close_db)
    app.cli.add_command(init_db_command)


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Create new tables."""
    DBHelper.init_db()
    click.echo("Initialized the database.")


def create_app(*args, **kwargs):
    app = Flask(__name__, instance_relative_config=True)
    init_app(app)

    @app.route("/metrics", methods=["POST"])
    def piantina_metrics():
        json_data = request.get_json(force=True)
        db_param = {}

        for item in json_data.values():
            db_param.update({item["name"]: item["value"]})

        DBHelper.write_data(**db_param)
        return "ok"

    @app.route("/latest", methods=["GET"])
    def latest_data():
        return DBHelper.get_latest_data()

    @app.route("/report", methods=["GET"])
    def report_data():
        return {
            "data": DBHelper.get_report_data(
                date_from=datetime.strptime("2021-01-01", "%Y-%M-%d"),
                date_to=datetime.now(),
            )
        }

    if settings.TELEGRAM_TOKEN != "":
        # TELEGRAM BOT ENDPOINTS
        @app.route(f"/{settings.TELEGRAM_TOKEN}", methods=["POST"])
        def telegram_respond():
            return telegram.handle_message(request)

        @app.route("/set_webhook", methods=["GET", "POST"])
        def telegram_set_webhook():
            return telegram.set_webhook()

    @app.route("/")
    def index():
        return "."

    return app


app = create_app()
