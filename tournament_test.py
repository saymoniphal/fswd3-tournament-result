#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.

from tournament import *

def testRegister():
    """Test for registration of tournament and players """
def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    deleteTournamentPlayers()
    deleteMatches()
    deleteTournaments()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, countPlayers should return zero.")
    print "1. countPlayers() returns 0 after initial deletePlayers() execution."
    tournament_id = registerTournament("Tour1")
    p_id1 = registerPlayer("Chandra Nalaar")
    addPlayerToTournament(p_id1, tournament_id)
    c = countPlayers(tournament_id)
    if c != 1:
        raise ValueError(
            "After one player registers to tournament {t_id}, "
            "countPlayers(tournament={t_id}) should be 1. Got {c}".format(
                          t_id=tournament_id,c=c))
    print("2. countPlayers(tournament={t_id}) returns 1 after one player is "
           "registered to tournament {t_id}.".format(t_id=tournament_id))
    p_id2 = registerPlayer("Jace Beleren")
    addPlayerToTournament(p_id2, tournament_id)
    c = countPlayers(tournament_id)
    if c != 2:
        raise ValueError("After two players register, countPlayers() should "
                         "be 2. Got {c}".format(c=c))
    print("3. countPlayers(tournament={t_id}) returns 2 after two players are "
           "registered.".format(t_id=tournament_id))

    c = countPlayers()
    if c != 2:
        raise ValueError("After two players register to tou, countPlayers() "
                         "should be 2. Got {c}".format(c=c))
    print "4. countPlayers() returns 2 after two players are registered."
    
    deleteTournamentPlayers()
    deletePlayers([p_id1])
    rec = getPlayer(p_id1)
    if len(rec) > 1:
        raise ValueError(
            "After deleting player id {pid}, getPlayer({pid} should return zero"
            " record but Got {rec}".format(pid=p_id1,rec=rec.len()))
    print("5. After deletePlayer([{p_id}]), getPlayer({p_id}) return zero "
          "record.".format(p_id=p_id1))
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deletion all players, countPlayers should "
                         "return zero but got {c}.".format(c=c))
    print "6. countPlayers() returns zero after registered players are deleted."
    print "7. Player records successfully deleted."

def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    deleteMatches()
    deletePlayers()
    tournament_id = registerTournament("Tour2")
    p_id1 = registerPlayer("Melpomene Murray")
    addPlayerToTournament(p_id1, tournament_id)
    p_id2 = registerPlayer("Randy Schwartz")
    addPlayerToTournament(p_id2, tournament_id)
    standings = playerStandings(tournament_id)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "8. Newly registered players appear in the standings with no matches."

def testReportMatches():
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    deleteTournamentPlayers()
    deleteTournaments()
    deleteMatches()
    deletePlayers()
    registerTournament("Tour1")
    tournament_ids = getTournamentIDs()
    p1 = registerPlayer("Bruno Walton")
    addPlayerToTournament(p1, tournament_ids[0])
    p2 = registerPlayer("Boots O'Neal")
    addPlayerToTournament(p2, tournament_ids[0])
    p3 = registerPlayer("Cathy Burton")
    addPlayerToTournament(p3, tournament_ids[0])
    p4 = registerPlayer("Diane Grant")
    addPlayerToTournament(p4, tournament_ids[0])

    standings = playerStandings(tournament_ids[0])
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, 1, tournament_ids[0])
    reportMatch(id3, id4, 1, tournament_ids[0])
    standings = playerStandings(tournament_ids[0])
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "9. After a match, players have updated standings."
    deleteMatches()
    standings = playerStandings(tournament_id[0])
    if len(standings) != 4:
        raise ValueError("Match deletion should not change number of players in standings.")
    for (i, n, w, m) in standings:
        if m != 0:
            raise ValueError("After deleting matches, players should have zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have zero wins recorded.")
    print "10. After match deletion, player standings are properly reset.\n9. Matches are properly deleted."

def testPairings():
    """
    Test that pairings are generated properly both before and after match reporting.
    """
    deleteTournaments()
    deleteMatches()
    deletePlayers()
    registerTournament("Tour1")
    tournament_ids = getTournamentIDs()
    registerPlayer("Twilight Sparkle", tournament_ids[0])
    registerPlayer("Fluttershy", tournament_ids[0])
    registerPlayer("Applejack", tournament_ids[0])
    registerPlayer("Pinkie Pie", tournament_ids[0])
    registerPlayer("Rarity", tournament_ids[0])
    registerPlayer("Rainbow Dash", tournament_ids[0])
    registerPlayer("Princess Celestia", tournament_ids[0])
    registerPlayer("Princess Luna", tournament_ids[0])
    standings = playerStandings(tournament_ids[0])
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    reportMatch(id1, id2, 1, tournament_ids[0])
    reportMatch(id3, id4, 1, tournament_ids[0])
    reportMatch(id5, id6, 1, tournament_ids[0])
    reportMatch(id7, id8, 1, tournament_ids[0])
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "11. After one match, players with one win are properly paired."


if __name__ == '__main__':
    testCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"
