from flask import Flask
from flask.ext.restful import Api
from jenkins import JenkinsJobBuilderVersionAPI, JenkinsJobBuilderJobAPI

app = Flask(__name__)
api = Api(app)

api.add_resource(JenkinsJobBuilderVersionAPI, '/v1/version')
api.add_resource(JenkinsJobBuilderJobAPI, '/v1/job')

if __name__ == '__main__':
    if not app.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
        app.run(debug=True)
