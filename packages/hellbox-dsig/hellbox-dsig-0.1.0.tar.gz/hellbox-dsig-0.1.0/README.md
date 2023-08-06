hellbox-dsig
============

A hellbox job that works with [digital signature tables](https://docs.microsoft.com/en-us/typography/opentype/spec/dsig).

* `InsertDummyDsig` — adds a valid digital signature table to an OTF/TTF font file.

```python
from hellbox.jobs.dsig import InsertDummyDsig

with Hellbox("build") as task:
    source = task.read("./source/*.otf")
    source >> InsertDummyDsig() >> task.write("./build/otf")
```

Installation
------------

Using the [hell CLI](https://github.com/hellboxpy/hell#installation):

```shell
$ hell install hellbox-dsig
```

Development
-----------

```shell
$ pip install -e .
$ pytest
```

Contributing
------------

To come...