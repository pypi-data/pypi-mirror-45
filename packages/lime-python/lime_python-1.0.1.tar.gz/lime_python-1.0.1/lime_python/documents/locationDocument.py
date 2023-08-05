from lime_python.utils.documentsType import GetDocumentByMediaType
from lime_python.base.mediaType import MediaType
from lime_python.base.document import Document


class _LocationDocument(Document):

    MIME_TYPE = 'application/vnd.lime.location+json'

    def __init__(self, text=None, latitude=None,
                 longitude=None, altitude=None):
        super().__init__(MediaType.Parse(_LocationDocument.MIME_TYPE))
        self.Text = text
        self.Latitude = latitude
        self.Longitude = longitude
        self.Altitude = altitude

    @property
    def Text(self):
        return self.__Text

    @Text.setter
    def Text(self, text):
        if text is not None and not isinstance(text, str):
            raise ValueError('"Text" must be a string')
        self.__Text = text

    @property
    def Latitude(self):
        return self.__Latitude

    @Latitude.setter
    def Latitude(self, latitude):
        if latitude is not None and not isinstance(latitude, float):
            try:
                latitude = float(latitude)
            except:
                raise ValueError('"Latitude" must be a float')
        self.__Latitude = latitude

    @property
    def Longitude(self):
        return self.__Longitude

    @Longitude.setter
    def Longitude(self, longitude):
        if longitude is not None and not isinstance(longitude, float):
            try:
                longitude = float(longitude)
            except:
                raise ValueError('"Logintude" must be a float')
        self.__Longitude = longitude

    @property
    def Altitude(self):
        return self.__Altitude

    @Altitude.setter
    def Altitude(self, altitude):
        if altitude is not None and not isinstance(altitude, float):
            try:
                altitude = float(altitude)
            except:
                raise ValueError('"Altitude" must be a float')
        self.__Altitude = altitude

    def ToJson(self):
        json = {}

        if self.Latitude is not None:
            json.update({'latitude': self.Latitude})
        if self.Longitude is not None:
            json.update({'longitude': self.Longitude})
        if self.Altitude is not None:
            json.update({'altitude': self.Altitude})
        if self.Text is not None:
            json.update({'text': self.Text})

        return json


class LocationDocument(_LocationDocument):
    """
    Representation of a LIME location document

    Parameters:
        text (str)
        latitude (float)
        longitude (float)
        altitude (float)
    """

    Type = MediaType.Parse(_LocationDocument.MIME_TYPE)

    @staticmethod
    def FromJson(inJson):
        if isinstance(inJson, str):
            inJson = json.loads(inJson)
        try:
            text = ('text' in inJson and inJson['text']) or None
            latitude = ('latitude' in inJson and inJson['latitude']) or None
            longitude = ('longitude' in inJson and inJson['longitude']) or None
            altitude = ('altitude' in inJson and inJson['altitude']) or None

            return LocationDocument(text, latitude, longitude, altitude)
        except KeyError:
            raise ValueError('The given json is not a InputDocument')
