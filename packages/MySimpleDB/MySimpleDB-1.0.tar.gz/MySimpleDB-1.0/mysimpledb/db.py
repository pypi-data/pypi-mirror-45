#!/usr/bin/python3

import pymysql
from screenlogger.screenlogger import Msg


class DB:
    def __init__(self, dbuser, dbpass, dbname, logfilename, logpath, msgmode):
        self.msg = Msg(logfilename,
                       logpath,
                       msgmode)
        self.db = pymysql.connect("localhost",
                                  dbuser,
                                  dbpass,
                                  dbname)
        self.cursor = self.db.cursor()
        self.dbresults = None

    def __del__(self):
        """ opens a database connection
        """
        self.db.close()

    def get_results(self, sql, *args):
        """ Gets the results of an SQL statement
        """
        try:
            self.cursor.execute(pymysql.escape_string(sql), args)
            self.dbresults = self.cursor.fetchall()
        except Exception as e:
            self.msg.error_message(e)
            self.dbresults = False
            self.db.rollback()
            return False
        else:
            return len(self.dbresults)

    def commit(self, sql, *args):
        """ Commits the actions of an SQL
        statement to the database
        """
        try:
            self.cursor.execute(pymysql.escape_string(sql), args)
            self.db.commit()
        except Exception as e:
            self.msg.error_message(e)
            self.db.rollback()
            return False
        else:
            return True


# EOF
