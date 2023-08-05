from pyqalx.core.entities import QalxEntity


class Set(QalxEntity):
    """QalxEntity with entity_type Set

    """
    entity_type = 'set'
    
    def get_item_data(self, item_key):
        """
        helper method to get data from an item in the set

        :param item_key: key on the set to add the item as
        :type item_key: str
        :return: dict or None if key is missing
        """
        if self['items'].get(item_key):
            return self['items'].get(item_key)['data']
        else:
            return None
