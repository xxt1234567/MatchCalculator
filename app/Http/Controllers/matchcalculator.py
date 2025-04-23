import numpy as np
import copy
import sys
import json
import traceback
import random

def getmark(x, y):
    if(x == 0):
        return 0
    if(x == 1):
        if(y == 1):
            return 0
        else:
            return 1
    if(x == 2):
        return x + y
    if(x == 3):
        if(y == -1):
            return 0
        else:
            return 3

def scoretorank(scoreboard, matchleft, matchleftcnt, teamcnt, teamindex, bo_win, double, wscore, lscore, dscore):
    rank = []
    for i in range(teamcnt):
        rank.append([teamindex[i], [0, 0, 0], 0, 0, 2, 0, 0])#[序号，胜-平-负，积分，净胜分，?/<=/=/>=，总得分，=/>=]
    for i in range(teamcnt):
        for j in range(i + 1, teamcnt):
            for k in range(double):
                flag = False
                if ([teamindex[i], teamindex[j], k] in matchleft):
                    if(matchleftcnt != 0):
                        continue
                    else:
                        flag = True
                if ((bo_win == 0 and scoreboard[i][j][k] > scoreboard[j][i][k]) or (bo_win != 0 and scoreboard[i][j][k] == bo_win)):
                    rank[i][1][0] += 1
                    rank[j][1][2] += 1
                    rank[i][2] += wscore
                    rank[j][2] += lscore
                    if(flag and bo_win == 0):
                        rank[i][4] = getmark(rank[i][4], 1)
                        rank[j][4] = getmark(rank[j][4], -1)
                        rank[i][6] = 1
                        rank[j][6] = 1
                elif ((bo_win == 0 and scoreboard[i][j][k] < scoreboard[j][i][k]) or (bo_win != 0 and scoreboard[j][i][k] == bo_win)):
                    rank[i][1][2] += 1
                    rank[j][1][0] += 1
                    rank[j][2] += wscore
                    rank[i][2] += lscore
                    if(flag and bo_win == 0):
                        rank[i][4] = getmark(rank[i][4], -1)
                        rank[j][4] = getmark(rank[j][4], 1)
                        rank[i][6] = 1
                        rank[j][6] = 1
                else:
                    rank[i][1][1] += 1
                    rank[j][1][1] += 1
                    rank[i][2] += dscore
                    rank[j][2] += dscore
                    if(flag and bo_win == 0):
                        rank[i][4] = getmark(rank[i][4], 0)
                        rank[j][4] = getmark(rank[j][4], 0)
                        rank[i][6] = 1
                        rank[j][6] = 1
                rank[i][3] += scoreboard[i][j][k] - scoreboard[j][i][k]
                rank[j][3] += scoreboard[j][i][k] - scoreboard[i][j][k]
                rank[i][5] += scoreboard[i][j][k]
                rank[j][5] += scoreboard[j][i][k]
    return rank

def subscoreboard(scoreboard, teamcnt, teamindex, double):
    subboard = np.zeros((teamcnt, teamcnt, double), int)
    for i in range(teamcnt):
        for j in range(teamcnt):
            for k in range(double):
                subboard[i][j][k] = scoreboard[teamindex[i]][teamindex[j]][k]
    return subboard

def ranksortcmp(a, b, bo_win):
    if(bo_win == 0):
        if (a[2] != b[2]):
            return a[2] > b[2]
        elif (a[3] != b[3]):
            return a[3] > b[3]
        elif (a[5] != b[5]):
            return a[5] > b[5]
        else:
            return a[0] < b[0]
    else:
        if (a[1][0] != b[1][0]):
            return a[1][0] > b[1][0]
        elif (a[3] != b[3]):
            return a[3] > b[3]
        else:
            return a[0] < b[0]
    
