from lime_python.utils.documentsType import GetDocumentByMediaType
from lime_python.base.mediaType import MediaType as MT
from lime_python.base.document import Document


class _MediaLinkDocument(Document):

    MIME_TYPE = 'application/vnd.lime.media-link+json'

    def __init__(self, mimeType=None, size=None, aspectRatio=None, uri=None,
                 title=None, text=None, previewType=None, previewUri=None):
        super().__init__(MT.Parse(_MediaLinkDocument.MIME_TYPE))

        self.MimeType = mimeType
        self.Size = size
        self.AspectRatio = aspectRatio
        self.Uri = uri
        self.Title = title
        self.Text = text
        self.PreviewType = previewType
        self.PreviewUri = previewUri

    @property
    def MimeType(self):
        return self.__MimeType

    @MimeType.setter
    def MimeType(self, mimeType):
        if isinstance(mimeType, str):
            mimeType = MT.Parse(mimeType)
        if mimeType is not None and not isinstance(mimeType, MT):
            raise ValueError('"MimeType" must be a MimeType or str')
        self.__MimeType = mimeType

    @property
    def Size(self):
        return self.__Size

    @Size.setter
    def Size(self, size):
        if size is not None and not isinstance(size, float):
            try:
                size = float(size)
            except:
                raise ValueError('"Size" must be a float')
        self.__Size = size

    @property
    def AspectRatio(self):
        return self.__AspectRatio

    @AspectRatio.setter
    def AspectRatio(self, aspectRatio):
        if aspectRatio is not None and not isinstance(aspectRatio, str):
            raise ValueError('"AspectRatio" must be a string')
        self.__AspectRatio = aspectRatio

    @property
    def Uri(self):
        return self.__Uri

    @Uri.setter
    def Uri(self, uri):
        if uri is not None and not isinstance(uri, str):
            raise ValueError('"Uri" must be a string')
        self.__Uri = uri

    @property
    def Title(self):
        return self.__Title

    @Title.setter
    def Title(self, title):
        if title is not None and not isinstance(title, str):
            raise ValueError('"Title" must be a string')
        self.__Title = title

    @property
    def PreviewType(self):
        return self.__PreviewType

    @PreviewType.setter
    def PreviewType(self, previewType):
        if isinstance(previewType, str):
            previewType = MT.Parse(previewType)
        if previewType is not None and not isinstance(previewType, MT):
            raise ValueError('"PreviewType" must be a MediaType or str')
        self.__PreviewType = previewType

    @property
    def PreviewUri(self):
        return self.__PreviewUri

    @PreviewUri.setter
    def PreviewUri(self, previewUri):
        if previewUri is not None and not isinstance(previewUri, str):
            raise ValueError('"PreviewUri" must be a string')
        self.__PreviewUri = previewUri

    def ToJson(self):
        json = {
            'uri': self.Uri
        }
        if self.MimeType is not None:
            json.update({'type': str(self.MimeType)})
        if self.Text is not None:
            json.update({'text': self.Text})
        if self.Size is not None:
            json.update({'size': self.Size})
        if self.AspectRatio is not None:
            json.update({'aspectRatio': self.AspectRatio})
        if self.Title is not None:
            json.update({'title': self.Title})
        if self.PreviewType is not None:
            json.update({'previewType': str(self.PreviewType)})
        if self.PreviewUri is not None:
            json.update({'previewUri': self.PreviewUri})

        return json


class MediaLinkDocument(_MediaLinkDocument):
    """
    Representation of a LIME media link document

    Parameters:
    mimeType (MediaType or str)
    size (float)
    aspectRatio (str)
    uri (str)
    title (str)
    text (str)
    previewType (MediaType or str)
    previewUri (str)
    """

    Type = MT.Parse(_MediaLinkDocument.MIME_TYPE)

    @staticmethod
    def FromJson(inJson):
        if isinstance(inJson, str):
            inJson = json.loads(inJson)
        try:
            mimeType = ('type' in inJson and inJson['type']) or None
            text = ('text' in inJson and inJson['text']) or None
            size = ('size' in inJson and inJson['size']) or None
            aspectRatio = (
                'aspectRatio' in inJson and inJson['aspectRatio']) or None
            title = ('title' in inJson and inJson['title']) or None
            previewType = (
                'previewType' in inJson and inJson['previewType']) or None
            previewUri = (
                'previewUri' in inJson and inJson['previewUri']) or None

            return MediaLinkDocument(
                mimeType,
                size,
                aspectRatio,
                inJson['uri'],
                title,
                text,
                previewType,
                previewUri
            )
        except KeyError:
            raise ValueError('The given json is not a MediaLinkDocument')
