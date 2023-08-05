<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/filetest.svg?longCache=True)](https://pypi.org/project/filetest/)

#### Installation
```bash
$ [sudo] pip install filetest
```

#### Functions
function|`__doc__`
-|-
`filetest.d(path)` |return True if path exists and is a directory, else False
`filetest.f(path)` |return True if file exists and is a regular file, else False
`filetest.nt(path1, path2)` |return True if path1 is newer than path2, else False
`filetest.ot(path1, path2)` |return True if path1 is older than path2, else False
`filetest.r(path)` |return True if path exists and has read permission (for the current user), else False
`filetest.s(path)` |return True if path exists and is not zero size, else False
`filetest.w(path)` |return True if path exists and has write permission (for the current user), else False
`filetest.x(path)` |return True if path exists and has execute permission (for the current user), else False

#### Links
+   [File test operators](https://www.tldp.org/LDP/abs/html/fto.html)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>