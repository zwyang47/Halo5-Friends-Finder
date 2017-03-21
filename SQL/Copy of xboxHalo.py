import requests
import json

# XboxApi key
xbox_api_key = "07cd76bd1544e99f7a1612f0cb253682b905369f"

#Halo key
halo_api_key = "6ef9dea897d5422f856d67d58d898149"

def main():
    #All Xbox Api Calls (JSON returned)
    
    #currently only for BigLew117

    #print_players_and_friends_inserts()

    #print_players_games()
       
    #print_player_game_stats()

    #response = get_games("2533274826802377")
    #games_list = response['titles']
    #for game in games_list:
    #     print game['name']
    #     print game['titleId']

    #response = get_game_stats("2533274826802377", "1019936697")
    #print json.dumps(response, indent=4)
    #timeFound = None 
    #sublist = response['statlistscollection']
    #statsdict = sublist[0]
    #statslist = statsdict['stats']
    #for item in statslist:
    #    if item['name'].find('GameProgress') != -1:
    #        print item['value']
    #    if item['name'].find('MinutesPlayed') != -1:
    #        print item['value']
    #        timeFound = True

    #if not timeFound:
    #    sublist = response['groups']
    #    subdict = sublist[0]
    #    sublist2 = subdict['statlistscollection']
    #    statsdict = sublist2[0]
    #    statslist = statsdict['stats']
    #    for item in statslist:
    #         if item['name'].find('HoursPlayed') != -1:
    #            print item['value'] * 60


    #playtime = statslist[0]
    #gameprogress = statslist[1]
    #print playtime['value']
    #print gameprogress['value']


    #All Halo Api Calls (JSON returned)

    #print_csr_inserts()
    
    #print_season_inserts()
    
    #print_playlist_inserts()

    #response = get_arena_player_stats("biglew117", "2041d318-dd22-47c2-a487-2818ecf14e41")
    #results = response['Results']
    #result = results[0]
    #lowerResult = result['Result']
    #arenaStats = lowerResult['ArenaStats']
    #arenaPlaylistStats = arenaStats['ArenaPlaylistStats']
    #for playlist in arenaPlaylistStats:
    #    print playlist['PlaylistId']
    #    print playlist['TotalGamesCompleted']
    #    print playlist['TotalGamesWon']
    #    print playlist['TotalGamesLost']
    #    csr = playlist['HighestCsr']
    #    if csr is not None:
    #       print csr['DesignationId']
    #       print csr['Tier']


    #response = get_warzone_player_stats("biglew117") 
    #results = response['Results']
    #result = results[0]
    #lowerResult = result['Result']
    #warzoneStats = lowerResult['WarzoneStat']
    #print warzoneStats['TotalGamesCompleted']
    #print warzoneStats['TotalGamesWon']
    #print warzoneStats['TotalGamesLost']

def print_player_game_stats():
    myXuid =  get_xuid("DiZzY fUn") 

    response = get_games(myXuid)
    games_list = response['titles']
    for game in games_list:
        if game['name'].find('Xbox One') == 0:
            print "\n" 
        elif game['titleType'].find('DGame') != -1:
            timeFound = None 
            response = get_game_stats(myXuid, game['titleId'])
            sublist = response['statlistscollection']
            statsdict = sublist[0]
            statslist = statsdict['stats']
            for item in statslist:
                if item['name'].find('GameProgress') != -1:
                    if 'value' in item:
                        gameProg = item['value']
                if item['name'].find('MinutesPlayed') != -1:
                    timePlayed = item['value']
                    timeFound = True

            if not timeFound:
                sublist = response['groups']
                subdict = sublist[0]
                sublist2 = subdict['statlistscollection']
                statsdict = sublist2[0]
                statslist = statsdict['stats']
                for item in statslist:
                    if item['name'].find('HoursPlayed') != -1:
                        timePlayed = item['value'] * 60

            print 'INSERT INTO GAMES_PLAYED (PlayerXUID, GID, TimePlayed, GameProgress)'
            print('   VALUES ({}, {}, {}, {});'.format(myXuid, game['titleId'], timePlayed, gameProg))
    return

