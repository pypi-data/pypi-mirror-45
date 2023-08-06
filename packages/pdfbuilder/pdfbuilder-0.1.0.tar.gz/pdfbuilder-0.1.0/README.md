# PdfBuilder

PdfBuilder is a Python library for low-level PDF crafting. It allows:
- creating new PDF files from list of COS objects;
- adding new objects and editing existing ones via incremental saves;
- working with both old xref tables and new xref stream objects.

## How to install

`$ pip install pdfbuilder`

PdfBuilder is written in a pure Python and doesn't have any external dependencies. It requires Python 3.5 or higher to function properly.

## Example

A minimalistic code sample that creates "Hello, world" PDF file is listed below:
```python
import os, zlib
from pdfbuilder import PDF, Object, ObjectReference

# (0) Open new, empty file
if os.path.isfile('test.pdf'):
    os.remove('test.pdf')
doc = PDF('test.pdf')

# (1) Add pages object to PDF
pages_object = Object({
    'Type': '/Pages',
    'Kids': [ObjectReference(5)],  # We need to know page id beforehand :(
    'Count': 1,
    'MediaBox': [0, 0, 595.28, 841.89]
})
doc.add_new_object(pages_object)

# (2) Add font to pdf
font_object = Object({
    'Type': '/Font',
    'BaseFont': '/Helvetica',
    'Subtype': '/Type1',
    'Encoding': '/WinAnsiEncoding'
})
doc.add_new_object(font_object)

# (3) Add info object to PDF
pdf_info_object = Object({
    'ProcSet': ['/PDF', '/Text', '/ImageB', '/ImageC', '/ImageI'],
    'Font': [Object({'F1': font_object.ref()})]
})
doc.add_new_object(pdf_info_object)

# (4) Add first page content to PDF
content = b'2 J\n0.57 w\nBT /F1 14.00 Tf ET\nBT 56.69 785.20 Td (Hello, world!) Tj ET\n'
content_compressed = zlib.compress(content)
content_object = Object({
    'Filter': '/FlateDecode',
    'Length': len(content_compressed)
}, stream_data=content_compressed)
doc.add_new_object(content_object)

# (5) Add first page to PDF
page_object = Object({
    'Type': '/Page',
    'Parent': pages_object.ref(),
    'Resources': pdf_info_object.ref(),
    'Contents': content_object.ref()
})
doc.add_new_object(page_object)

# (6) Add main catalog to PDF
catalog_object = Object({
    'Type': '/Catalog',
    'Pages': pages_object.ref(),
    'OpenAction': [page_object.ref(), '/FitH', 'null'],
    'PageLayout': '/OneColumn'
})
doc.add_new_object(catalog_object)

# (7) Add xref table object and save PDF
doc.save(root_id=6, info_id=2)
```
The following example shows how to add another page to newly created document. Updates in PDF structure will be saved incrementally.
```python
from pdfbuilder import PDF, Object, ObjectReference

# (0) Open already existing PDF
doc = PDF('test.pdf')

# (1) Add new page to PDF
second_page_object = Object({
    'Type': '/Page',
    'Parent': ObjectReference(1),
    'Resources': ObjectReference(3),
    'Contents': ObjectReference(4)
})
doc.add_new_object(second_page_object)

# (2) Update pages object
new_pages_object = Object({
    'Type': '/Pages',
    'Kids': [ObjectReference(5), second_page_object.ref()],
    'Count': 2,
    'MediaBox': [0, 0, 595.28, 841.89]
}, id=1)
doc.update_object(new_pages_object, 1)

# (3) Add new xref table object and incrementally update PDF
doc.save(root_id=6, info_id=2)
```