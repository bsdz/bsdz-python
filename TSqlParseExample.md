# Input file (TSqlParseSample.sql) #

```
declare @startdate datetime = /* var:startdate */ '2010-04-01 00:00' /* end */
declare @enddate datetime = /* var:enddate */ '2010-10-26 00:00' /* end */

declare @foo varchar(max) = CAST(/* var:foo */ 5 /*end */ as varchar(max)) 
declare @bar varchar(max) = /* var:bar */ null /* end */ 

/* log: "%s{16,120}: %s{10,120} -> %s{10,120}, foo is %s and bar is %s", getdate(), @startdate, @enddate, @foo, @bar */

declare @exitcode int = 10

/* sqlcmd: exit(select @exitcode) */

```



# Usage #

```
TSqlParse.py -dcafis -f"C:\TSqlParseSample.sql" -vstartdate='20090401' -venddate='20110430'
```

# Output #
```
INFO|2011-04-15 15:19:41,944|tsqlparse.py:165|sqlcmd -E -dcafis -i"c:\docume~1\bls\locals~1\temp\tmptdsdvz"
INFO|2011-04-15 15:19:42,115|tsqlparse.py:168|2011-04-15 15:19: 2009-04-01 -> 2011-04-30, foo is 5 and bar is NULL

-----------
         10

(1 rows affected)

INFO|2011-04-15 15:19:42,115|tsqlparse.py:169|Script terminated with code '10'
```