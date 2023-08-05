from lime_python.documents.plainTextDocument import PlainTextDocument
from lime_python.utils.documentsType import GetDocumentByMediaType
from lime_python.base.mediaType import MediaType
from lime_python.base.document import Document


class _SensitiveInformationDocument(Document):

    MIME_TYPE = 'application/vnd.lime.sensitive+json'

    def __init__(self, value):
        super().__init__(
            MediaType.Parse(_SensitiveInformationDocument.MIME_TYPE))

        self.Value = value

    @property
    def Value(self):
        return self.__Value

    @Value.setter
    def Value(self, value):
        if isinstance(value, str):
            value = PlainTextDocument(value)
        if not isinstance(value, Document) and not isinstance(value, dict):
            raise ValueError('"Value" must be a Document, dict or str')
        self.__Value = value

    def GetValueMediaType(self):
        return self.Value.GetMediaType()

    def GetValueJson(self):
        if isinstance(self.Value, dict):
            return self.Value
        return self.Value.ToJson()

    def ToJson(self):
        return {
            'type': str(self.GetValueMediaType()),
            'value': self.GetValueJson()
        }


class SensitiveInformationDocument(_SensitiveInformationDocument):
    """
    Representation of a LIME sensitive information document

    Parameters:
        value (Document, dict or str)
    """

    Type = MediaType.Parse(_SensitiveInformationDocument.MIME_TYPE)

    @staticmethod
    def FromJson(inJson):
        if isinstance(inJson, str):
            inJson = json.loads(inJson)
        try:
            valueType = GetDocumentByMediaType(
                inJson['type']
            )
            if valueType == dict:
                value = inJson['value']
            else:
                value = valueType.FromJson(
                    inJson['value']
                )
            return SensitiveInformationDocument(value)
        except KeyError:
            raise ValueError(
                'The given json is not a SensitiveInformationDocument')
