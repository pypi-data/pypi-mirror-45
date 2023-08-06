<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install gist-delete
```

#### Config
```bash
$ export GITHUB_TOKEN="<GITHUB_TOKEN>"
```

#### Scripts usage
```bash
usage: gist-delete id ...
```

#### Examples
```bash
$ gist-id <id1> <id2>
```

delete orphaned gists
```bash
$ pip install gist-id gists-id
$ python -m gists_id | grep -v "$(find ~/git/gists -maxdepth 1 -exec gist-id {} \; 2> /dev/null)" | xargs gist-delete;:
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>