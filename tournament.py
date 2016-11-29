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
        sql += ";"
        cursor.execute(sql)


def deleteTournamentPlayers(tournament=None):
    with connect() as conn, getcursor(conn) as cursor:
       sql = "DELETE FROM tournamentplayers"
       if tournament is not None:
          sql += " WHERE tournament_id = %s"
       sql += ";"
       cursor.execute(sql, [tournament])


def deletePlayers(ids=None):
    """Remove the player(s) records in tournament from the database."""
    with connect() as conn, getcursor(conn) as cursor:
        sql =  "DELETE from player"
        if ids is not None:
           sql += " WHERE id IN ("
           valuelist = ['%s' for i in range(len(ids))]
           sql += ', '.join(valuelist) + ')'
        sql += ";"
        cursor.execute(sql, ids)


def countPlayers(tournament=None):
    """Returns the number of players registered for tournament(s)."""
    nums = 0
    with connect() as conn, getcursor(conn) as cursor:
        sql = "SELECT count(*) as nums from player"
        if tournament is not None:
           sql += " JOIN tournamentplayers \
                    ON player.id = tournamentplayers.player_id \
                    WHERE tournamentplayers.tournament_id = %s"
        sql += ";"
        cursor.execute(sql, [tournament])
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
       return the tournament id number of last inserted.
    """
    with connect() as conn, getcursor(conn) as cursor:
        sql = "INSERT INTO tournament(name, year) VALUES (%s,%s) \
               RETURNING tournament_id;"
        if year is None:
            year = time.localtime().tm_year
        cursor.execute(sql, [name, year])
        return cursor.fetchone()[0]


def getTournamentIDs():
    """Returns list of tournament ids"""

    with connect() as conn, getcursor(conn) as cursor:
       sql = "SELECT tournament_id from tournament;"
       cursor.execute(sql)
       ids = cursor.fetchall()
       return ids


def registerPlayer(name, **kwargs):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.

    Args:
      name: the player's full name (need not be unique).
      kwargs: a dictionary with key: 'gender', 'dob' as additional information
      of the player, could be None
    Returns:
      The id number of the last inserted player.
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
        sql += ") values (" + ', '.join(valuelist) + ")"
        # need the last inserted id to add to tournamentplayers record 
        sql += " RETURNING id;"
        cursor.execute(sql, queryargs)
        return cursor.fetchone()[0]


def getPlayer(player_id):
    """Return player record"""
    with connect() as conn, getcursor(conn) as cursor:
       sql = "SELECT * FROM player WHERE id = %s;"
       cursor.execute(sql, [player_id])
       return cursor.fetchall()


def addPlayerToTournament(player_id, tournament_id):
    """Add player to tournament.
    Args:
       player_id: the id number of the player
       tournament_id: the id number of the tournament.
    """
    with connect() as conn, getcursor(conn) as cursor:
       sql = "INSERT INTO tournamentplayers(tournament_id, player_id) VALUES \
               (%s, %s);"
       cursor.execute(sql, [tournament_id, player_id])


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
       sql = "SELECT * FROM playerStandings_view WHERE tournament_id=%s;"


def reportMatch(winner_id, loser_id, match, tournament):
    """Records the outcome of a single match between two players in a tournament.

    Args:
      winner_id: the id number of the winner 
      loser_id: the id number of the loser 
      match: round of match
      tournament: the id number of the tournament
    """
    with connect() as conn, getcursor(conn) as cursor:
        sql = "INSERT INTO match (winner_id, loser_id, match, tournament) \
               values (%s, %s, %s, %s);"
        queryargs = [winner_id, loser_id, match, tournament]
        cursor.execute(sql, queryargs) 


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

