"""Models representation for SQLAlchemy."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base()


class Applications(Base):
    """Representation of applications table."""

    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    version = Column(String(250))


class SystemInfo(Base):
    """Representation of system_info table."""

    __tablename__ = 'system_info'
    id = Column(Integer, primary_key=True)
    version = Column(String(250))


class Solutions(Base):
    """Representation of solution table."""

    __tablename__ = 'solutions'
    id = Column(Integer, primary_key=True)
    details = Column(Text())
    connected_groups = relationship("CrashGroups", back_populates="solution")


class CrashGroups(Base):
    """Representation of crash group table."""

    __tablename__ = 'crash_groups'
    id = Column(Integer, primary_key=True)
    solution_id = Column(Integer, ForeignKey('solutions.id'))
    solution = relationship("Solutions", back_populates="connected_groups")
    connected_reports = relationship("CrashReports",
                                     back_populates="crash_group")


class CrashReports(Base):
    """Representation of crash reports table."""

    __tablename__ = 'crash_reports'
    id = Column(Integer, primary_key=True)
    exit_code = Column(Integer)
    stderr_output = Column(String)

    # Foreign keys
    crash_group_id = Column(Integer, ForeignKey('crash_groups.id'))
    crash_group = relationship("CrashGroups",
                               back_populates="connected_reports")

    application_id = Column(Integer, ForeignKey('applications.id'))
    application = relationship("Applications")

    system_info_id = Column(Integer, ForeignKey('system_info.id'))
    system_info = relationship("SystemInfo")
