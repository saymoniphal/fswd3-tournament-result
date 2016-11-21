#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import config
import time

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    params = config.readconfig('database.ini')
    conn = psycopg2.connect(database=params['database'])
    return conn

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    with conn:
       cursor = conn.cursor()
       with cursor:
          cursor.execute("DELETE from match")
          conn.commit()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    with conn:
       cursor = conn.cursor()
       with cursor:
          """Since table match reference to player, need to delete records from
          match first"""
          cursor.execute("DELETE from match")
          cursor.execute('DELETE from player')
          conn.commit()

def deleteTournament():
    """Remove all the tournament records from the database."""
    conn = connect()
    with conn:
       cursor = conn.cursor()
       with cursor:
          cursor.execute("DELETE from tournament")
          conn.commit()

def countPlayers():
    """Returns the number of players registered for all tournaments."""
    nums = 0
    conn = connect()
    with conn:
       cursor = conn.cursor()
       with cursor:
          cursor.execute("SELECT count(*) as nums from player")
          nums = cursor.fetchone()[0]
    return nums

def countPlayers_in_tournament(tournament):
    """Returns the number of players registered for given tournament.
    Args:
        tournament: the tournament id
    """
    nums = 0
    conn = connect()
    with conn:
        cursor = conn.cursor()
        with cursor:
           cursor.execute("SELECT count(*) as nums from players")
           nums = cursor.fetchone()[0]
    return nums

def registerTournament(name, year=None):
    """Add a tournament to the tournament database.
    The database assigns a unique serial id number for the tournament.

    Args:
       name: the tournament's name (need not be unique)
       year: the  year that the tournament taken place
       (current year will be added in case of None)
    """
    conn = connect()
    with conn:
       cursor = conn.cursor()
       with cursor:
          sql = "INSERT INTO %s VALUES (%s)"
          if year is None:
             year = time.localtime().tm_year
          cursor.execute(sql, ('tournament', name, year))
          conn.commit()

def registerPlayer(name, **kwargs):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
      kwargs: a dictionary with key: 'gender', 'dob' as additional information
      of the player, could be None
    """
    conn = connect()
    with conn:
       cursor = conn.cursor()
       with cursor:
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
          cursor.execute(sql, queryargs)
          conn.commit()

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
    conn = connect()
    with conn:
       cursor = conn.cursor()
       with cursor:
          pass


def reportMatch(winner, loser, tournament):
    """Records the outcome of a single match between two players in a tournament.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament: the id number of the tournament
    """
    conn = connect()
    with conn:
       cursor = conn.cursor()
       with cursor:
          pass
 
 
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
    conn = connect()
    with conn:
       cursor = conn.cursor()
       with cursor:
          pass
