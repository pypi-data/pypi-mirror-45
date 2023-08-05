from lime_python.base.mediaType import MediaType
from lime_python.base.document import Document


class _ResourceDocument(Document):

    MIME_TYPE = 'application/vnd.iris.resource+json'

    def __init__(self, key, variables={}):
        super().__init__(MediaType.Parse(_ResourceDocument.MIME_TYPE))

        self.Key = key
        self.Variables = variables

    @property
    def Key(self):
        return self.__Key

    @Key.setter
    def Key(self, key):
        if not isinstance(key, str):
            raise ValueError('"Key" must be a string')
        self.__Key = key

    @property
    def Variables(self):
        return self.__Variables

    @Variables.setter
    def Variables(self, variables):
        if not isinstance(variables, dict):
            raise ValueError('"Variables" must be a dict')
        self.__Variables = variables

    def ToJson(self):
        json = {
            'key': self.Key
        }
        if len(self.Variables) > 0:
            json.update({'variables': self.Variables})

        return json


class ResourceDocument(_ResourceDocument):
    """
    Representation of a LIME resource document

    Parameters:
        key (str)
        variables (dict)
    """

    Type = MediaType.Parse(_ResourceDocument.MIME_TYPE)

    @staticmethod
    def FromJson(inJson):
        if isinstance(inJson, str):
            inJson = json.loads(inJson)
        try:
            variables = ('variables' in inJson and inJson['variables']) or {}
            return ResourceDocument(
                inJson['key'],
                variables
            )
        except KeyError:
            raise ValueError('The given json is not a ResourceDocument')
