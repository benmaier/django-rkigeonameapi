# -*- coding: utf-8 -*-

import sys

from optparse import OptionParser
from configparser import ConfigParser

if __name__=="__main__":

    parser = OptionParser()
    #parser.add_option("-d", "--db-file", dest="db_file",
    #                  help="The database .cnf-file containing the relevant connection information.", metavar="FILE")
    #parser.add_option("-o", "--migration-file", dest="mig_file",
    #                  help="The .sql-file in which to store the migration commands. [default: %default]", metavar="FILE", default=None)
    parser.add_option("-l", "--language-code", dest="lang",
                      help="Which language to use for the default names of the Geoname objects. [default: %default]", default="de", type=str)

    (options, args) = parser.parse_args()

    if (len(args) != 2):
        print('This command requires two positional arguments: 1) the cnf-file to connect to the database and 2) an output file-name to create the SQL-commands for migration.')
        sys.exit(1)

    cnf = ConfigParser()
    cnf.read(args[0])

    with open('./sql/dummy_geonamemigration.sql','r') as f:
        sql = f.read()
        sql = sql.replace('your_db_name',cnf['client']['database'])

        if options.lang == 'en':
            options.lang = 'XXXXX'

        sql = sql.replace("isoLanguage = 'de'","isoLanguage = '{}'".format(options.lang.lower()))

    with open(args[1],'w') as f:
        f.write(sql)
