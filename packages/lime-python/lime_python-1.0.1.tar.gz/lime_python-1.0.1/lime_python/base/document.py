from lime_python.base.mediaType import MediaType as MT


class Document:
    """
    Representation of a LIME Document

    Parameters:
        mediaType (MediaType or str)
    """

    def __init__(self, mediaType):

        self.MediaType = mediaType

    @property
    def MediaType(self):
        return self.__MediaType

    @MediaType.setter
    def MediaType(self, mediaType):
        if isinstance(mediaType, str):
            mediaType = MT.Parse(mediaType)
        if not isinstance(mediaType, MT):
            raise ValueError('"MediaType" must be a MediaType')
        self.__MediaType = mediaType

    def GetMediaType(self):
        if self.MediaType is not None:
            return self.MediaType
        return None

    def ToJson(self):
        return {
            'type': str(self.GetMediaType())
        }

    @staticmethod
    def FromJson(inJson):
        if isinstance(inJson, str):
            inJson = json.loads(inJson)
        try:
            return Document(inJson['type'])
        except KeyError:
            raise ValueError('The given json is not a Document')
