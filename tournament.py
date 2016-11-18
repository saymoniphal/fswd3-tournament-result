#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import config

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

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE from match")
    cur.close()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()

    """Since table match reference to player, need to delete records from
    match first"""
    cursor.execute("DELETE from match, delete from player")
    cur.close()
    conn.close()

def deleteTournament():
    """Remove all the tournament records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE from tournament")
    cur.close()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""

def registerTournament(name, year=None)
    """Add a tournament to the tournament database.
    The database assigns a unique serial id number for the tournament.

    Args:
       name: the tournament's name (need not be unique)
       year: the  year that the tournament taken place
       (current year will be added in case of None)
    """

def registerPlayer(name, kwargs=None):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
      kwargs: a dictionary with key: 'gender', 'dob' as additional information
      of the player, could be None
    """

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
