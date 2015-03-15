# Supported Options #

```
Usage: TSqlParse.py [options]

TSqlParse - run tsql with macro substitution

Options:
  -h, --help            show this help message and exit

  Main Options:
    The following actions are available.

    -f FILEPATH, --file=FILEPATH
                        Specify a different date
    -v VAR=VALUE, --var=VAR=VALUE
                        Specify variables mappings

  SqlCmd Options:
    The following options are passed throught to sqlcmd.

    -S [PROTOCOL:]HOSTNAME[\DATABASE][,PORT], --server=[PROTOCOL:]HOSTNAME[\DATABASE][,PORT]
                        Specify server
    -H HOSTNAME, --hostname=HOSTNAME
                        Specify hostname
    -d DATABASE, --database=DATABASE
                        Specify database
    --sqlcmd-options=EXTRA-OPTIONS
                        Other SqlCmd options

```