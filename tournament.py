#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import contextlib
import time

import psycopg2

import config


"""context manager decorator for database connection for 'with' statement
   avoiding repeating line of codes on connection commit, and close.
"""
@contextlib.contextmanager
def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    conn = None
    try:
        params = config.readconfig('database.ini')
        conn = psycopg2.connect(database=params['database'])
        yield conn
        conn.commit()
    except:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


@contextlib.contextmanager
def getcursor(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        yield cursor
    finally:
        if cursor:
            cursor.close()


def deleteMatches(tournament=None):
    """Remove the match records in tournament(s) from the database.
    Arg:
       tournament (optional): the tournament id to remove matches from.
       If None, then All match records of all tournaments will be removed.
    """
    with connect() as conn, getcursor(conn) as cursor:
        sql = "DELETE from match"
        if tournament:
           sql += " WHERE tournament_id=" + tournament
        cursor.execute(sql)


def deleteTournaments(tournament=None):
    """Remove the tournament record(s) from the database. If tournament id
       is None, then remove all the tournament records."""
    with connect() as conn, getcursor(conn) as cursor:
        sql = "DELETE FROM tournament"
        if tournament is not None:
           sql += " WHERE id = " + tournament
        cursor.execute(sql)


def deletePlayers(tournament=None):
    """Remove all the player records in tournament(s) from the database."""
    with connect() as conn, getcursor(conn) as cursor:
        sql =  "DELETE from"
        if tournament is None:
           sql += " player"
        else:
           sql += " player WHERE id IN (SELECT player_id FROM tournamentplayers\
                    WHERE tournament_id = %s);"
        cursor.execute(sql, [tournament])


def deleteTournamentPlayers():
    """Remove all the player records from the database."""
    with connect() as conn, getcursor(conn) as cursor:
        cursor.execute('DELETE from player')


def countPlayers(tournament=None):
    """Returns the number of players registered for tournament(s)."""
    nums = 0
    with connect() as conn, getcursor(conn) as cursor:
        sql = "SELECT count(*) as nums from player"
        if tournament is not None:
           sql += " JOIN tournamentplayers \
                    ON   hplayer.id = tournamentplayers.player_id \
                    WHERE tournamentplayers.tournament_id = " + tournament
        cursor.execute(sql)
        nums = cursor.fetchone()[0]
    return nums


def countPlayers_in_tournament(tournament):
    """Returns the number of players registered for given tournament.
    Args:
        tournament: the tournament id
    """
    nums = 0
    with connect() as conn, getcursor(conn) as cursor:
        sql = "SELECT count(*) as nums from tournamentplayers \
               WHERE tournament_id=%s;", tournament
        cursor.execute(sql, tournament)
        nums = cursor.fetchone()[0]
    return nums


def registerTournament(name, year=None):
    """Add a tournament to the tournament database.
    The database assigns a unique serial id number for the tournament.

    Args:
       name: the tournament's name (need not be unique)
       year: the  year that the tournament taken place
       (current year will be added in case of None)
    Returns:
       return the tournament id.
    """
    with connect() as conn, getcursor(conn) as cursor:
        sql = "INSERT INTO tournament(name, year) VALUES (%s,%s);"
        if year is None:
            year = time.localtime().tm_year
        cursor.execute(sql, [name, year])


def getTournamentIDs():
    """Returns list of tournament ids"""

    with connect() as conn, getcursor(conn) as cursor:
       sql = "SELECT id from tournament;"
       cursor.execute(sql)
       ids = cursor.fetchall()
       return ids


def registerPlayer(name, tournament, **kwargs):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
      tournament: the id of the tournament.
      kwargs: a dictionary with key: 'gender', 'dob' as additional information
      of the player, could be None
    """
    with connect() as conn, getcursor(conn) as cursor:
        sql = "INSERT INTO player (name"
        queryargs = [name]
        valuelist = ['%s']
        if 'gender' in kwargs:
            queryargs.append(kwargs['gender'])
            valuelist.append('%s')
            sql += ", gender"
        if 'dob' in kwargs:
            queryargs.append(kwargs['dob'])
            valuelist.append('%s')
            sql += ", dob"
        sql += ") values (" + ', '.join(valuelist) + ");"
        cursor.execute(sql, queryargs)


def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Args:
      tournament: the id number of the tournament
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played

    """
    with connect() as conn, getcursor(conn) as cursor:
        pass


def reportMatch(id1, id2, match=None, tournament=None):
    """Records the outcome of a single match between two players in a tournament.

    Args:
      id1: the id number of the first player
      id2: the id number of the second player
      match: round of match(if None, all match rounds will be consider)
      tournament: the id number of the tournament(consider all if None)
    """
    with connect() as conn, getcursor(conn) as cursor:
        sql = "SELECT * FROM match WHERE winner_id IN (%s, %s) AND \
               loser_id IN (%s, %s)"
        queryargs = [id1, id2, id1, id2]
        if match is not None:
            sql += " AND match_round = %s"
            queryags.push(match)
        if tournament is not None:
            sql += " AND tournament = %s"
            queryargs.push(tournament)
        sql += ";" 
        cursor.execute(sql, [id1, id2, id1, id2]) 


def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
      tournament: the id number of the tournament

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    with connect() as conn, getcursor(conn) as cursor:
        pass

