"""Connect to the stored data."""
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from models import Applications, CrashReports, CrashGroups, SystemInfo,\
    Solutions
from models import Base
from classification import classify


class database():
    """Database crash_fixer."""

    def __init__(self):
        """Initialize and return on stdout if success."""
        self.engine = create_engine(
            # database adress
            "postgresql://postgres:postgres@localhost:5433/crash_fixer",
            echo=True
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        print " * DATABASE: Conncetion established"

    def __del__(self):
        """Delete object and connection."""
        self.session.commit()
        self.session.close()
        print " * DATABASE: Connection closed"

    def instertApplication(self, app, commit=False):
        """Send new application info to database."""
        app_sql = Applications(name=app['name'], version=app['version'])
        self.session.add(app_sql)
        self.session.commit()
        return app

    def insertSystemInfo(self, info, commit=False):
        """Send new system info to database."""
        info_sql = SystemInfo(version=info['version'])
        self.session.add(info_sql)
        self.session.commit()
        info['id'] = info_sql.id
        return info_sql

    def insertSolution(self, solution, commit=False):
        """Send new solution to the database."""
        solution_sql = Solutions(details=solution['details'])
        self.session.add(solution_sql)
        if commit:
            self.session.commit()
        return solution_sql

    def insertCrashGroup(self, crash_group, commit=False):
        """Send new crash group to database."""
        self.insertSolution(crash_group['solution'])
        crash_group_sql = CrashGroups(
            solution_id=crash_group['solution']['id']
        )
        self.session.add(crash_group_sql)
        if commit:
            self.session.commit()
        crash_group['id'] = crash_group_sql.id
        return crash_group_sql

    def insertCrashReport(self, crash_report, commit=False, todict=True):
        """"Classify crash_report, insert to the database, return updated."""
        crash_report = crash_report['crash_report']

        # Find crash group
        crash_group_id = classify(crash_report)
        try:
            crash_group = self.session.query(CrashGroups).\
                filter(CrashGroups.id == crash_group_id).one()
        except:
            print "Clusterization error"
            exit(1)

        # Find application data
        app_dict = crash_report['application']
        try:
            application = self.session.query(Applications).\
                filter(Applications.name == app_dict['name']).\
                filter(Applications.version == app_dict['version']).\
                one()
        except NoResultFound:
            application = self.instertApplication(app_dict)

        # Find system_info data
        sys_info_dict = crash_report['system_info']
        try:
            system_info = self.session.query(SystemInfo).\
                filter(SystemInfo.version == sys_info_dict['version']).\
                one()
        except NoResultFound:
            system_info = self.insertSystemInfo(sys_info_dict)

        result = CrashReports(
            exit_code=crash_report['exit_code'],
            stderr_output=crash_report['stderr_output'],
            crash_group=crash_group,
            application=application,
            system_info=system_info
        )
        self.session.add(result)
        if commit:
            self.session.commit()
        if todict:
            return {
                'crash_report_ack': {
                    'crash_report_id': result.id,
                    'crash_report_url': 'vd1/crash_reports/' + str(result.id),
                    'crash_group_id': result.crash_group.id,
                    'crash_group_url': ('vd1/crash_groups/' +
                                        str(result.crash_group.id)),
                    'solution': {
                        "solution_id": result.crash_group.solution.id,
                        "solution_url": ('vd1/solutions/' +
                                         str(result.crash_group.solution.id)),
                        "shell_script": result.crash_group.solution.details
                    }
                }
            }
        else:
            return result

    def getCrashReport(self, crash_report_id, todict=True):
        """Return object representing interesting crash report."""
        result = self.session.query(CrashReports).\
            filter(CrashReports.id == crash_report_id).\
            one()

        if todict:
            return {
                'crash_report': {
                    'crash_report_id': result.id,
                    'crash_report_url': 'vd1/crash_reports/' + str(result.id),
                    'crash_group_id': result.crash_group.id,
                    'crash_group_url': ('vd1/crash_groups/' +
                                        str(result.crash_group.id)),
                    'exit_code': result.exit_code,
                    'stderr_output': result.stderr_output,
                    'application': {
                        'name': result.application.name,
                        'version': result.application.version,
                    },
                    'system_info': {
                        'version': result.system_info.version
                    }

                }
            }
        else:
            return result

database_instance = database()
