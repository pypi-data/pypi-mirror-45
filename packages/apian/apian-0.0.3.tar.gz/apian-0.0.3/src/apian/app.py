import logging
import os

from flask import Blueprint, Flask, url_for
from flask_restplus import Resource, apidoc

from flask_starter.config import init_logging
from flask_starter.meta import read_version
from flask_starter.web.api import CustomAPI

log = logging.getLogger(__name__)


def _create_blueprint(config, name, prefix):
    """Create blueprint for the generic endpoints.

    :param config: The application configuration.
    :param title: The API title (to be displayed in SwaggerUI).
    :param prefix: The URL prefix for the API (e.g., '/flask-starter/api')

    :rtype: :class:`~flask.Blueprint`.
    """
    # pylint: disable=unused-variable, no-self-use

    title = _title_from_name(name)
    blueprint = Blueprint(prefix, __name__)
    api = CustomAPI(blueprint, title=title, prefix=prefix, doc=prefix + '/')

    @api.route('/info')
    class Info(Resource):
        def get(self):
            """Show information about the service"""
            return {
                'name': name,
                'version': read_version(),
                'config': config['__path']
            }

    @api.route('/health')
    class Health(Resource):
        def get(self):
            """Check the health of the service"""
            return {'status': 'ok'}

    return blueprint


def _create_swagger():
    swagger = apidoc.Apidoc(
        'restplus_custom_doc',
        __name__,
        template_folder='templates',
        static_folder=os.path.dirname(apidoc.__file__) + '/static',
        static_url_path='/swagger')

    @swagger.add_app_template_global
    def swagger_static(filename):
        # pylint: disable=unused-variable
        return url_for('restplus_custom_doc.static', filename=filename)

    return swagger


def create_app(name, config):
    init_logging(config.get('log_config'))
    app = Flask(__name__)
    app.config.update(config)

    app.config['DEBUG'] = config.get('debug', False)
    app.config['ENV'] = config.get('environment', 'production')

    prefix = '/{}/api'.format(name)
    blueprint = _create_blueprint(config, name, prefix)
    swagger = _create_swagger()
    app.register_blueprint(blueprint)
    app.register_blueprint(swagger, url_prefix=prefix)

    return app


def _title_from_name(name):
    return ' '.join(name.split('-')).title()
