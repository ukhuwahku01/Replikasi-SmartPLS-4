"""Review the completed paper, including whether table cells survive PDF rendering."""
from pathlib import Path
import json,re,hashlib,unicodedata
from docx import Document
import fitz

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
doc=Document(OUT/'KidSense_JADS_Draft_Paper.docx')
pdf=fitz.open(OUT/'KidSense_JADS_Draft_Paper.pdf')
data=json.loads((OUT/'paper_tables_full_precision_sources.json').read_text())
norm=lambda s:re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s)).strip()
text=norm(' '.join(p.get_text() for p in pdf))
checked=0
for table,info in zip(doc.tables,data['tables_display'].values()):
    assert [[c.text for c in row.cells] for row in table.rows]==[info['headers']]+info['rows'],info['title']
    for row in table.rows:
        for cell in row.cells:
            value=norm(cell.text)
            assert value in text, f'Not visible in PDF: {value!r}'
            checked+=1
assert len(doc.tables)==10
assert len(doc.inline_shapes)==2
for name in ['Introduction','Literature Review','Methodology','Results and Discussion','Conclusion','Declarations','References','Appendix A.','Appendix B.']:
    assert name in text,name
for name in ['Ratih Titi Komala Sari','Widowati','Adi Wibowo','ratihtiti@students.undip.ac.id']:
    assert name in text,name
for bad in ['First Author','Click here','doi.org/example','September 2024','Not applicable.','Type the paper title','1449-1461']:
    assert bad not in text,bad
assert 'AIR–EXP' in text and '0.888' in text and '0.908' in text and '0.913' in text
assert '0.122338' in text
refs=[p.text for p in doc.paragraphs if re.match(r'^\[\d+\] ',p.text)]
assert len(refs)==17
assert [int(re.match(r'^\[(\d+)\]',s).group(1)) for s in refs]==list(range(1,18))
for p in pdf:
    # Check visible words do not extend past the A4 page edges.
    for word in p.get_text('words'):
        assert word[0]>=0 and word[2]<=p.rect.width+.5 and word[1]>=0 and word[3]<=p.rect.height+.5,word
template=ROOT.parent/'attachments/2f82fc2f-7333-4b16-932a-c23db07d7717/JADS-template.docx'
assert hashlib.sha256(template.read_bytes()).hexdigest()=='dc78efa689c434b9d8c67f8d7f3c9e9dd9fa42bcd7a99628f04f2620a4501cc9'
report={
 'status':'PASS',
 'pages':len(pdf),'tables':len(doc.tables),'figures':len(doc.inline_shapes),'references':len(refs),
 'table_cells_checked_in_DOCX_and_PDF':checked,
 'template_unchanged':True,
 'template_format':'A4, one column; original styles/headers/ISSN retained; sample publication metadata replaced',
 'yellow_marker_paragraphs':[p.text for p in doc.paragraphs if '[TO BE COMPLETED:' in p.text],
 'reference_metadata_online_verified':False,
 'checks':['all table cells occur in rendered PDF','DOCX table cells equal source-backed display tables','all main sections and supplied author metadata present','template sample facts removed','reference numbering consecutive','no PDF word extends past page edges'],
 'files':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [OUT/'KidSense_JADS_Draft_Paper.docx',OUT/'KidSense_JADS_Draft_Paper.pdf']}
}
(OUT/'paper_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['yellow_marker_paragraphs','files']},ensure_ascii=False,indent=2))
