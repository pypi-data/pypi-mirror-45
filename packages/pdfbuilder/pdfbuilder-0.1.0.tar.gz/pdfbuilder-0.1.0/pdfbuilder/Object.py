from .ObjectReference import ObjectReference


class Object:
    def __init__(self, properties, id=None, stream_data=None):
        self.properties = properties
        self.id = id
        self.stream_data = stream_data

    @staticmethod
    def _build_obj_from_properties(properties):
        result = b''
        for key, value in properties.items():
            if isinstance(value, list):
                result += b'/%b [%b ] ' % (bytes(str(key), 'ascii'), b' '.join([bytes(str(v), 'ascii') for v in value]))
            else:
                result += b'/%b %b ' % (bytes(str(key), 'ascii'), bytes(str(value), 'ascii'))
        return result

    def get_properties(self):
        return b'<<%b>>' % Object._build_obj_from_properties(self.properties)

    def __str__(self):
        return self.get_properties().decode('ascii')

    def get_bytes(self):
        if self.id is None:
            raise Exception('id must be defined')
        if self.stream_data is None:
            return b'%d 0 obj\r\n%b\r\nendobj\r\n' % (self.id,
                                                      self.get_properties())
        else:
            return b'%d 0 obj\r\n%b\r\nstream\r\n%b\r\nendstream\r\nendobj\r\n' % (self.id,
                                                                                   self.get_properties(),
                                                                                   self.stream_data)

    def ref(self):
        if self.id is None:
            raise Exception('id must be defined')
        return ObjectReference(self.id)
