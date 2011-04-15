declare @startdate datetime = /* var:startdate */ '2010-04-01 00:00' /* end */
declare @enddate datetime = /* var:enddate */ '2010-10-26 00:00' /* end */
declare @classes varchar(max) = CAST(/* var:sizeclassid */ 5 /*end */ as varchar(max)) -- '5,6,7'
declare @fleet varchar(max) = /* var:fleetfilter */ null /* end */ -- 'Clean LR1'


/* log: "%s{16,120}: %s{10,120} -> %s{10,120}", getdate(), @startdate, @enddate */



