-- Table definitions for the tournament project.

CREATE TABLE player(
   name text NOT NULL,
   id SERIAL PRIMARY KEY
);

CREATE TABLE tournament(
   name text NOT NULL,
   year smallint check(
       year between 0 and extract(year from current_date)
   ), 
   id SERIAL PRIMARY KEY
);

CREATE TABLE tournamentplayers (
   tournament_id integer REFERENCES tournament (id),
   player_id integer REFERENCES player (id),
   PRIMARY KEY (tournament_id, player_id)
);

CREATE TABLE match(
   winner_id integer REFERENCES player (id),
   loser_id integer REFERENCES player (id),
   match_id integer,
   tournament_id integer REFERENCES tournament (id),
   PRIMARY KEY (winner_id, loser_id, match_id, tournament_id)
);

-- Create a view as a result query of:
-- all player and the number of matches the player has won (wins)
-- and the number of matches the player has played (matches)
-- in all tournaments 
CREATE VIEW playerStandings_view AS
   SELECT player.id, player.name, count (match.winner_id) as wins,
          tournament.name as tournament
   FROM player
        LEFT JOIN match ON (player.id = match.winner_id)
        LEFT JOIN tournament ON (match.tournament_id = tournament.id)
   GROUP BY player.id, tournament.name ORDER BY wins;

CREATE VIEW matches_view AS
   SELECT player.id, match.winner_id, match.loser_id
   FROM player
        LEFT JOIN match ON (player.id = match.winner_id) OR
                           (player.id = match.loser_id)
        LEFT JOIN tournament ON (match.tournament_id = tournament.id)
