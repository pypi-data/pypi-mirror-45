<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/gists_id.svg?longCache=True)](https://pypi.org/project/gists_id/)

#### Installation
```bash
$ [sudo] pip install gists_id
```

#### Config
```bash
$ export GITHUB_TOKEN="<GITHUB_TOKEN>"
```

#### Executable modules
usage|`__doc__`
-|-
`python -m gists_id` |print gists id

#### Examples
```bash
$ python -m gists_id
```

delete orphaned gists

```bash
$ pip install gist-delete gist-id
$ python -m gists_id | grep -v "$(find ~/git/gists -maxdepth 1 -exec gist-id {} \; 2> /dev/null)" | xargs gist-delete;:
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>