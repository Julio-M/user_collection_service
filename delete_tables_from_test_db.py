import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Start a PostgreSQL database session

psqlCon = psycopg2.connect("dbname=usersdb user=${whoami} password=${whoami}");

psqlCon.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

# Open a database cursor

psqlCursor = psqlCon.cursor();

# Name of the table to be deleted

tableName = "users";

# Form the SQL statement - DROP TABLE

dropTableStmt = "DROP TABLE %s;" % tableName;

# Execute the drop table command

psqlCursor.execute(dropTableStmt);

# Free the resources

psqlCursor.close();

psqlCon.close();