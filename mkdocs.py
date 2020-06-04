from docstr_md.python import PySoup, compile_md
from docstr_md.src_href import Github

src_href = Github('https://github.com/dsbowen/sqlalchemy-mutablesoup/blob/master')

path = 'sqlalchemy_mutablesoup/__init__.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
for obj in soup.objects:
    if hasattr(obj, 'name'):
        if obj.name == 'MutableSoup':
            obj.methods = [m for m in obj.methods if m.name=='set_element']
        elif obj.name == 'MutableSoupType':
            obj.methods.clear()
compile_md(soup, compiler='sklearn', outfile='docs_md/use.md')