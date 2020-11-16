from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine('postgresql://postgres:{}@{}:{}/{}'.format(os.getenv('DB_USER'), os.getenv('DB_URL'), os.getenv('DB_PORT'), os.getenv('DB_DATABASE')), echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class OrganizationsNetwork(Base):
    __tablename__='organization_networks'
    request_id = Column(Integer, primary_key=True)
    organization_id = Column(String)
    network_id = Column(String)
    name = Column(String)
    timezone = Column(String)
    tags = Column(String)
    productType = Column(String)
    type = Column(String)
    disableRemoteStatusPage = Column(Boolean)

class NetworkClients(Base):

    __tablename__ = 'network_clients_2'
    request_id = Column(Integer, primary_key=True)
    network_id = Column(String)
    client_id = Column(String)
    mac = Column(String)
    description = Column(String)
    ip = Column(String)
    ip6 = Column(String)
    ip6Local = Column(String)
    user = Column(String)
    firstSeen = Column(DateTime)
    lastSeen = Column(DateTime)
    manufacturer = Column(String)
    os = Column(String)
    recentDeviceSerial = Column(String)
    recentDeviceName = Column(String)
    recentDeviceMac = Column(String)
    ssid = Column(String)
    vlan = Column(String)
    switchport = Column(String)
    usage_sent = Column(String)
    usage_recv = Column(String)
    status = Column(String)
    notes = Column(String)
    smInstalled = Column(Boolean)
    groupPolicy8021x = Column(String)


Base.metadata.create_all(engine)