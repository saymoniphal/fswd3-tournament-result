#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import config
import time

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    try:
       """Read connection parameters"""
        params = config.readconfig()
        conn = psycopg2.connect(host=params{'host'},
                                database=params{'database'})
        return conn 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
           conn.close()

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE from match")
    conn.commit()
    cursor.close()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()

    """Since table match reference to player, need to delete records from
    match first"""
    cursor.execute("DELETE from match, delete from player")
    conn.commit()
    cursor.close()
    conn.close()

def deleteTournament():
    """Remove all the tournament records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE from tournament")
    conn.commit()
    cursor.close()
    conn.close()

def countPlayers():
    """Returns the number of players registered for all tournaments."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) as nums from players")
    nums = cursor.fetchone()
    cursor.close()
    conn.close()
    return nums

def countPlayers_in_tournament(tournament):
    """Returns the number of players registered for given tournament.
    Args:
        tournament: the tournament id
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) as nums from players")
    nums = cursor.fetchone()
    cursor.close()
    conn.close()
    return nums

def registerTournament(name, year=None)
    """Add a tournament to the tournament database.
    The database assigns a unique serial id number for the tournament.

    Args:
       name: the tournament's name (need not be unique)
       year: the  year that the tournament taken place
       (current year will be added in case of None)
    """
    sql = "INSERT INTO %s VALUES (%s)"
    if year is None:
       year = time.localtime().tm_year
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(sql, ('tournament', name, year))
    conn.commit()
    cursor.close()
    conn.close()

def registerPlayer(name, kwargs=None):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
      kwargs: a dictionary with key: 'gender', 'dob' as additional information
      of the player, could be None
    """
    sql = "INSERT INTO %s (name"
    if 'gender' in kwargs:
       gender = kwargs['gender']
       sql += ", gender"
    if 'dob' in kwargs:
       dob = kwargs['dob'] 
       sql += ", dob"
    sql += ") values (%)"
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(sql, ('player', name, gender, dob))
    conn.commit()
    cursor.close()
    conn.close()

def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
      tournament: the id number of the tournament
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser, tournament):
    """Records the outcome of a single match between two players in a tournament.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament: the id number of the tournament
    """
 
 
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
