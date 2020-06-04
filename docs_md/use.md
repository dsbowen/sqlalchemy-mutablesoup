<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

<link rel="stylesheet" href="https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css" type="text/css" />

<style>
    a.src-href {
        float: right;
    }
    p.attr {
        margin-top: 0.5em;
        margin-left: 1em;
    }
    p.func-header {
        background-color: gainsboro;
        border-radius: 0.1em;
        padding: 0.5em;
        padding-left: 1em;
    }
    table.field-table {
        border-radius: 0.1em
    }
</style># Mutable BeautifulSoup database type

## Examples

#### Setup

```python
from sqlalchemy_mutablesoup import MutableSoupType

from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# standard session creation
engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base = declarative_base()

# define and instantiate a model with a MutableSoupType column.
class Model(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True)
    soup = Column(MutableSoupType)

Base.metadata.create_all(engine)

model = Model()
session.add(model)
```

#### Setting soup objects

```python
model.soup = '<p>Hello World.</p>'
model.soup
```

Out:

```
<p>Hello World.</p>
```

#### Setting soup elements: basic use

```python
model.soup.set_element(parent_selector='p', val='Hello Moon.')
session.commit()
model.soup
```

Out:

```
<p>Hello Moon.</p>
```

#### Creating soup elements with a `gen_target` function

```python
def gen_span_tag(*args, **kwargs):
    print('My args are:', args)
    print('My kwargs are:', kwargs)
    return '<span></span>'

model.soup.set_element(
    parent_selector='p',
    val='Span text',
    target_selector='span',
    gen_target=gen_span_tag,
    args=['hello world'],
    kwargs={'hello': 'moon'},
)
session.commit()
model.soup
```

Out:

```
My args are: ('hello world',)
My kwargs are: {'hello': 'moon'}
<p>Hello Moon.<span></span></p>
```

#### Registering changes

Call `changed` to register other changes with the database.

```python
model.soup.select_one('p')['style'] = 'color:red;'
model.soup.changed()
session.commit()
model.soup
```

Out:

```
<p style="color:red;">Hello Moon.<span></span></p>
```

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##sqlalchemy_mutablesoup.**SoupBase**



Base for `MutableSoup` objects. Interits from `bs4.BeautifulSoup`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>text</b>(<i>self, selector</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutablesoup/blob/master/sqlalchemy_mutablesoup/__init__.py#L119">[source]</a>
</p>

Get text from html element.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>selector : <i>str</i></b>
<p class="attr">
    CSS selector.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>text : <i>str or None</i></b>
<p class="attr">
    Return text from selected html element. Return <code>None</code> if no element is selected.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>copy</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutablesoup/blob/master/sqlalchemy_mutablesoup/__init__.py#L137">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>sqlalchemy_mutablesoup.SoupBase</i></b>
<p class="attr">
    Shallow copy of <code>self</code>.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>render</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutablesoup/blob/master/sqlalchemy_mutablesoup/__init__.py#L146">[source]</a>
</p>

Render html for insertion into a Jinja template.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>rendered : <i>flask.Markup</i></b>
<p class="attr">
    Rendered html.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>set_element</b>(<i>self, parent_selector, val, target_selector=None, gen_target=None, args=(), kwargs={}</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutablesoup/blob/master/sqlalchemy_mutablesoup/__init__.py#L157">[source]</a>
</p>

Set a soup element.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>parent_selector : <i>str</i></b>
<p class="attr">
    CSS selector for the parent of the html element being set (the 'target element').
</p>
<b>val : <i>str or bs4.BeautifulSoup</i></b>
<p class="attr">
    Value to which the target element will be set. If <code>val</code> evaluates to <code>False</code>, the target element is cleared.
</p>
<b>target_selector : <i>str or None, default=None</i></b>
<p class="attr">
    CSS selector for the target element; a child of the parent element. If <code>None</code>, the parent element is treated as the target element.
</p>
<b>gen_target : <i>callable or None, default=None</i></b>
<p class="attr">
    Callable which generates the target element if none of the parent element's children are selected by the <code>target_selector</code>. The output of <code>gen_target</code> should be a string or <code>bs4. BeautifulSoup</code> object.
</p>
<b>args : <i>iterable</i></b>
<p class="attr">
    Arguments for <code>gen_target</code>.
</p>
<b>kwargs : <i>dict</i></b>
<p class="attr">
    Keyword arguments for <code>gen_target</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>sqlalchemy_mutablesoup.SoupBase</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##sqlalchemy_mutablesoup.**MutableSoup**



Mutable BeautifulSoup database object. Inherits from `SoupBase`. Note
that a `MutableSoup` object can be set using a string or
`bs4.BeautifulSoup` object.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>set_element</b>(<i>self, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutablesoup/blob/master/sqlalchemy_mutablesoup/__init__.py#L266">[source]</a>
</p>

Inherits from `SoupBase.set_element`. The only addition is that this
method also registers that it has changed.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>sqlalchemy_mutable.MutableSoup</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##sqlalchemy_mutablesoup.**MutableSoupType**



Mutable BeautifulSoup database type associated with `MutableSoup` object.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>







<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

