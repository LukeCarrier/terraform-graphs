# Better Terraform graphing

An experiment for improving Terraform graph output. Currently applies fill colours exclusively to Azure resources.

* * *

## Usage

Either use shell pipelines:

```
$ terraform graph | ./graph.py | twopi -Goverlap=false -Gsplines=true -Tsvg -o graph.svg
```

Or apply to an existing document:

```
$ terraform graph >graph.gv
$ ./graph.py --source graph.pre.gv >graph.gv
```
