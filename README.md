## Project Overview
This goal of project is to built a database schema and python program to keep
track of players and matches in a game tournament using swiss-paring system.

## How to run project

The project uses PosgreSQL database.
1. run 'psql' to connect to PosgreSQL database
2. import 'tournament.sql' file to create database and table definitions
3. run python scrip 'tournament\_test.sql' to run testcases for functions implemented in 'tournament.sql'

Example:

```
vagrant@@vagrant-ubuntu-trusty-32:/vagrant/tournament$ ls
config.py  database.ini  README.md  tournament.py  tournament.sql  tournament_test.py

vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql
psql (9.3.15)
Type "help" for help.

vagrant=> \i tournament.sql

DROP DATABASE
CREATE DATABASE
You are now connected to database "tournament" as user "vagrant".

psql:tournament.sql:8: NOTICE:  table "tournament" does not exist, skipping
DROP TABLE
CREATE TABLE
psql:tournament.sql:18: NOTICE:  table "player" does not exist, skipping
DROP TABLE
CREATE TABLE
psql:tournament.sql:27: NOTICE:  table "tournamentplayers" does not exist, skipping
DROP TABLE
CREATE TABLE
psql:tournament.sql:35: NOTICE:  table "match" does not exist, skipping
DROP TABLE
CREATE TABLE
CREATE FUNCTION
CREATE TRIGGER
psql:tournament.sql:71: NOTICE:  view "win_view" does not exist, skipping
DROP VIEW
CREATE VIEW
psql:tournament.sql:84: NOTICE:  view "match_view" does not exist, skipping
DROP VIEW
CREATE VIEW
psql:tournament.sql:94: NOTICE:  view "playerstandings_view" does not exist, skipping
DROP VIEW
CREATE VIEW
tournament=> \q

vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament\_test.py 

1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers(tournament=1) returns 1 after one player is registered to tournament 1.
3. countPlayers(tournament=1) returns 2 after two players are registered.
4. countPlayers() returns 2 after two players are registered.
5. After deletePlayer([1]), getPlayer(1) return zero record.
6. countPlayers() returns zero after registered players are deleted.
7. Player records successfully deleted.
8. Newly registered players appear in the standings with no matches.
9. After a match, players have updated standings.
10. After match deletion, player standings are properly reset.
11. Matches are properly deleted.
12. After one match, players with one win are properly paired.
Success!  All tests pass!
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ 
```
## How to get source code
Use Git or checkout with SVN using the web url:
https://github.com/saymoniphal/fswd3-tournament-result.git

#### clone using git:
Run command:
```
git clone https://github.com/saymoniphal/fswd3-tournament-result.git
```
## Project structure
The database used in this project is Postgresql.

The project structure is as below:
<pre>
|-- README.md
|-- tournament.sql: setup database schema (database and tables definitions ) 
|-- tournament.py: provides access to the database to add, delete, query data
|-- tournament\_test.py: provides unit tests for the funtionality implemented
in tournament.py
|-- database.ini: contains database configuration (database name)
|-- config.py: provides access to database.ini file.
</pre>

