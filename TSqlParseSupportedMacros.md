## var ##

```
/* var:name */ ... /* end */
```

The whole comment and section `...` is replaced with the variable specified by the command line option `-v=<value>`.

**Example 1**

```
declare @d1 datetime = /* var:date */ '20110101' /* end */
```

using

`TSqlParse.py -vdate='20121001'`

will be result in: -

```
declare @d1 datetime = '20121001'
```

Not specifying the parameter on the command line will leave the variable unchanged.

## log ##

```
/* log: "<format string>", @var1, @var2, function(), ..., @varn */
```

Uses format string to construct a log message that is raised with severity 10 and state 1.

Format string currently supports the following substitution place holders: -

| `%s` | substitute value directly |
|:-----|:--------------------------|
| `%s{,m`} | substitute value and convert to style m |
| `%s{n,m`} | substitute value and convert to style m and truncate to length n |
| `%s{n`} | substitute value and truncate to length n |

## sqlcmd ##

```
/* sqlcmd: ... */
```

Substitutes `...` into a sqlcmd command prefixed with a colon ":".

**Example 2**

```
/* sqlcmd: exit(select @exitcode) */
```

will be converted to: -

```
:exit(select @exitcode)
```

This might be useful if one wishes to provide a script with an exit code without having to use sqlcmd processing in SSMS (doing so will disable Intellisense).