def ranksort(rank, subrank, left, teamcnt, bo_win):
    for i in range(1, teamcnt):
        temp1 = subrank[i]
        temp2 = rank[left + i]
        j = i - 1
        while (j >= 0 and ranksortcmp(temp1, subrank[j], bo_win)):
            subrank[j + 1] = subrank[j]
            rank[left + j + 1] = rank[left + j]
            j = j - 1
        subrank[j + 1] = temp1
        rank[left + j + 1] = temp2

def issame(a, b, bo_win):
    if (bo_win != 0):
        return (a[1][0] == b[1][0] and a[3] == b[3])
    else:
        return (a[2] == b[2] and a[3] == b[3] and a[5] == b[5])

def teamsort(scoreboard, rank, left, teamcnt, matchleft, matchleftcnt, bo_win, double, wscore, lscore, dscore, additeam, addirank):
    if (teamcnt == 1):
        return
    teamindex = []
    rankindex = []
    for i in range(left, left + teamcnt):
        teamindex.append(rank[i][0])
        rankindex.append(i)
    subboard = subscoreboard(scoreboard, teamcnt, teamindex, double)
    subrank = scoretorank(subboard, matchleft, matchleftcnt, teamcnt, teamindex, bo_win, double, wscore, lscore, dscore)
    ranksort(rank, subrank, left, teamcnt, bo_win)
    i = 0
    while(i < teamcnt):
        j = i + 1
        cnt = 1
        while (j < teamcnt and issame(subrank[i], subrank[j], bo_win)):
            j += 1
            cnt += 1
        if (cnt == teamcnt):
            if(matchleftcnt == 0):
                additeam.append(teamindex)
                addirank.append(rankindex)
            return
        teamsort(scoreboard, rank, left + i, cnt, matchleft, matchleftcnt, bo_win, double, wscore, lscore, dscore, additeam, addirank)
        i = j

def bo0_addi(rank, teamcnt, matchleftcnt, additeam, addirank):
    if (matchleftcnt == 0):
        i = 0
        while(i < teamcnt):
            j = i + 1
            cnt = 1
            teamindex = [rank[i][0]]
            rankindex = [i]
            while (j < teamcnt and rank[i][2] == rank[j][2]):
                teamindex.append(rank[j][0])
                rankindex.append(j)
                j += 1
                cnt += 1
            if (cnt > 1):
                additeam.append(teamindex)
                addirank.append(rankindex)
            i = j

def calccurrent(scoreboard, matchleft, matchleftcnt, teamcnt, bo_win, double, wscore, lscore, dscore):
    teamindex = []
    for i in range(teamcnt):
        teamindex.append(i)
    currentrank = scoretorank(scoreboard, matchleft, matchleftcnt, teamcnt, teamindex, bo_win, double, wscore, lscore, dscore)
    additeam = []
    addirank = []
    teamsort(scoreboard, currentrank, 0, teamcnt, matchleft, matchleftcnt, bo_win, double, wscore, lscore, dscore, additeam, addirank)
    if (bo_win == 0):
        additeam = []
        addirank = []
        bo0_addi(currentrank, teamcnt, matchleftcnt, additeam, addirank)
    outcurrentrank = outputrank(currentrank, teamcnt, bo_win)
    print(json.dumps(outcurrentrank))
    print(json.dumps(additeam))

def outputrank(rank, teamcnt, bo_win):
    outrank = copy.deepcopy(rank)
    for i in range(teamcnt):
        if (bo_win == 0):
            outrank[i][1] = str(rank[i][1][0]) + '-' + str(rank[i][1][1]) + '-' + str(rank[i][1][2])
            if (rank[i][4] == 0):
                outrank[i][3] = '?'
            elif (rank[i][4] == 1):
                outrank[i][3] = '<=' + str(rank[i][3])
            elif (rank[i][4] == 2):
                outrank[i][3] = str(rank[i][3])
            else:
                outrank[i][3] = '>=' + str(rank[i][3])
            if (rank[i][6] == 0):
                outrank[i][5] = str(rank[i][5])
            else:
                outrank[i][5] = '>=' + str(rank[i][5])
        else:
            outrank[i][1] = str(rank[i][1][0]) + '-' + str(rank[i][1][2])
    return outrank

