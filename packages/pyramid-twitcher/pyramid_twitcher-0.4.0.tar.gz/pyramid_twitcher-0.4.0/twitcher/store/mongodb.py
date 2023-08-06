"""
Store adapters to read/write data to from/to mongodb using pymongo.
"""
import pymongo

from twitcher.store.base import AccessTokenStore
from twitcher.datatype import AccessToken
from twitcher.exceptions import AccessTokenNotFound

from twitcher.store.base import ServiceStore
from twitcher.datatype import Service
from twitcher.exceptions import ServiceNotFound
from twitcher import namesgenerator
from twitcher.utils import baseurl


import logging
LOGGER = logging.getLogger(__name__)


class MongodbStore(object):
    """
    Base class extended by all concrete store adapters.
    """

    def __init__(self, collection):
        self.collection = collection


class MongodbTokenStore(AccessTokenStore, MongodbStore):
    def save_token(self, access_token):
        self.collection.insert_one(access_token)

    def delete_token(self, token):
        self.collection.delete_one({'token': token})

    def fetch_by_token(self, token):
        token = self.collection.find_one({'token': token})
        if not token:
            raise AccessTokenNotFound
        return AccessToken(token)

    def clear_tokens(self):
        self.collection.drop()


class MongodbServiceStore(ServiceStore, MongodbStore):
    """
    Registry for OWS services. Uses mongodb to store service url and attributes.
    """

    def save_service(self, service, overwrite=True):
        """
        Stores an OWS service in mongodb.
        """
        name = namesgenerator.get_sane_name(service.name)
        if not name:
            name = namesgenerator.get_random_name()
            if self.collection.count_documents({'name': name}) > 0:
                name = namesgenerator.get_random_name(retry=True)
        # check if service is already registered
        if self.collection.count_documents({'name': name}) > 0:
            if overwrite:
                self.collection.delete_one({'name': name})
            else:
                raise Exception("service name already registered.")
        self.collection.insert_one(Service(
            name=name,
            url=baseurl(service.url),
            type=service.type,
            purl=service.purl,
            public=service.public,
            auth=service.auth,
            verify=service.verify))
        return self.fetch_by_name(name=name)

    def delete_service(self, name):
        """
        Removes service from mongodb storage.
        """
        self.collection.delete_one({'name': name})
        return True

    def list_services(self):
        """
        Lists all services in mongodb storage.
        """
        my_services = []
        for service in self.collection.find().sort('name', pymongo.ASCENDING):
            my_services.append(Service(service))
        return my_services

    def fetch_by_name(self, name):
        """
        Gets service for given ``name`` from mongodb storage.
        """
        service = self.collection.find_one({'name': name})
        if not service:
            raise ServiceNotFound
        return Service(service)

    def fetch_by_url(self, url):
        """
        Gets service for given ``url`` from mongodb storage.
        """
        service = self.collection.find_one({'url': url})
        if not service:
            raise ServiceNotFound
        return Service(service)

    def clear_services(self):
        """
        Removes all OWS services from mongodb storage.
        """
        self.collection.drop()
        return True
