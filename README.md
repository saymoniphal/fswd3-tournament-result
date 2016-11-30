## Project Overview
This goal of project is to built a database schema and python program to keep
track of players and matches in a game tournament using swiss-paring system.
This supports multiple tournaments.

## How to get source code
Use Git or checkout with SVN using the web url:
https://github.com/saymoniphal/fswd3-tournament-result.git

## How to run project
This project requires PosgreSQL database, you may run it on the system with
PosgreSQL server installed or use Vagrant virtual machine.

#### Use Vagrant virtual machine

1. Go to ```fswd3-tournament-result``` directory in the terminal,
Run command ```vagrant up``` (powers on the virtual machine),
Run command ```vagrant ssh``` (logs into the virtual machine),
2. run ```psql``` to connect to PosgreSQL database
3. run ```\i tournament.sql``` to import sql to create database and table definitions
4. run ```python tournament_test.sql``` to run testcases for functions
implemented in 'tournament.sql'

Example:

```
moniphal@titanium:~/git-trees/vagrant/fswd-p3-tournament-result$ vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Importing base box 'ubuntu/trusty32'...
==> default: Matching MAC address for NAT networking...
==> default: Checking if box 'ubuntu/trusty32' is up to date...
==> default: A newer version of the box 'ubuntu/trusty32' is available! You currently
==> default: have version '20161109.0.0'. The latest is version '20161122.0.0'. Run
==> default: `vagrant box update` to update.
==> default: Setting the name of the VM: fswd-p3-tournament-result_default_1480499539203_97178
==> default: Clearing any previously set forwarded ports...
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
...
...
```

```

moniphal@titanium:~/git-trees/vagrant/fswd-p3-tournament-result$ vagrant ssh
Welcome to Ubuntu 14.04.5 LTS (GNU/Linux 3.13.0-101-generic i686)

 * Documentation:  https://help.ubuntu.com/

 System information disabled due to load higher than 1.0

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

0 packages can be updated.
0 updates are security updates.

New release '16.04.1 LTS' available.
Run 'do-release-upgrade' to upgrade to it.

The shared directory is located at /vagrant
To access your shared files: cd /vagrant
Last login: Wed Nov 30 10:03:24 2016 from 10.0.2.2

```

```
vagrant@vagrant-ubuntu-trusty-32:~$ cd /vagrant/
vagrant@vagrant-ubuntu-trusty-32:/vagrant$ ls
config.py  database.ini  pg_config.sh  README.md  tournament.py  tournament.sql  tournament_test.py  Vagrantfile

vagrant@@vagrant-ubuntu-trusty-32:/vagrant$ ls
config.py  database.ini  README.md  tournament.py  tournament.sql  tournament_test.py

vagrant@vagrant-ubuntu-trusty-32:/vagrant$ psql
psql (9.3.15)
Type "help" for help.

vagrant=> \i tournament.sql

psql:tournament.sql:3: NOTICE:  database "tournament" does not exist, skipping
DROP DATABASE
CREATE DATABASE
You are now connected to database "tournament" as user "vagrant".

CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE FUNCTION
CREATE TRIGGER
CREATE VIEW
CREATE VIEW
CREATE VIEW

tournament=> \dt
              List of relations
 Schema |       Name        | Type  |  Owner  
--------+-------------------+-------+---------
 public | match             | table | vagrant
 public | player            | table | vagrant
 public | tournament        | table | vagrant
 public | tournamentplayers | table | vagrant
(4 rows)

tournament=> \dv
               List of relations
 Schema |         Name         | Type |  Owner  
--------+----------------------+------+---------
 public | match_view           | view | vagrant
 public | playerstandings_view | view | vagrant
 public | win_view             | view | vagrant
(3 rows)

tournament=> \q

```

```
vagrant@vagrant-ubuntu-trusty-32:/vagrant$ python tournament\_test.py 

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

|-- pg_config.sh and Vagrantfile: these files are taken from
http://github.com/udacity/fullstack-nanodegree-vm as part of Udacity course.
</pre>