def indtrans(ind, cnt, bo_):
    res = [0] * cnt
    i = cnt - 1
    while (ind > 0):
        res[i] = ind % bo_
        ind = ind // bo_
        i = i - 1
    return res
    
def calcfinal(scoreboard, matchleft, matchleftcnt, teamcnt, bo, bo_win, double, wscore, lscore, dscore, tags, mkflag):
    if (bo == -1):
        bo_ = 3
        possiblescore = [[1, 0], [0, 0], [0, 1]]
    else:
        bo_ = bo + 1
        possiblescore = [0] * bo_
        for i in range(bo_win):
            possiblescore[i] = [bo_win, i]
            possiblescore[bo - i] = [i, bo_win]
    maxind = bo_ ** matchleftcnt
    mkmaxind = 70000 if mkflag else maxind
    possibleranks = []
    simplifiedranks = []
    selectaddmatchs = []
    selectteamranks = []
    ranknum = []
    selectaddnum = []
    selectteamnum = []
    rankpossibilities = np.zeros((teamcnt, teamcnt + 1))
    topposs = np.zeros(teamcnt)
    botposs = np.zeros(teamcnt)
    possaftermatch = np.zeros((bo_, teamcnt, teamcnt + 1))
    toppossaftermatch = np.zeros((teamcnt, teamcnt))
    botpossaftermatch = np.zeros((teamcnt, teamcnt))
    teamindex = []
    for i in range(teamcnt):
        teamindex.append(i)
    
    for i in range(mkmaxind):
        possiblescoreboard = scoreboard
        if (mkflag):
            x = random.randint(0, maxind)
            scoreind = indtrans(x, matchleftcnt, bo_)
        else:
            scoreind = indtrans(i, matchleftcnt, bo_)
        resname = []
        for j in range(matchleftcnt):
            possiblescoreboard[matchleft[j][0]][matchleft[j][1]][matchleft[j][2]] = possiblescore[scoreind[j]][0]
            possiblescoreboard[matchleft[j][1]][matchleft[j][0]][matchleft[j][2]] = possiblescore[scoreind[j]][1]
            resname.append([matchleft[j][0], possiblescore[scoreind[j]][0], possiblescore[scoreind[j]][1], matchleft[j][1]])
                
            if (tags['possaftermatchtag'] and
               ((matchleft[j][0] == tags['nextmatchteam1'] and matchleft[j][1] == tags['nextmatchteam2']) or
                (matchleft[j][0] == tags['nextmatchteam2'] and matchleft[j][1] == tags['nextmatchteam1']))):
                if (matchleft[j][0] == tags['nextmatchteam1']):
                    possaftermatchind = scoreind[j]
                else:
                    possaftermatchind = bo - scoreind[j]           
        possiblerank = scoretorank(possiblescoreboard, matchleft, 0, teamcnt, teamindex, bo_win, double, wscore, lscore, dscore)
        additeam = []
        addirank = []
        teamsort(possiblescoreboard, possiblerank, 0, teamcnt, matchleft, 0, bo_win, double, wscore, lscore, dscore, additeam, addirank)
        if (bo_win == 0):
            additeam = []
            addirank = []
            bo0_addi(possiblerank, teamcnt, 0, additeam, addirank)
        outpossiblerank = outputrank(possiblerank, teamcnt, bo_win)
            
        simplifiedrank = []
        for j in range(teamcnt):
            simplifiedrank.append(possiblerank[j][0])    
            rankpossibilities[possiblerank[j][0]][j] += 1
            if (j < tags['toprank']):
                topposs[possiblerank[j][0]] += 1
            if (j >= tags['botrank'] - 1):
                botposs[possiblerank[j][0]] += 1
                
            if tags['possaftermatchtag']:    
                possaftermatch[possaftermatchind][possiblerank[j][0]][j] += 1
                if (j < tags['toprank']):
                    toppossaftermatch[possaftermatchind][possiblerank[j][0]] += 1
                if (j >= tags['botrank'] - 1):
                    botpossaftermatch[possaftermatchind][possiblerank[j][0]] += 1 

        simplifiedrank.append([])
        if (matchleftcnt <= 3):
            ranknum.append(resname)
            possibleranks.append(outpossiblerank)
            possibleranks[i].append([])
        
        selectteamflag = False
        if (len(additeam) > 0):
            addistr = []
            selectteamaddflag = True
            for j in range(len(additeam)):
                addistr.append([])
                for k in range(len(additeam[j])):
                    addistr[j].append(additeam[j][k])
                    r = 0
                    while (additeam[j][k] != possiblerank[r][0]):
                        r = r + 1
                    top = 0
                    bot = 0
                    for l in range(len(additeam[j])):
                        if(addirank[j][l] < tags['toprank']):
                            top += 1
                        if(addirank[j][l] >= tags['botrank'] - 1):
                            bot += 1    
                    rankpossibilities[additeam[j][k]][teamcnt] += 1
                    rankpossibilities[additeam[j][k]][r] -= 1
                    if (r < tags['toprank']):
                        topposs[additeam[j][k]] -= 1
                    if (r >= tags['botrank'] - 1):
                        botposs[additeam[j][k]] -= 1
                    topposs[additeam[j][k]] += top / len(additeam[j])
                    botposs[additeam[j][k]] += bot / len(additeam[j])
                    
                    if tags['possaftermatchtag']:
                        possaftermatch[possaftermatchind][additeam[j][k]][teamcnt] += 1
                        possaftermatch[possaftermatchind][additeam[j][k]][r] -= 1
                        if (r < tags['toprank']):
                            toppossaftermatch[possaftermatchind][additeam[j][k]] -= 1
                        if (r >= tags['botrank'] - 1):
                            botpossaftermatch[possaftermatchind][additeam[j][k]] -= 1
                        toppossaftermatch[possaftermatchind][additeam[j][k]] += top / len(additeam[j])
                        botpossaftermatch[possaftermatchind][additeam[j][k]] += bot / len(additeam[j])
                        
                    if (tags['selectteamtag'] and additeam[j][k] == tags['selectteamname'] and
                        addirank[j][0] + 1 <= tags['selectteamrank2'] and
                        addirank[j][len(additeam[j]) - 1] + 1 >= tags['selectteamrank1']):
                        selectteamflag = True
                        selectteamaddflag = False

                    
            simplifiedrank[teamcnt] = addistr
            if (matchleftcnt <= 3):
                possibleranks[i][teamcnt] = addistr
            if tags['selectaddtag']:
                selectaddmatchs.append(simplifiedrank)
                selectaddnum.append(resname)
            if (tags['selectteamtag'] and selectteamaddflag):
                j = 0
                while (possiblerank[j][0] != tags['selectteamname']):
                    j += 1
                if (j + 1 >= tags['selectteamrank1'] and j + 1 <= tags['selectteamrank2']):
                    selectteamflag = True
                    
        elif tags['selectteamtag']:
            j = 0
            while (possiblerank[j][0] != tags['selectteamname']):
                j += 1
            if (j + 1 >= tags['selectteamrank1'] and j + 1 <= tags['selectteamrank2']):
                selectteamflag = True
                
        if selectteamflag:
            selectteamranks.append(simplifiedrank)
            selectteamnum.append(resname)

        if (matchleftcnt <= 3):
            simplifiedranks.append(simplifiedrank)
            
    rankpossibilities = rankpossibilities / mkmaxind
    topposs = topposs / mkmaxind
    botposs = botposs / mkmaxind
    rankpossoutput = []
    for i in range(teamcnt):
        rankpossoutput.append([])
        for j in range(teamcnt + 1):
            rankpossstr = int(rankpossibilities[i][j] * 1000000 + 0.5) / 10000
            rankpossoutput[i].append(rankpossstr)
        if tags['showtoptag']:
            rankpossstr = int(topposs[i] * 1000000 + 0.5) / 10000
            rankpossoutput[i].append(rankpossstr)
        if tags['showbottag']:
            rankpossstr = int(botposs[i] * 1000000 + 0.5) / 10000
            rankpossoutput[i].append(rankpossstr)
            
    if tags['possaftermatchtag']:
        possaftermatch = possaftermatch / mkmaxind * bo_
        toppossaftermatch = toppossaftermatch / mkmaxind * bo_
        botpossaftermatch = botpossaftermatch / mkmaxind * bo_
        possaftermatchoutput = []
        for k in range(bo_):
            possaftermatchoutput.append([])
            for i in range(teamcnt):
                possaftermatchoutput[k].append([])
                for j in range(teamcnt + 1):
                    rankpossstr = int(possaftermatch[k][i][j] * 1000000 + 0.5) / 10000
                    possaftermatchoutput[k][i].append(rankpossstr)
                if tags['showtoptag']:
                    rankpossstr = int(toppossaftermatch[k][i] * 1000000 + 0.5) / 10000
                    possaftermatchoutput[k][i].append(rankpossstr)
                if tags['showbottag']:
                    rankpossstr = int(botpossaftermatch[k][i] * 1000000 + 0.5) / 10000
                    possaftermatchoutput[k][i].append(rankpossstr)

    print(json.dumps(rankpossoutput))                   
    if (matchleftcnt <= 3):
        print(json.dumps(ranknum))
        print(json.dumps(possibleranks))
        print(json.dumps(simplifiedranks))
    else:
        print([])
        print([])
        print([])
    if tags['selectaddtag']:
        print(json.dumps(selectaddnum))
        print(json.dumps(selectaddmatchs))
    else:
        print([])
        print([])
    if tags['selectteamtag']:
        print(json.dumps(selectteamnum))
        print(json.dumps(selectteamranks))
    else:
        print([])
        print([])
    for i in range(bo_):
        if tags['possaftermatchtag']:
            print(json.dumps(possaftermatchoutput[i]))
        else:
            print([])
            
