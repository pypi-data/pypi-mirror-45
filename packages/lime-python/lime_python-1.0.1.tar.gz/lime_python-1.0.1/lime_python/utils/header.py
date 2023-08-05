from lime_python.utils.documentsType import GetDocumentByMediaType
from lime_python.base.document import Document


class Header:
    """
    Representation of a Header element

    Parameters:
        value (Document)
    """

    def __init__(self, value=None):
        self.Value = value

    @property
    def Value(self):
        return self.__Value

    @Value.setter
    def Value(self, value):
        if value is not None and not isinstance(value, Document):
            raise ValueError('"Value" must be a Document')
        self.__Value = value

    def GetMediaType(self):
        if self.Value is not None:
            return self.Value.GetMediaType()
        return None

    def GetValueJson(self):
        if self.Value is not None:
            return self.Value.ToJson()
        return None

    def ToJson(self):
        return {
            'type': str(self.GetMediaType()),
            'value': self.GetValueJson()
        }

    def FromJson(inJson):
        if isinstance(inJson, str):
            inJson = json.loads(inJson)
        try:
            return Header(
                GetDocumentByMediaType(
                    inJson['type']
                ).FromJson(inJson['value'])
            )
        except KeyError:
            raise ValueError('The given json is not a InputDocument')