def print_players_games():
    xuids = open('dump.txt', 'r').read()
    xuidList = xuids.split('\n')

    fGames = open('insertGames.sql', 'a')
    fGamesPlayed = open('insertGamesPlayed.sql', 'a')
    print len(xuidList)
    counter = 1
    for xuid in xuidList:
        if len(xuid) > 10:
            print counter
            counter += 1
            response = get_games(xuid)
            if 'titles' in response:
                games_list = response['titles']
                for game in games_list:
                    if game['name'].find('Xbox One') == 0:
                        blah = None
                    if game['titleType'].find('DGame') != -1:
                        fGames.write('INSERT INTO GAMES (GameTitle, GameID)\n')
                        if game['name'].find('\'') != -1:
                            line = game['name'].encode('utf8') 
                            line = line.translate(None, '\'')
                            game['name'] = line
                            fGames.write('   VALUES (\'{}\', {});\n'.format(game['name'], game['titleId']))
                        else:
                            fGames.write('   VALUES (\'{}\', {});\n'.format(game['name'].encode('utf8'), game['titleId']))
                    if game['name'].find('Xbox One') == 0:
                        print "\n"
                    elif game['titleType'].find('DGame') != -1:
                        timeFound = None
                        response = get_game_stats(xuid, game['titleId'])
                        if 'statlistscollection' in response:
                            sublist = response['statlistscollection']
                            statsdict = sublist[0]
                            statslist = statsdict['stats']
                            for item in statslist:
                                if item['name'].find('GameProgress') != -1:
                                    if 'value' in item:
                                        gameProg = item['value']
                                if item['name'].find('MinutesPlayed') != -1:
                                    if 'value' in item:
                                        timePlayed = item['value']
                                    else:
                                        timePlayed = 0
                                    timeFound = True

                            if not timeFound:
                                sublist = response['groups']
                                subdict = sublist[0]
                                sublist2 = subdict['statlistscollection']
                                statsdict = sublist2[0]
                                statslist = statsdict['stats']
                                for item in statslist:
                                    if item['name'].find('HoursPlayed') != -1:
                                        timePlayed = item['value'] * 60

                            fGamesPlayed.write('INSERT INTO GAMES_PLAYED (PlayerXUID, GID, TimePlayed, GameProgress)\n')
                            fGamesPlayed.write('   VALUES ({}, {}, {}, {});\n'.format(xuid, game['titleId'], timePlayed, gameProg))

    return

def print_players_and_friends_inserts():
    myXuid =  get_xuid("BigLew117") 
    fPlayers = open('insertPlayers.sql', 'a')
    fPlayers.write('INSERT INTO PLAYERS (Gamertag, XUID)\n')
    fPlayers.write('    VALUES (\'Biglew117\', {});\n'.format(myXuid))

    friends_list = get_friends(myXuid)
    for friend in friends_list:
        if 'Gamertag' in friend and 'id' in friend:
            fPlayers.write('INSERT INTO PLAYERS (Gamertag, XUID)\n')
            fPlayers.write('    VALUES (\'{}\', {});\n'.format(friend['Gamertag'], friend['id']))
        sub_friends_list = get_friends(friend['id'])
        for sub_friend in sub_friends_list:
            if 'Gamertag' in sub_friend and 'id' in sub_friend:
                fPlayers.write('INSERT INTO PLAYERS (Gamertag, XUID)\n')
                fPlayers.write('    VALUES (\'{}\', {});\n'.format(sub_friend['Gamertag'], sub_friend['id']))
            #sub1_friends_list = get_friends(sub_friend['id'])
            #for sub1_friend in sub1_friends_list:
            #    if 'Gamertag' in sub1_friend and 'id' in sub1_friend:
            #        fPlayers.write('INSERT INTO PLAYERS (Gamertag, XUID)\n')
            #        fPlayers.write('    VALUES (\'{}\', {});\n'.format(sub1_friend['Gamertag'], sub1_friend['id']))

    fFriends = open('insertFriends.sql', 'a')
    for friend in friends_list:
        if 'Gamertag' in friend and 'id' in friend:
            fFriends.write('INSERT INTO FRIENDS_OF (PXUID, FXUID)\n')
            fFriends.write('    VALUES ({}, {});\n'.format(myXuid, friend['id']))
        sub_friends_list = get_friends(friend['id'])
        for sub_friend in sub_friends_list:
            if 'id' in friend and 'id' in sub_friend:
                fFriends.write('INSERT INTO FRIENDS_OF (PXUID, FXUID)\n')
                fFriends.write('    VALUES ({}, {});\n'.format(friend['id'], sub_friend['id']))
            #sub1_friends_list = get_friends(sub_friend['id'])
            #for sub1_friend in sub1_friends_list:
            #    if 'id' in sub_friend and 'id' in sub1_friend:
            #        fFriends.write('INSERT INTO FRIENDS_OF (PXUID, FXUID)\n')
            #        fFriends.write('    VALUES ({}, {});\n'.format(sub_friend['id'], sub1_friend['id']))

    fPlayers.close()
    fFriends.close()
    return

