from lime_python.base.document import Document
from lime_python.base.mediaType import MediaType
from lime_python.utils.documentsType import GetDocumentByMediaType
import json


class _CollectionDocument(Document):

    MIME_TYPE = 'application/vnd.lime.collection+json'

    def __init__(self, itemType, items=[]):
        super().__init__(MediaType.Parse(_CollectionDocument.MIME_TYPE))

        self.ItemType = itemType
        self.Items = items

    @property
    def ItemType(self):
        return self.__ItemType

    @ItemType.setter
    def ItemType(self, itemType):
        if itemType is not None and not isinstance(itemType, MediaType):
            raise ValueError('"ItemType" must be a MediaType')
        self.__ItemType = itemType

    @property
    def Items(self):
        return self.__Items

    @Items.setter
    def Items(self, items):
        if not isinstance(items, list):
            raise ValueError(
                '"Items" must be a list of the given type')
        for i in items:
            if not isinstance(i, Document) and not isinstance(i, dict):
                raise ValueError('All Items must be a Document or dict')

        self.__Items = items

    @property
    def Total(self):
        return len(self.Items)

    def GetDocumentsJson(self):
        if self.ItemType == MediaType.ApplicationJson:
            return self.Items
        return [x.ToJson() for x in self.Items]

    def ToJson(self):
        return {
            'itemType': str(self.ItemType),
            'items': self.GetDocumentsJson()
        }


class CollectionDocument(_CollectionDocument):
    """
    Representation of a LIME collection document

    Parameters:
        itemType (MediaType)
        items ([Document])
    """

    Type = MediaType.Parse(_CollectionDocument.MIME_TYPE)

    @staticmethod
    def FromJson(inJson):
        if isinstance(inJson, str):
            inJson = json.loads(inJson)
        try:
            itemType = GetDocumentByMediaType(inJson['itemType'])
            if itemType is not None and itemType != dict:
                items = [itemType.FromJson(x) for x in inJson['items']]
            else:
                items = inJson['items']
            return CollectionDocument(
                MediaType.Parse(inJson['itemType']),
                items
            )
        except KeyError:
            raise ValueError('The given json is not a CollectionDocument')
