declare @startdate datetime = /* var:startdate */ '2010-04-01 00:00' /* end */
declare @enddate datetime = /* var:enddate */ '2010-10-26 00:00' /* end */

declare @foo varchar(max) = CAST(/* var:foo */ 5 /*end */ as varchar(max)) 
declare @bar varchar(max) = /* var:bar */ null /* end */ 


/* log: "%s{16,120}: %s{10,120} -> %s{10,120}, foo is %s and bar is %s", getdate(), @startdate, @enddate, @foo, @bar */


declare @exitcode int = 10

/* sqlcmd: exit(select @exitcode) */


