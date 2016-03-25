"""Retrieve and modify information about crash report(s)."""
from flask import abort
from flask_restful import Resource, reqparse
# Place holder for postgres communication
from database import database_instance as db
import types
import json


class CrashReportById(Resource):
    """Retrieve and modify information about given crash report."""

    def get(self, crash_report_id):
        """Retrieve information about given crash report."""
        report = db.getCrashReport(crash_report_id)
        if report:
            return report
        else:
            abort(404)

    def put(self, crash_report_id):
        """Update information about given crash report."""
        pass

    def delete(self, crash_report_id):
        """Delete information about given crash report."""
        pass


class CrashReportNoId(Resource):
    """Search for and send new crash report."""

    # get_parser parses incoming search requests
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('browser', location='args')
    get_parser.add_argument('version', location='args')

    # post_parser parses incoming new crash reports
    crashReport = types.useSchema('inputCrashReportSchema')
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('crash_report', location='json', type=crashReport)

    def get(self):
        """Search for crash report."""
        args = self.get_parser.parse_args()
        print args
        print args['version']
        print args['browser']
        pass

    def post(self):
        """Post new crash report and return its reference with solution."""
        read_data = self.post_parser.parse_args()
        print json.dumps(read_data, indent=5)
        return db.insertCrashReport(read_data, commit=True), 201