def main():
    scoreboard = json.loads(sys.argv[1])
    matchleft = json.loads(sys.argv[2])
    matchleftcnt = int(sys.argv[3])
    teamcnt = int(sys.argv[4])
    bo = int(sys.argv[5])
    bo_win = (bo + 1) // 2
    double = int(sys.argv[6])
    wscore = int(sys.argv[7])
    lscore = int(sys.argv[8])
    dscore = int(sys.argv[9])
    tags = {}
    tags['showtoptag'] = int(sys.argv[10])
    tags['showbottag'] = int(sys.argv[11])
    tags['toprank'] = int(sys.argv[12])
    tags['botrank'] = int(sys.argv[13])
    tags['selectaddtag'] = int(sys.argv[14])
    tags['selectteamtag'] = int(sys.argv[15])
    tags['possaftermatchtag'] = int(sys.argv[16])
    tags['selectteamname'] = int(sys.argv[17])
    tags['selectteamrank1'] = int(sys.argv[18])
    tags['selectteamrank2'] = int(sys.argv[19])
    tags['nextmatchteam1'] = int(sys.argv[20])
    tags['nextmatchteam2'] = int(sys.argv[21])
    mostml = int(sys.argv[22])
    if matchleft is None:
        matchleft = []
    calccurrent(scoreboard, matchleft, matchleftcnt, teamcnt, bo_win, double, wscore, lscore, dscore)
    if (matchleftcnt > 0):
        calcfinal(scoreboard, matchleft, matchleftcnt, teamcnt, bo, bo_win, double, wscore, lscore, dscore, tags, matchleftcnt > mostml)
    else:
        for i in range(9 + bo):
            print([])
    
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        error_info = {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }
        print(json.dumps(error_info))
        sys.exit(1)
