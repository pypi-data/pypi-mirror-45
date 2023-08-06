import zlib
import collections
import re
from .Object import Object, ObjectReference
from .utils import random_string


class PDF:
    def __init__(self, file_name):
        self.file_name = file_name
        try:
            self.old_content = open(file_name, 'rb').read()
        except:
            self.old_content = b''

        self.xref_obj = True
        if len(self.old_content) > 0:
            self.base = len(self.old_content)
            object_numbers = [int(s[:s.find(b' ')]) for s in re.findall(b'[0-9]+ 0 obj', self.old_content)]
            self.next_object_number = max(object_numbers) + 1
            prev_xref_pos = self.old_content.rfind(b'startxref\r\n') + 11
            self.prev_xref = int(self.old_content[prev_xref_pos:self.old_content.find(b'\r\n', prev_xref_pos)])
            self.xref = collections.OrderedDict()
            self.new_content = b''
            if self.old_content.find(b'\nxref') != -1:
                self.xref_obj = False
        else:
            self.base = 0
            self.next_object_number = 1
            self.prev_xref = None
            self.xref = collections.OrderedDict({0: [0, 0xffff]})
            self.new_content = b'%PDF-1.5\r\n'

    def add_new_object(self, object):
        object.id = self.next_object_number
        object_offset = self.base + len(self.new_content)
        self.new_content += object.get_bytes()
        self.xref[self.next_object_number] = [object_offset, 0]
        self.next_object_number += 1

    def update_object(self, object, object_version):
        object_offset = self.base + len(self.new_content)
        self.new_content += object.get_bytes()
        self.xref[object.id] = [object_offset, object_version]

    @staticmethod
    def _gen_entry(position, version, free=False, binary=True):
        if binary:
            return (b'\x00' if free else b'\x01') + \
                   position.to_bytes(4, byteorder='big') + \
                   version.to_bytes(2, byteorder='big')
        else:
            return b'%b %b %b' % (bytes(str(position).zfill(10), 'ascii'),
                                  bytes(str(version).zfill(5), 'ascii'),
                                  b'f' if free else b'n')

    def _build_xref_entries(self, binary):
        xref_index = {}
        xref_table_entries = []
        for object_number, object_data in self.xref.items():
            added_to_index = False
            for start, count in xref_index.items():
                if object_number >= start:
                    if object_number < start + count:
                        added_to_index = True
                        break
                    elif object_number == start + count:
                        added_to_index = True
                        xref_index[start] += 1
                        break
            if not added_to_index:
                xref_index[object_number] = 1
        xref_index = collections.OrderedDict(sorted(xref_index.items()))
        for first, count in xref_index.items():
            for i in range(count):
                obj_id = first + i
                free = obj_id == 0
                xref_table_entries.append(PDF._gen_entry(self.xref[obj_id][0], self.xref[obj_id][1], free, binary))
        return xref_index, xref_table_entries

    def make_xref(self, root_id, info_id):
        xref_offset = self.base + len(self.new_content)
        xref = b'xref\r\n'
        xref_index, xref_table_entries = self._build_xref_entries(False)
        xref_next_entry = 0
        for start, count in xref_index.items():
            xref += b'%d %d\r\n' % (start, count)
            for i in range(count):
                xref += xref_table_entries[xref_next_entry] + b'\r\n'
                xref_next_entry += 1
        trailer_properties = {
            'ID': '[<%s><%s>]' % (random_string(32), random_string(32)),
            'Root': ObjectReference(root_id),
            'Size': xref_next_entry
        }
        if self.prev_xref:
            trailer_properties['Prev'] = self.prev_xref
        if info_id:
            trailer_properties['Info'] = ObjectReference(info_id)
        trailer_obj = Object(trailer_properties)
        xref += b'trailer\r\n%b\r\nstartxref\r\n%d\r\n%%EOF\r\n' % (trailer_obj.get_properties(), xref_offset)
        self.new_content += xref

    def make_xref_obj(self, root_id, info_id):
        xref_offset = self.base + len(self.new_content)
        xref_object_number = self.next_object_number
        self.xref[self.next_object_number] = [xref_offset, 0]
        self.next_object_number += 1
        xref_index, xref_table_entries = self._build_xref_entries(True)
        xref_table_entries_predicted = [xref_table_entries[0]]
        for i in range(1, len(xref_table_entries)):
            pred = b''
            for j in range(len(xref_table_entries[i])):
                pred += ((int(xref_table_entries[i][j]) - int(xref_table_entries[i - 1][j])) & 0xff) \
                    .to_bytes(1, byteorder='big')
            xref_table_entries_predicted.append(pred)
        xref_table = zlib.compress(b''.join(b'\x02' + bp for bp in xref_table_entries_predicted))
        xref_properties = {
            'Type': '/XRef',
            'W': [1, 4, 2],
            'Index': [item for pair in xref_index.items() for item in pair],
            'Size': self.next_object_number,
            'Filter': '/FlateDecode',
            'DecodeParms': Object({'Columns': 7, 'Predictor': 12}),
            'Length': len(xref_table),
            'ID': '[<%s><%s>]' % (random_string(32), random_string(32)),
            'Root': ObjectReference(root_id)
        }
        if self.prev_xref:
            xref_properties['Prev'] = self.prev_xref
        if info_id:
            xref_properties['Info'] = ObjectReference(info_id)
        xref_object = Object(xref_properties, xref_object_number, xref_table)
        self.new_content += xref_object.get_bytes() + b'\r\nstartxref\r\n%d\r\n%%EOF\r\n' % xref_offset

    def save(self, root_id, info_id=None):
        xref_offset = self.base + len(self.new_content)
        if self.xref_obj:
            self.make_xref_obj(root_id, info_id)
        else:
            self.make_xref(root_id, info_id)
        open(self.file_name, 'ab+').write(self.new_content)
        self.old_content += self.new_content
        self.new_content = b''
        self.base = len(self.old_content)
        self.prev_xref = xref_offset
        self.xref = {}
