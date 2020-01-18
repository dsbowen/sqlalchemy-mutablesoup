# SQLAlchemy-MutableSoup

SQLAlchemy-MutableSoup defines a mutable [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) [SQLAlchemy](https://www.sqlalchemy.org/) database type.

## Example

After setup, we can manipulate a `MutableSoupType` database column as if it were a `BeautifulSoup` object.

```python
model.soup = '<p>Hello World.</p>'
print(model.soup)
print(
    '`soup` is a BeautifulSoup object?', 
    isinstance(model.soup, BeautifulSoup)
)
```

Output:

```
<p>Hello World.</p>
`soup` is a BeautifulSoup object? True
```

## Documentation

You can find the latest documentation at [https://dsbowen.github.io/sqlalchemy-mutablesoup](https://dsbowen.github.io/sqlalchemy-mutablesoup).

## License

Publications which use this software should include the following citation:

Bowen, D.S. (2020). SQLAlchemy-MutableSoup \[Computer software\]. [https://dsbowen.github.io/sqlalchemy-mutablesoup](https://dsbowen.github.io/sqlalchemy-mutablesoup).

This project is licensed under the MIT License [LICENSE](https://github.com/dsbowen/sqlalchemy-mutablesoup/blob/master/LICENSE).