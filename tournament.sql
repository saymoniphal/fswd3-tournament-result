-- Table definitions for the tournament project.

CREATE TABLE tournament (
   name text NOT NULL,
   year smallint check(
       year between 0 and extract(year from current_date)
   ),
   id SERIAL PRIMARY KEY
);

CREATE TABLE player (
   name text NOT NULL,
   gender text,
   dob date,
   id SERIAL PRIMARY KEY
);

CREATE TABLE tournamentplayers (
   tournament_id integer REFERENCES tournament (id),
   player_id integer REFERENCES player (id),
   PRIMARY KEY (tournament_id, player_id)
);

CREATE TABLE match(
   match_id SERIAL,
   tournament_id integer REFERENCES tournament (id),
   match_round integer NON NULL,
   loser_id integer REFERENCES player (id),
   winner_id integer REFERENCES player (id),
   PRIMARY KEY (match_id)
);

-- Create a PL/pgSQL Procedure to ensure that in same match and tournament,
-- the same player can not be a winner and a loser.
CREATE OR REPLACE FUNCTION control_match() RETURNS TRIGGER AS $control_match$
DECLARE
  result RECORD;
BEGIN
      SELECT count(*) as exists INTO result
        FROM match
        WHERE (loser_id = NEW.loser_id AND winner_id = NEW.winner_id)
           OR (loser_id = NEW.winner_id AND winner_id = NEW.loser_id);
      IF result.exists <> 0 THEN
        RAISE EXCEPTION 'duplicate match between % and % in same tournament',\
                        NEW.loser_id, NEW.winner_id;
      END IF;

      RETURN NEW;
END;
$control_match$ LANGUAGE plpgsql;

CREATE TRIGGER match_control BEFORE INSERT OR UPDATE on match
  FOR EACH ROW EXECUTE PROCEDURE control_match();

-- Create a view to get:
-- all player and the number of matches player has won (wins)
-- in all tournaments
CREATE VIEW playerwin_view AS
   SELECT player.id, player.name, COUNT (match.winner_id) as wins,
          tournament.name as tournament
   FROM player
        LEFT JOIN match ON (player.id = match.winner_id)
        LEFT JOIN tournament ON (match.tournament_id = tournament.id)
   GROUP BY player.id, tournament.name ORDER BY wins;

-- Create a view to get:
-- all player and the number of matches the player has played (matches)
-- in all tournaments
CREATE VIEW match_view AS
   SELECT player.id, player.name, COUNT (match.match_id) as matches,
          tournament.name as tournament
   FROM player
        LEFT JOIN match ON (player.id = match.winner_id) OR (player.id = match.loser_id)
        LEFT JOIN tournament ON (match.tournament_id = tournament.id)
   GROUP BY player.id, tournament.name ORDER BY matches;

CREATE VIEW playerStandings_view AS
   SELECT playerwin_view.tournament, playerwin_view.id, playerwin_view.name,
          match_view.matches, playerwin_view.wins from playerwin_view
   JOIN match_view on (playerwin_view.id = match_view.id) ORDER BY wins;