def print_csr_inserts():
    csr_list =  get_csr_designations()
    for rank in csr_list:
        print 'INSERT INTO RANKS (RankID, RankName)'
        print('   VALUES ({}, \'{}\');'.format(rank['id'], rank['name']))
    return

def print_season_inserts():
    season_list = get_seasons()
    counter = 0
    for season in season_list:
        print 'INSERT INTO SEASONS (SName, STag, SID)'
        print('   VALUES (\'{}\', \'{}\', \'{}\');'.format(season['name'], season['id'], counter))
        counter += 1
    return

def print_playlist_inserts():
    playlist_list = get_playlists()
    counter = 0
    for playlist in playlist_list:
        print 'INSERT INTO PLAYLISTS (PName, PTag, PID)'
        print('   VALUES (\'{}\', \'{}\', \'{:2}\');'.format(playlist['name'], playlist['id'], counter))
        counter += 1
    return

def requestHaloApi(url, params={}):
    headers = {"Ocp-Apim-Subscription-Key" : halo_api_key}
    p = {}
    for k, v in params.items():
        if k not in p and v:
            p[k] = v

    res = requests.get(url, params=p, headers=headers)
    return res

def requestXboxApi(url):
    headers = {"X-AUTH" : xbox_api_key}
    res = requests.get(url, headers=headers)
    return res

def get_csr_designations():
    res = requestHaloApi("https://www.haloapi.com/metadata/h5/metadata/csr-designations")
    return res.json()

def get_seasons():
    res = requestHaloApi("https://www.haloapi.com/metadata/h5/metadata/seasons")
    return res.json()

def get_playlists():
    res = requestHaloApi("https://www.haloapi.com/metadata/h5/metadata/playlists")
    return res.json()

def get_arena_player_stats(gamertag, seasonId):
    res = requestHaloApi("https://www.haloapi.com/stats/h5/servicerecords/arena", {'players': gamertag,'seasonId': seasonId})
    return res.json()

def get_warzone_player_stats(gamertag):
    res = requestHaloApi("https://www.haloapi.com/stats/h5/servicerecords/warzone", {'players': gamertag})
    return res.json()

def get_xuid(gamertag):
    res = requestXboxApi("https://xboxapi.com/v2/xuid/{}".format(gamertag))
    return res.json()

def get_friends(xuid):
    res = requestXboxApi("https://xboxapi.com/v2/{}/friends".format(xuid))
    return res.json()

def get_games(xuid):
    res = requestXboxApi("https://xboxapi.com/v2/{}/xboxonegames".format(xuid))
    return res.json()

def get_game_stats(xuid, titleid):
    res = requestXboxApi("https://xboxapi.com/v2/{}/game-stats/{}".format(xuid, titleid))
    return res.json()

if __name__ == '__main__':
    main()
