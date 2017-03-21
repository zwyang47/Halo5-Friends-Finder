import requests
import json
import time

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


    #All Halo Api Calls (JSON returned)

    #print_csr_inserts()
    
    #print_season_inserts()
    
    #print_playlist_inserts()
    
    print_playlist_stats()
    
    #print_warzone_stats()


def print_warzone_stats():
    names = open('haloDump.txt', 'r').read()
    nameList = names.split('\n') 

    ids = open('haloXUID.txt', 'r').read()
    idsList = ids.split('\n') 

    fWarzone = open('insertWarzone.sql', 'a')
 
    haloList = dict(zip(nameList, idsList))
    print len(haloList)
    counter = 0 
    for key, value in haloList.iteritems():
        if len(value) > 2: 
            counter += 1
            print counter
            time.sleep(2)
            #print key
            #print value
            response = get_warzone_player_stats(key) 
            #print json.dumps(response, indent=4)
            results = response['Results']
            result = results[0]
            lowerResult = result['Result']
            playlist = lowerResult['WarzoneStat']
            if playlist['TotalGamesCompleted'] > 0:
                fWarzone.write('INSERT INTO PLAYER_STATS (GamerXUID, PlaylistID, SeasonID, TotalGames, Wins, Loses, Rank, Tier)\n')
                fWarzone.write('    VALUES ({}, \'21\', \'W\', {}, {}, {}, {}, {});\n'.format(value, playlist['TotalGamesCompleted'], playlist['TotalGamesWon'], playlist['TotalGamesLost'], 0, 0))
    fWarzone.close()
    return

def print_playlist_stats():
    playDict = get_playlist_dict()
    seasonDict = {
        "2041d318-dd22-47c2-a487-2818ecf14e41":0,
        "2fcc20a0-53ff-4ffb-8f72-eebb2e419273":1,
        "b46c2095-4ca6-4f4b-a565-4702d7cfe586":2, 
        "b28521af-7c40-4fe2-8d6e-158a5c2d9c03":3,
        "654493ed-b12d-40ee-902b-db809433f158":4
        }    
    names = open('haloDump.txt', 'r').read()
    nameList = names.split('\n') 

    ids = open('haloXUID.txt', 'r').read()
    idsList = ids.split('\n') 

    fStats = open('insertPlaylistStats.sql', 'a')
 
    haloList = dict(zip(nameList, idsList))
    #haloList = {'biglew117':'2541987111112175',
    #            'BrandonPwnage':'2533274815715877' }
    print len(haloList)
    seasonCounter = 0
    for sid, svalue in seasonDict.iteritems():
        print 'Season {}'.format(seasonCounter)
        seasonCounter += 1
        counter = 0 
        for key, value in haloList.iteritems():
            if len(value) > 2: 
                counter += 1
                print counter
                time.sleep(2)
                response = get_arena_player_stats(key, sid)
                results = response['Results']
                result = results[0]
                lowerResult = result['Result']
                arenaStats = lowerResult['ArenaStats']
                arenaPlaylistStats = arenaStats['ArenaPlaylistStats']
                for playlist in arenaPlaylistStats:
                    csr = playlist['HighestCsr']
                    playlistID = playlist['PlaylistId']
                    fStats.write('INSERT INTO PLAYER_STATS (GamerXUID, PlaylistID, SeasonID, TotalGames, Wins, Loses, Rank, Tier)\n')
                    if csr is not None:
                        fStats.write('    VALUES ({}, \'{}\', {}, {}, {}, {}, {}, {});\n'.format(value, playDict[playlistID], svalue, playlist['TotalGamesCompleted'], playlist['TotalGamesWon'], playlist['TotalGamesLost'], csr['DesignationId'], csr['Tier']))
                    else:
                        fStats.write('    VALUES ({}, \'{}\', {}, {}, {}, {}, {}, {});\n'.format(value, playDict[playlistID], svalue, playlist['TotalGamesCompleted'], playlist['TotalGamesWon'], playlist['TotalGamesLost'], 0, 0))
    fStats.close()
    return

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
    counter = 10
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

