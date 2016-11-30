#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import contextlib
import time

import psycopg2

import config


@contextlib.contextmanager
def connect():
    """Connect to the PostgreSQL database.  Returns a database connection.
       Use context manager decorator for database connection for 'with'
       statement, avoid repeated codes on connection commit, and close."""

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


def _run_sql(sql, args=None, fetch=True):
    """Connect to PosgreSQL database and execute the query
       Args:
         sql: sql query to be executed
         args: argument for the sql query
       Returns:
         sql query results
    """
    results = []
    with connect() as conn, getcursor(conn) as cursor:
        cursor = conn.cursor()
        cursor.execute(sql, args)
        if fetch:
            results = cursor.fetchall()
    return results


def deleteMatches(tournament=None):
    """Remove the match records in tournament(s) from the database.
    Arg:
       tournament (optional): the tournament id to remove matches from.
       If None, then All match records of all tournaments will be removed.
    """
    sql = "DELETE from match"
    if tournament:
        sql += " WHERE tournament_id=" + tournament
    sql += ";"
    _run_sql(sql, fetch=False)


def deleteTournaments(tournament=None):
    """Remove the tournament record(s) from the database. If tournament id
       is None, then remove all the tournament records."""
    if tournament is not None:
        sql = "DELETE FROM tournament WHERE id = %s;"
        args = (tournament,)
    else:
        sql = "DELETE FROM tournament;"
        args = tuple()
    _run_sql(sql, args, fetch=False)


def deleteTournamentPlayers(tournament=None):
    if tournament is not None:
        sql = "DELETE FROM tournamentplayers where tournament_id = %s;"
        args = (tournament,)
    else:
        sql = "DELETE FROM tournamentplayers;"
        args = (tournament,)
    _run_sql(sql, args, fetch=False)


def deletePlayers(ids=None):
    """Remove the player(s) records in tournament from the database."""
    sql = "DELETE from player"
    if ids is not None:
        sql += " WHERE id IN ("
        valuelist = ['%s' for i in range(len(ids))]
        sql += ', '.join(valuelist) + ')'
    sql += ";"
    _run_sql(sql, ids, fetch=False)


def countPlayers(tournament=None):
    """Returns the number of players registered for tournament(s)."""
    nums = 0
    sql = "SELECT count(*) as nums from player"
    if tournament is not None:
        sql += " JOIN tournamentplayers \
                    ON player.id = tournamentplayers.player_id \
                    WHERE tournamentplayers.tournament_id = %s"
    sql += ";"
    args = (tournament,)
    res = _run_sql(sql, args)
    nums = res[0][0]
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
    sql = "INSERT INTO tournament(name, year) VALUES (%s,%s) \
           RETURNING tournament_id;"
    if year is None:
        year = time.localtime().tm_year
    results = _run_sql(sql, [name, year])
    return results[0][0]


def getTournamentIDs():
    """Returns list of tournament ids"""

    sql = "SELECT tournament_id from tournament;"
    return _run_sql(sql)


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
    sql = "INSERT INTO player (name"
    kwargs['name'] = name
    namedlist = ['%(name)s']
    if 'gender' in kwargs:
        namedlist.append('%(gender)s')
        sql += ", gender"
    if 'dob' in kwargs:
        namedlist.append('%(dob)s')
        sql += ", dob"
    sql += ") values (" + ', '.join(namedlist) + ")"
    # need the last inserted id to add to tournamentplayers record
    sql += " RETURNING id;"
    results = _run_sql(sql, kwargs)
    return results[0][0]


def getPlayer(player_id):
    """Return player record"""
    sql = "SELECT * FROM player WHERE id = %s;"
    return _run_sql(sql, [player_id])


def addPlayerToTournament(player_id, tournament_id):
    """Add player to tournament.
    Args:
       player_id: the id number of the player
       tournament_id: the id number of the tournament.
    """
    sql = "INSERT INTO tournamentplayers(tournament_id, player_id) VALUES \
           (%s, %s);"
    _run_sql(sql, (tournament_id, player_id,), fetch=False)


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
    sql = "SELECT * FROM playerStandings_view;"
    return _run_sql(sql)


def reportMatch(winner_id, loser_id, match_round, tournament_id):
    """Records the outcome of a single match between two players in a tournament.

    Args:
      winner_id: the id number of the winner
      loser_id: the id number of the loser
      match: round of match
      tournament: the id number of the tournament
    """
    sql = "INSERT INTO match (winner_id, loser_id, match_round, \
           tournament_id) VALUES (%s, %s, %s, %s);"
    queryargs = [winner_id, loser_id, match_round, tournament_id]
    _run_sql(sql, queryargs, fetch=False)


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
    standings = playerStandings(tournament)
    id_names = [(elem[0], elem[1]) for elem in standings]
    return [(elem[0][0], elem[0][1], elem[1][0], elem[1][1])
            for elem in zip(id_names[::2], id_names[1::2])]
