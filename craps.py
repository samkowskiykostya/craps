import random, time

class Craps:
    def __init__(self, initialSum):
        self.mym = initialSum
        self.allbets = {'pass':1, 'notpass':1, '6':1.25, '8':1.25, '5':1.6, '9':1.6, '4':2.2, '10':2.2, 'h6':9, 'h10':7, 'h8':9, 'h4':7, '3':15, '2':30, '12':30, '11':15, 'cany':7, '7':4}
        self.curbets = {}
        self.historybet = {}
        self.throws = 0
        self.on = None
    def doWin(self, bet):
        if bet in self.curbets:
            self.mym += (self.allbets[bet] + 1) * self.curbets[bet]
            del self.curbets[bet]
    def doLost(self, bet):
        if bet in self.curbets:
            del self.curbets[bet]
    def bet(self, bet, m, check=True):
        if not self.on and not bet in ['pass', 'notpass'] or str(self.on) == bet:
            return
        if check and bet in self.curbets:
            return
        if self.mym >= m:
            self.curbets[bet] = m
            self.historybet[bet] = m
            self.mym -= m
    def withdrawBet(self, bet):
        if bet in self.curbets:
            self.mym += self.curbets[bet]
            del self.curbets[bet]
    def withdrawAllBets(self):
        for bet in self.allbets:
            if bet not in ['pass', 'notpass']:
                self.withdrawBet(bet)
    def cycle(self):
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        c = a + b
        self.throws += 1
        if self.on is None:
            if c in [7, 11]:
                self.doWin('pass')
                self.doLost('notpass')
                self.throws = 0
            elif c in [12, 2]:
                self.doLost('pass')
                self.throws = 0
            else:
                self.on = c
        else:
            if c == 7:
                self.doWin('notpass')
                self.curbets.clear()
                self.historybet.clear()
                self.on = None
            if c == self.on:
                self.doWin('pass')
            if 3 >= c >= 11:
                self.doWin('cany')
            self.doWin(str(c))
            if a == b:
                self.doWin('h' + str(c))
            self.doLost('h' + str(c))
            for b in ['2','3','11','12','cany']:
                self.doLost(b)
    def emulate(self, strategy, games=30):
        if strategy:
            i = 0
            while self.mym > 0 and i < games:
                strategy.strategy(self)
                self.cycle()
                if not self.on:
                    i += 1
            if i == games:
                return True, self.mym
            else:
                return False, i

class Strategy:
    def __init__(self, vals, step):
        self.values = vals
        self.step = step
    def strategy(self, craps):
        def doBet(bet, m):
            mmin = 1
            if bet in ['pass', 'notpass', '6', '8', '5', '9', '4', '10']:
                mmin = 10
            if m < mmin:
                return
            if bet in craps.historybet:
                m = craps.historybet[bet] - self.step
                m = max(mmin, m)
            craps.bet(bet, m)
        if not craps.on:
            if 'pass' in self.values:
                doBet('pass', self.values['pass'])
            if 'notpass' in self.values:
                doBet('notpass', self.values['notpass'])
        else:
            if craps.throws == 5:
                craps.withdrawAllBets()
            else:
                for k,v in self.values.iteritems():
                    if k not in ['pass', 'notpass']:
                        doBet(k, v)

random.seed(13)
N = 1000
startWith = 200

def findBestStrategies():
    earns = []
    step = 3
    # cany = 5
    for s68 in range(8, 22, step):
        for s59 in range(8, 22, step):
            for s410 in range(8, 22, step):
                for pnp in range(8, 22, step):
                    for h in range(0, 6, 1):
                        for c in range(0, 6, 1):
                            for cany in range(0, 6, 1):
                                # for c7 in range(0, 11, step):
                                vals = {'6':s68, '8':s68, '5':s59, '9':s59, '4':s410,'10':s410, 'h4':h, 'h6':h, 'h8':h, 'h10':h, 'pass':pnp, 'notpass':0, 'cany': cany, '7': 0, '2':c, '3':c, '11':c, '12':c}
                                s = Strategy(vals, step)
                                totalWin = totalWinN = 0
                                for _ in range(N):
                                    craps = Craps(startWith)
                                    win, sum = craps.emulate(s)
                                    totalWinN += win
                                    totalWin += win * sum
                                earn = (float(totalWinN) / N) * (totalWin / totalWinN - startWith)
                                earns.append([earn, {k:v for k,v in vals.iteritems() if v not in [0,8]}, float(totalWinN) / N, totalWin / totalWinN - startWith])
    earns.sort(key=lambda x: x[0], reverse=True)
    print earns[:20]

def testStrategy():
    s = Strategy({'11': 5, '12': 5, '3': 5, '2': 5, 'pass': 14})
    totalWin = totalWinN = 0
    for _ in range(N):
        craps = Craps(startWith)
        win, sum = craps.emulate(s)
        totalWinN += win
        totalWin += win * sum
    print 'Started with:', startWith, 'Won games:', float(totalWinN) / N, 'Average Earn:', totalWin / totalWinN - startWith

# testStrategy()
findBestStrategies()