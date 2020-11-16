import requests as req
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import _db


class ClientsRequest():

    def __init__(self, networkId, organizationId):
       
        self._networkId = networkId
        self.organizationId = organizationId
        self.db = _db
        self._authKey = os.getenv('BETHA_AUTH')
        self.headers = {'X-Cisco-Meraki-API-Key': self._authKey} 

    # *** Método que faz um request dos clientes de uma determinada network:
    def getNetworkClients(self):       
        res = req.get(
            f'https://api.meraki.com/api/v0/networks/{self._networkId}/clients',
            headers=self.headers)
        if res.status_code == 200:
            return res.json()
        else:
            return res.status_code

    # *** Método que faz um request das networks de uma determinada organização:
    def getOrganizationsNetworks(self):
        res = req.get(
            f'https://api.meraki.com/api/v0/organizations/{self.organizationId}/networks/',
             headers=self.headers)
        if res.status_code == 200:
            return res.json()
        else:
            return res.status_code

    def insertDb(self):

         # *** Criando a conexão com o postgres 
        engine = create_engine('postgresql://postgres:{}@{}:{}/{}'.format(os.getenv('DB_USER'), os.getenv('DB_URL'), os.getenv('DB_PORT'), os.getenv('DB_DATABASE')))
        Session = sessionmaker(bind=engine)
        session = Session()

        # *** Fazendo a request e armazenando a resposta em uma variável
        clientsOrganizations = self.getNetworkClients()
        networkOrganizations = self.getOrganizationsNetworks()

        # *** Iterando pelos itens da resposta e armazenado-os no banco de dados
        for client in clientsOrganizations:

            usage = client.get('usage', 'null')

            network_clients = self.db.NetworkClients(
                network_id = self._networkId,
                client_id = client.get('id'),
                mac = client.get('mac'),
                description = client.get('description'),
                ip = client.get('ip'),
                ip6 = client.get('ip6'),
                ip6Local = client.get('ip6Local'),
                user = client.get('user'),
                firstSeen = client.get('firstSeen'),
                lastSeen = client.get('lastSeen'),
                manufacturer = client.get('manufacturer'),
                os = client.get('os'),
                recentDeviceSerial = client.get('recentDeviceSerial'),
                recentDeviceName = client.get('recentDeviceName'),
                recentDeviceMac = client.get('recentDeviceMac'),
                ssid = client.get('ssid'),
                vlan = client.get('vlan'),
                switchport = client.get('switchport'),
                usage_sent = usage.get('sent'),
                usage_recv = usage.get('recv'),
                status = client.get('status'),
                notes = client.get('notes'),
                smInstalled = client.get('smInstalled'),
                groupPolicy8021x = client.get('groupPolicy8021x'),
                )

            session.add(network_clients)
            session.commit()

        for network in networkOrganizations:
            organization_network = self.db.OrganizationsNetwork(
                organization_id = network.get('organizationId'),
                network_id = network.get('id'),
                name = network.get('name'),
                timezone = network.get('timeZone'),
                tags = network.get('tags'),
                productType = network.get('productTypes'),
                type = network.get('type'),
                disableRemoteStatusPage = network.get('disableRemoteStatusPage'),
            )

            session.add(organization_network)
            session.commit()

            

    def testRequest(self):
        testeRequest = self.getNetworkClients()
        print(testeRequest)



#* Criando a classe passando os dados, e chamando o método      
migracaoRquests = ClientsRequest(os.getenv('BETHA_NET'), os.getenv('BETHA_ID'))
migracaoRquests.insertDb()

