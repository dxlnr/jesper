## PostgreSQL

Important commands for interacting with [PostgreSQL](https://www.postgresql.org/docs/15/index.html).
```bash
# Connect to postgres backend server.
sudo -i -u postgres
# Access the Postgres prompt.
psql
# Connect to specific DB.
psql -d jesper
# Get additional information.
psql --help
# Inspect tables in DB.
\dt
# Inspect table content in DB.
SELECT * FROM $tablename ;
```

Overall tutorial: [Install & setup PostgreSQL Server](https://www.cherryservers.com/blog/how-to-install-and-setup-postgresql-server-on-ubuntu-20-04).

###  How to start and stop PostgreSQL server?
By default, the postgres user has no password and can hence only connect if ran by the postgres system user. 
The following command will assign it:
```bash
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
sudo -u postgres psql -c "CREATE DATABASE testdb;"
```
Start the PostgreSQL server
```bash
sudo service postgresql start
```
Stop the PostgreSQL server:
```bash
sudo service postgresql stop
```

### (1) Using PostgreSQL Roles and Databases

Postgres uses a concept called *roles* to handle authentication and authorization. 

The installation procedure created a user account called **postgres** that is associated with the default Postgres role. To switch over to the postgres account on your server by running the following command:
```bash
sudo -i -u postgres
```

Then you can access the Postgres prompt by running:
```bash
psql
```

This will log you into the PostgreSQL prompt, and from here you are free to interact with the database management system right away.

To **exit** out of the PostgreSQL prompt, run the following:
```bash
postgres='#' \q
```

### (2) Creating a New Role

If you are logged in as the postgres account, you can create a new role by running the following command:
```bash
postgres@server:~$ createuser --interactive
# If sudo is preferred
sudo -u postgres createuser --interactive
```
Either way, the script will prompt you with some choices and, based on your responses, execute the correct Postgres commands to create a user to your specifications.
```bash
# Output
Enter name of role to add: daniel
Shall the new role be a superuser? (y/n) y
```

### (3) Creating a New Database

Another assumption that the Postgres authentication system makes by default is that for any role used to log in, that role will have a database with the same name which it can access.

This means that if the user you created in the last section is called *daniel*, that role will attempt to connect to a database which is also called *daniel* by default. You can create the appropriate database with the createdb command.

If you are logged in as the postgres account, you would type something like the following:
```bash
postgres@server:~$ createdb daniel
```

If sudo is preferred:
```bash
sudo -u postgres createdb daniel
```

### (4) Opening a Postgres Prompt with the New Role

To log in with ident based authentication, you’ll need a Linux user with the same name as your Postgres role and database.
```bash
sudo adduser daniel
```

Once this new account is available, you can either switch over and connect to the database by running the following:
```bash
sudo -u daniel psql
```

This command will log you in automatically, assuming that all of the components have been properly configured.

If you want your user to connect to a different database, you can do so by specifying the database like the following:
```bash
psql -d postgres
```

Once logged in, you can get check your current connection information by running:
```bash
daniel='#' \conninfo

# Output
You are connected to database "daniel" as user "daniel" via socket in "/var/run/postgresql" at port "5432".
```
