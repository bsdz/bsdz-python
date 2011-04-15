from sys import exc_info
from logging import getLogger, StreamHandler, DEBUG, INFO, Formatter
from subprocess import Popen, PIPE
from datetime import datetime
from traceback import format_tb
from optparse import OptionParser, OptionGroup
from re import sub, findall, match
from tempfile import mkstemp
from os import write, close, unlink

from pywin.debugger import brk

"""
usage: 

   TSqlParse.py -f"C:\BS_Apps\Scripts\TSqlParseSample.sql" -vstartdate='20090401' -venddate='20110430'

sample: -

declare @startdate datetime = /* var:startdate */ '2010-04-01 00:00' /* end */
declare @enddate datetime = /* var:enddate */ '2010-10-26 00:00' /* end */

declare @foo varchar(max) = CAST(/* var:foo */ 5 /*end */ as varchar(max)) 
declare @bar varchar(max) = /* var:bar */ null /* end */ 


/* log: "%s{16,120}: %s{10,120} -> %s{10,120}, foo is %s and bar is %s", getdate(), @startdate, @enddate, @foo, @bar */

"""
class TSqlParse():

    def __init__(self, sql_file, var_dict = dict()):
        self.sql_file = sql_file
        self.var_dict = var_dict

    def parse(self):
        orig_txt = file(self.sql_file).read()
        
        # replace all the commented vars, i.e. /* var:foo */ ... /* end */
        #
        def collect(matchobj, var_dict = self.var_dict):
            if matchobj.group(1) in var_dict:
                return var_dict[matchobj.group(1)]
            else:
                return matchobj.group(2)

        regex = '/\*\s*var:(\w+)\s*\*/(.*)/\*\s*end\s*\*/'
        new_txt = sub(regex, lambda x: sub(regex, collect , x.group(0)) , orig_txt)

        # replace all commented logs, i.e. /* log: "....", getdate(), @foo, @bar, ... */        
        #
        def collect2(matchobj):
            if len(matchobj.groups()) == 2:
                format_text = matchobj.group(1)
                sub_list = [i.strip() for i in matchobj.group(2).split(",")]

                regex = r"%s\{\S+\}|%s"
                place_holders = findall(regex, format_text)
                lengths = []
                styles = []
                for i, ph in enumerate(place_holders):
                    m_obj = match(r"%s{(\d*)(,\d+)?}", ph)
                    if m_obj:       
                        lengths.append(m_obj.group(1) if m_obj.group(1) else "max")
                        styles.append(m_obj.group(2) if m_obj.group(2) else "")
                    else:
                        lengths.append("max")
                        styles.append("")
                
                if len(place_holders) == len(sub_list):                   
                    new_format_text = sub(regex, lambda x: "' + convert(varchar(%s), isnull(%s,'NULL') %s) + '" 
                        % (lengths.pop(0), sub_list.pop(0), styles.pop(0)), format_text)

            return "set @__logmsg='%s'; raiserror(@__logmsg, 10, 1) with nowait" % new_format_text
        
        regex = '/\*\s*log:\s*"(.*)",\s*(.*)\*/'
        new_txt2 = sub(regex, lambda x: sub(regex, collect2 , x.group(0)), new_txt)
        
        return "declare @__logmsg varchar(2047)\r\n\r\n%s" % new_txt2        

def main():
    log = getLogger("TSqlParse")
    log.setLevel(DEBUG)

    console_logHandler = StreamHandler()
    console_logHandler.setFormatter(
        Formatter("%(levelname)s|%(asctime)s|%(filename)s:%(lineno)d|%(message)s"))
    console_logHandler.setLevel(DEBUG)
    log.addHandler(console_logHandler)
    log.setLevel(DEBUG) # INFO

    usage = "%prog [options]"
    description = "TSqlParse - run tsql with macro substitution"
    parser = OptionParser(usage=usage, description=description)

    main_options = OptionGroup(parser, "Main Options", 
        "The following actions are available.")

    main_options.add_option("-f", "--file",
        help="Specify a different date", metavar="FILEPATH",
        action="store", type="string", dest="sql_file")

    main_options.add_option("-v", "--var",
        help="Specify variables mappings", metavar="VAR=VALUE",
        action="append", type="string", dest="var_list")
        
    parser.add_option_group(main_options)
        
    sqlcmd_options = OptionGroup(parser, "SqlCmd Options", 
        "The following options are passed throught to sqlcmd.")
        
    sqlcmd_options.add_option("-S", "--server",
        help="Specify server", metavar="[PROTOCOL:]HOSTNAME[\DATABASE][,PORT]",
        action="store", type="string", dest="server")   

    sqlcmd_options.add_option("-H", "--hostname",
        help="Specify hostname", metavar="HOSTNAME",
        action="store", type="string", dest="hostname")           
        
    sqlcmd_options.add_option("-d", "--database",
        help="Specify database", metavar="DATABASE",
        action="store", type="string", dest="database")
        
    sqlcmd_options.add_option("--sqlcmd-options",
        help="Other SqlCmd options", metavar="EXTRA-OPTIONS",
        action="store", type="string", dest="sqlcmd_options")        

    parser.add_option_group(sqlcmd_options)

    try:
        (options, args) = parser.parse_args()

        if options.sql_file:

            if options.var_list:
                var_dict = dict([v.split("=") for v in options.var_list if v.find("=") > 0])
            
            sqlcmd_options = []
            
            if options.server:
                sqlcmd_options.append("-S%s" % options.server)
            
            if options.hostname:
                sqlcmd_options.append("-H%s" % options.hostname)                 
            
            if options.database:
                sqlcmd_options.append("-d%s" % options.database)
            else:
                raise Exception("No database specified")

            if options.sqlcmd_options:
                sqlcmd_options.append(options.sqlcmd_options)
            
            fd, filename = mkstemp(text=True)            
            tsqlparse = TSqlParse(options.sql_file, var_dict)                                         
            write(fd, tsqlparse.parse())
            close(fd)

            command = "sqlcmd -E %s -i\"%s\"" % (" ".join(sqlcmd_options), filename)
            log.info(command)
            p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
            output, errors = p.communicate()                    
            log.info(output.replace("\r\n", "\n"))            
            log.info("Job terminated with code '%s'" % p.returncode)         
            
            unlink(filename)
            exit(p.returncode)
        else:
            raise Exception("No file specified!")

    except Exception, e:
        message = "FAILED TO RUN: %s" % (e)        
        log.critical(message)
        message = "TRACEBACK:\n%s" % (''.join(format_tb(exc_info()[2])))
        log.debug(message)

    exit(1)


if __name__ == "__main__":
    main()
