import secrets

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

from local_spaces import VERSION
from local_spaces.local import local


def create_app():
    app = Flask("local-spaces")
    app.config.update(
        {
            "SECRET_KEY": secrets.token_hex(64),
            "TESTING": False,
            "DEBUG": False,
            "TEMPLATES_AUTO_RELOAD": True,
            "LOCALSPACES_SPACEAPI_ENDPOINT": "https://api.spaceapi.io",
            "LOCALSPACES_LOCAL_ENDPOINT": "https://api.leighhack.org/space.json",
            "LOCALSPACES_DISTANCE": 260,
        }
    )
    app.config.from_prefixed_env()
    register_extensions(app)
    register_blueprints(app)

    @app.context_processor
    def inject_app_info():
        return {"app_version": VERSION}

    return app


def register_extensions(app):
    # Prometheus Metrics
    metrics = PrometheusMetrics.for_app_factory()
    metrics.info("local_spaces_info", "Information about Local-Spaces", version=VERSION)
    metrics.init_app(app)


def register_blueprints(app):
    app.register_blueprint(local)