def get_playlist_dict():
    playlist = {
       "7b7e892c-d9b7-4b03-bef8-c6a071df28ef":10,
       "f27a65eb-2d11-4965-aa9c-daa088fa5c9c":11,
       "f72e0ef0-7c4a-4307-af78-8e38dac3fdba":12,
       "892189e9-d712-4bdb-afa7-1ccab43fbed4":13,
       "c98949ae-60a8-43dc-85d7-0feb0b92e719":14,
       "b617e24f-71aa-432b-a8a0-a9b417a3d47e":15,
       "bdd69f49-d962-4d9a-8a7a-ca1013609347":16,
       "b6dc4d50-4c24-4b4e-8fc5-6a378eeb299d":17,
       "505f3f9e-363f-4148-918b-46c43c33fe50":18,
       "a3f93d83-d89c-4373-b311-ec482f8d236a":19,
       "e10d9bd5-9efd-4b91-bf83-2f55b183a6f5":20,
       "b50c4dc2-6c86-4d79-aa8a-23a65da292c6":21,
       "27140f92-3b4e-4bca-b43c-ab33d7bf3986":22,
       "78ba29d5-6fdf-4d2a-8e58-14baf004fd09":23,
       "0e39ead4-383b-4452-bbd4-babb7becd82e":24,
       "98c52586-04bb-4645-99ba-55c772ac6f01":25,
       "0bcf2be1-3168-4e42-9fb5-3551d7dbce77":26,
       "c00181ea-f931-41c0-aa6d-45904cb765eb":27,
       "a355df34-acd9-45c3-bc1c-e024891df5c0":28,
       "eef52f20-860c-4ec2-84df-dda8947668cb":29,
       "476afe03-3a33-4cf1-9134-7d8b8422bea3":30,
       "69b4de92-7bd4-49ea-aa93-4aeefb730a9a":31,
       "2b04d702-0996-4b8e-8402-a7fc8b888bef":32,
       "8e393993-ea0d-4513-860e-a5acb0fe9234":33,
       "b8d651a5-087e-4990-b209-d335b6c7a05a":34,
       "9c4f9280-0054-44f6-a3bc-7a70ed4fda67":35,
       "e31d2f7e-7aa0-47f4-b1f8-6cea9cc70bbe":36,
       "0625fb37-6c3e-4526-b413-d252128b42ac":37,
       "ea669123-09c0-4c93-bf95-bdbe74d55e3d":38,
       "2d4afa59-b046-4e4e-b918-c02687f9ca87":39,
       "35ddd45e-065e-42fc-8c25-fe765739bf12":40,
       "8d3beae9-e4e8-4c14-bbf0-475286ff9404":41,
       "62b0b398-c790-4003-87ef-b4024e96f619":42,
       "79b6f0a6-5622-4c5a-a770-634d7dcc4391":43,
       "e1aaa797-c544-426e-9a0b-66a0c86a85c7":44,
       "91233698-8234-4330-be10-05d54d1d565c":45,
       "c7ad591d-1c1e-4c11-8bc8-cf90d8638faf":46,
       "00bb0332-6edc-4dbb-95dd-cbe6d25847be":47,
       "c59a19c1-fa74-4952-ba40-b74e348813ae":48,
       "a822dde2-106c-4740-88fa-e83c8219a77e":49,
       "c506d28e-fd7c-4a45-b7d1-05e20f1d425b":50,
       "a57e68b7-6623-410f-9663-c8f9e9942210":51,
       "819eb188-1a1c-48b4-9af3-283d2447ff6f":52,
       "5728f612-3f20-4459-98bd-3478c79c4861":53,
       "88b7de19-113c-4beb-af7f-8553aeda3f4c":54,
       "7385b4a1-86bf-4aec-b9c2-411a6aa48633":55,
       "4b12472e-2a06-4235-ba58-f376be6c1b39":56,
       "d0766624-dbd7-4536-ba39-2d890a6143a9":57,
       "2323b76a-db98-4e03-aa37-e171cfbdd1a4":58,
       "bc0f8ad6-31e6-4a18-87d9-ad5a2dbc8212":59,
       "780cc101-005c-4fca-8ce7-6f36d7156ffe":60,
       "ddfb6af3-2a64-4ecd-8eda-c1ce4413b676":61,
       "fe2ad4e1-3def-46a9-a18e-9ab685aa66d4":62,
       "d21c8381-26f1-4d65-832a-ef9fa0854eb5":63,
       "355dc154-9809-4edb-8ed4-fff910c6ae9c":64,
       "0504ca3c-de41-48f3-b9c8-3aab534d69e5":65,
       "f0c9ef9a-48bd-4b24-9db3-2c76b4e23450":66,
       "da2cbc67-fb2f-43b1-9a2f-88cc5e1c4dd0":67,
       "f44a5508-e208-4c65-835d-a155e363abc8":68,
       "2e812e09-912f-458b-a659-4ccb84232c65":69,
       "b5d5a242-ffa5-4d88-a229-5031916be036":70
    }
    return playlist

if __name__ == '__main__':
    main()
