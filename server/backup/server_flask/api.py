#!/usr/bin/env python
"""Listen to the server requests."""

from flask import Flask
from flask_restful import Api

from resources.helloWorld import HelloWorld
from resources.crashReport import CrashReportById, CrashReportNoId

app = Flask(__name__)
api = Api(app)

# api config
app.config['ERROR_404_HELP'] = False

# api routes
api.add_resource(HelloWorld, '/')
api.add_resource(CrashReportById, '/vd1/crash-reports/<int:crash_report_id>')
api.add_resource(CrashReportNoId, '/vd1/crash-reports/')

if __name__ == '__main__':
    app.run(debug=True)
