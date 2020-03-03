# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Date, DateTime, Float, ForeignKey, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, ENUM, INTEGER, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, SMALLINT, TEXT, TINYINT, TINYTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_CurrentReservations = Table(
    'CurrentReservations', metadata,
    Column('userID', INTEGER(11), server_default=text("'0'")),
    Column('lastName', String(100)),
    Column('firstName', String(100)),
    Column('riverName', String(100)),
    Column('sectionName', String(100)),
    Column('resDate', Date),
    Column('linked', INTEGER(11), server_default=text("'0'"))
)


class Fish(Base):
    __tablename__ = 'Fish'

    fishID = Column(INTEGER(11), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(LONGTEXT)
    imgURL = Column(String(200))


class Membership(Base):
    __tablename__ = 'Membership'

    membershipID = Column(INTEGER(11), primary_key=True)
    userID = Column(ForeignKey('User.userID'), index=True)
    wp_MembershipKey = Column(String(100))
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)
    createdByID = Column(ForeignKey('User.userID'), nullable=False, index=True)
    createdDate = Column(Date, nullable=False)
    modifiedByID = Column(ForeignKey('User.userID'), nullable=False, index=True)
    modifiedDate = Column(Date, nullable=False)

    User = relationship('User', primaryjoin='Membership.createdByID == User.userID')
    User1 = relationship('User', primaryjoin='Membership.modifiedByID == User.userID')
    User2 = relationship('User', primaryjoin='Membership.userID == User.userID')


class Reservation(Base):
    __tablename__ = 'Reservation'

    reservationID = Column(INTEGER(11), primary_key=True)
    userID = Column(ForeignKey('User.userID'), nullable=False, index=True)
    sectionID = Column(ForeignKey('Section.sectionID'), nullable=False, index=True)
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)
    dateScheduled = Column(DateTime, nullable=False)
    canceled = Column(INTEGER(11), nullable=False)
    isLinked = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    linkedReservationID = Column(INTEGER(11))

    Section = relationship('Section')
    User = relationship('User')


class River(Base):
    __tablename__ = 'River'

    riverID = Column(INTEGER(11), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(LONGTEXT)
    imgURL = Column(String(200))
    colorHex = Column(String(100))
    centerLat = Column(Float(asdecimal=True))
    centerLong = Column(Float(asdecimal=True))
    centerCoords = Column(Float(asdecimal=True))
    active = Column(INTEGER(11), server_default=text("'1'"))
    cityState = Column(String(45))


class RiverFish(Base):
    __tablename__ = 'RiverFish'

    riverFishID = Column(INTEGER(11), primary_key=True)
    riverID = Column(ForeignKey('River.riverID'), nullable=False, index=True)
    fishID = Column(ForeignKey('Fish.fishID'), nullable=False, index=True)
    seq = Column(INTEGER(11), nullable=False, server_default=text("'1'"))
    percentage = Column(INTEGER(11))

    Fish = relationship('Fish')
    River = relationship('River')


class Section(Base):
    __tablename__ = 'Section'

    sectionID = Column(INTEGER(11), primary_key=True)
    riverID = Column(ForeignKey('River.riverID'), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    reservationLimit = Column(INTEGER(11), nullable=False)
    hexColor = Column(String(100), nullable=False)
    active = Column(INTEGER(11), nullable=False, server_default=text("'1'"))

    River = relationship('River')


t_TodaysReservations = Table(
    'TodaysReservations', metadata,
    Column('userID', INTEGER(11), server_default=text("'0'")),
    Column('lastName', String(100)),
    Column('firstName', String(100)),
    Column('riverName', String(100)),
    Column('sectionName', String(100)),
    Column('resDate', Date),
    Column('linked', INTEGER(11), server_default=text("'0'"))
)


class User(Base):
    __tablename__ = 'User'

    userID = Column(INTEGER(11), primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    lastName = Column(String(100))
    firstName = Column(String(100))
    email = Column(String(100))
    createdDate = Column(Date, nullable=False)
    createdByID = Column(ForeignKey('User.userID'), nullable=False, index=True)
    modifiedDate = Column(Date, nullable=False)
    modifiedByID = Column(ForeignKey('User.userID'), nullable=False, index=True)
    adminFlag = Column(INTEGER(11), server_default=text("'0'"))
    wp_userID = Column(BIGINT(20))
    password = Column(String(100), nullable=False)
    activeToday = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    currentMembershipID = Column(ForeignKey('Membership.membershipID'), index=True)
    forcePasswordChange = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    reservationLimit = Column(INTEGER(10), nullable=False, server_default=text("'3'"))

    parent = relationship('User', remote_side=[userID], primaryjoin='User.createdByID == User.userID')
    Membership = relationship('Membership', primaryjoin='User.currentMembershipID == Membership.membershipID')
    parent1 = relationship('User', remote_side=[userID], primaryjoin='User.modifiedByID == User.userID')


class Waypoint(Base):
    __tablename__ = 'Waypoint'

    waypointID = Column(INTEGER(11), primary_key=True)
    riverID = Column(ForeignKey('River.riverID'), nullable=False, index=True)
    sectionID = Column(ForeignKey('Section.sectionID'), nullable=False, index=True)
    latitude = Column(Float(asdecimal=True), nullable=False)
    longitude = Column(Float(asdecimal=True), nullable=False)
    seq = Column(INTEGER(11), nullable=False)

    River = relationship('River')
    Section = relationship('Section')


class AdminUser(Base):
    __tablename__ = 'admin_user'

    admin_user_id = Column(INTEGER(6), primary_key=True)
    firstName = Column(String(30), nullable=False)
    lastName = Column(String(30), nullable=False)
    email = Column(String(50))
    username = Column(String(30), nullable=False)
    password = Column(String(30), nullable=False)


class EmpUploadDb(Base):
    __tablename__ = 'emp_upload_db'

    id = Column(MEDIUMINT(8), primary_key=True)
    first_name = Column(String(100, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    last_name = Column(String(100, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    email = Column(String(200, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    department = Column(String(50, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    hire_date = Column(DateTime, nullable=False)
    file_data = Column(MEDIUMBLOB, nullable=False)
    file_name = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    file_type = Column(String(50, 'utf8_unicode_ci'), nullable=False)


class EmpUploadDir(Base):
    __tablename__ = 'emp_upload_dir'

    id = Column(MEDIUMINT(8), primary_key=True)
    first_name = Column(String(100, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    last_name = Column(String(100, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    email = Column(String(200, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    department = Column(String(50, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    hire_date = Column(DateTime, nullable=False)
    file_name = Column(String(100, 'utf8_unicode_ci'), nullable=False)


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(MEDIUMINT(8), primary_key=True)
    first_name = Column(String(100, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    last_name = Column(String(100, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    email = Column(String(200, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    department = Column(String(50, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    hire_date = Column(DateTime, nullable=False)
    notes = Column(Text(collation='utf8_unicode_ci'), nullable=False)


class LoginInfo(Base):
    __tablename__ = 'login_info'

    id = Column(MEDIUMINT(8), primary_key=True)
    employee_id = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    login = Column(String(100, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    password = Column(String(250, 'utf8_unicode_ci'), nullable=False, server_default=text("''"))
    account_type = Column(String(25, 'utf8_unicode_ci'), nullable=False, server_default=text("'User'"))


