## Utilities

### `map2map`

`map2map` converts mapping files to the RML format. When provided with a
YARRRML file (``.yml``/``.yaml``) it relies on the
[YATTER](https://github.com/RMLio/yatter) CLI to do the conversion.  Existing
RML files are copied to the requested destination.

```
python -m src.map2map path/to/mapping.yml -o path/to/mapping.rml.ttl
```

The command prints the location of the generated file to standard output.
Set the ``YATTER_CMD`` environment variable or pass ``--yatter`` to point to a
custom executable when ``yatter`` is not on ``PATH``.

### `map2graph`

`map2graph` executes an RML mapping using the
[`RMLMapper`](https://github.com/RMLio/rmlmapper-java) CLI.  The path to the
mapper is read from the ``RMLMAPPER_JAR`` environment variable unless it is
provided via ``--rmlmapper``.  Use ``--ontology`` and ``--headers`` to provide
paths that can be consumed in the mapping via RMLMapper parameter placeholders
(``@{ontology}`` and ``@{headers}``).

```
python -m src.map2graph path/to/mapping.rml.ttl --ontology path/to/ontology.ttl \
    --headers path/to/headers.csv --rmlmapper /path/to/rmlmapper.jar
```

The generated triples are printed to standard output (one line per line in the
output file) and also written to disk. By default the file is named
``graph.ttl`` in the current working directory; supply ``--output`` to override
this behaviour. If the mapping fails or produces no triples the command exits
with a non-zero status code.

