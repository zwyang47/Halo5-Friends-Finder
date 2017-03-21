Using the python script xboxhalo.py, the xbox data was scraped from xboxapi.com.
The following tables were populated from that api:
	PLAYERS, FRIENDS_OF, GAMES, GAMES_PLAYED

Using the same script, the halo 5 data was scraped from developer.haloapi.com.
The following tables were populated from that api:
	PLAYLISTS, SEASONS, RANKS, PLAYER_STATS

createTables.sql will setup the eight tables

insertAll.sql will populate the data.

Data was pulled on 318 players.
Of the 318 players, 375 uniques games were pulled with stats of all players for the games they played

Of the 318 players, 107 of them had played Halo 5, so stats were pulled for all those players
