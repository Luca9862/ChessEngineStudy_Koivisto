from pgn_manager import _readPGN

def game_count(pgn, number_plycount):
    count = 0
    games = _readPGN(pgn)
    for game in games:
        result = game.headers.get("Result")
        playCount = game.headers.get("PlayCount")
        if result == '0-1':
            if(int(playCount) >= number_plycount and int(playCount) <= 400):
                count += 1
                print(game)
        print(count)

def main(pgn):
    tot = 0
    twenty_five = 0
    fifty = 0
    one_hundred = 0
    one_hundred_and_fifty = 0
    two_hundred = 0
    two_hundred_fifty = 0
    three_hundred = 0
    three_hundred_and_fifty = 0
    four_hundred = 0
    games = _readPGN(pgn)
    for game in games:
        moves_number = game.headers.get("PlayCount")
        tot += int(moves_number)

        if int(moves_number) >= 25:
            twenty_five += 1 
        if int(moves_number) >=50:
            fifty += 1 
        if int(moves_number) >= 100:
            one_hundred+=1
        if int(moves_number) >= 150:
            one_hundred_and_fifty +=1
        if int(moves_number) >= 200:
            two_hundred += 1 
        if int(moves_number) >= 250:
            two_hundred_fifty += 1
        if int(moves_number) >= 300:
            three_hundred += 1
        if int(moves_number) >= 350:
            three_hundred_and_fifty += 1
        if int(moves_number) >= 400:
            four_hundred += 1
        

    average = int(tot/len(games))
    print(pgn)
    print('La media delle mosse è: ' + str(average))
    print('Le partite con almeno 25 mosse sono: ' + str(twenty_five))
    print('Le partite con almeno 50 mosse sono: ' + str(fifty))
    print('Le partite con almeno 100 mosse sono: ' + str(one_hundred))
    print('Le partite con almeno 150 mosse sono: ' + str(one_hundred_and_fifty))
    print('Le partite con almeno 200 mosse sono: ' + str(two_hundred))
    print('Le partite con almeno 250 mosse sono: ' + str(two_hundred_fifty))
    print('Le partite con almeno 300 mosse sono: ' + str(three_hundred))
    print('Le partite con almeno 350 mosse sono: ' + str(three_hundred_and_fifty))
    print('Le partite con almeno 400 mosse sono: ' + str(four_hundred))

    with open('playcount_analyzer_output.txt', 'w') as f:
        f.write('PlayCount average: ' + str(average) + '\n')
        f.write('>=25: ' + str(twenty_five) + '\n')
        f.write('>=50: ' + str(fifty) + '\n')
        f.write('>=100 ' + str(one_hundred) + '\n')
        f.write('>=150: ' + str(one_hundred_and_fifty) + '\n')
        f.write('>=200: ' + str(two_hundred) + '\n')
        f.write('>=250: ' + str(two_hundred_fifty) + '\n')
        f.write('>=300: ' + str(three_hundred) + '\n')
        f.write('>=350: ' + str(three_hundred_and_fifty) + '\n')
        f.write('>=400: ' + str(four_hundred) + '\n')


#main(r'/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_lc0/1sec/Koivisto_lc0_1_fix.pgn')
game_count(r'C:\Users\canal\Documents\GitHub\tirocinio_lucacanali\dataset\game_script_eros\koiv_berserk\0,1sec\Koivisto_Berserk_0.1_fix.pgn', 350)
