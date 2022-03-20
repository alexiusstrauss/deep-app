from service_storage.interfaces import StorageInterface


class ServiceStorage:
    """
    Storage's Services
    """

    def __init__(self, storage: StorageInterface):
        self.storage = storage
