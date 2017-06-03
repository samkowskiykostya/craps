# craps
Ok, so back to craps, now when game is finally properly emulated, we can find out best winning strategy.
Emulated table (stakes coefficients):
pass -> 1
notpass -> 1
6 -> 1.25
8 -> 1.25
5 -> 1.6
9 -> 1.6
4 -> 2.2
10 -> 2.2
hard 6 -> 9
hard 10 -> 7
hard 8 -> 9
hard 4 -> 7
3 -> 15
2 -> 30
12 -> 30
11 -> 15
craps any -> 7
7 -> 4
Minimal stake on pass/notpass and number prediction is 10$, the rest minimal stakes - 1$
Basically I did bruteforce of all possible combinations of stakes with step 3$ (for min 10$) and step 1$ for min 1$. Why 3$ and not 1$? Because I don't have a few spare years for calculations. I think this step will show us the trend.
Each strategy is run during 30 games in a row, 1000 times. Then I calculate win rate and average money win (this is absolute value, meaning, how much you gain on top of initial investment)
Dices throws are emulated as random normal distribution. Should be close to real life.
I start game with 200$.
Strategy looks like following: initially we put on pass 10-22$ or 0$ and then add new stakes on second run, if game hasn't finished. Each run I put same stakes, with 2 exemptions:
1. If some stake wins - I keep betting on it, but reduce stake by 3$, until I reach minimal. Why reduce? Because it is less probable that same value will appear several times in a row. Why 3$? Well, because. 
2. If game goes more than 5 throws - I withdraw all my numbers stake except pass/notpass stake. Why? Because probability of 7 is 1/6, which means every 6th throw on average will give 7. We don't want it, so withdrawing everything.
So, who is the winner? Here are top 3:
win 157$, stakes: {'10': 20, 'hard 8': 1, 'hard 10': 1, '6': 20, 'hard 6': 1, 'hard 4': 1, '5': 20, '4': 20, 'pass': 17, '9': 20, '8': 20}, win rate: 0.77%
win 141$, stakes: {'10': 20, 'hard 8': 1, 'hard 10': 1, 'hard 6': 1, 'hard 4': 1, '5': 20, '4': 20, 'pass': 11, '9': 20}, win rate: 0.81%
win 142$, stakes: {'10': 20, 'hard 8': 1, 'hard 10': 1, 'hard 6': 1, 'hard 4': 1, '5': 20, '4': 20, '9': 20}, win rate: 0.81%
So, now we can see that strategies are similar to ones which are often played: put 1 on hards, bet on 4,5,9 and 10. Interesting that safer strategies (81% vs 77%) do not use 6 and 8 bets, though they are most probable. 
You can see that sometimes pass worth betting twice as minimal (20), sometimes - about minimal (11) or not betting at all.
81% win rate is pretty good, isn't it? and 140-150$ is about 75% of investment just in an hour or two.
Hidden gems were not found, you can't win thousands, but that's what casino is about.
Speaking of strategies search - brute force is far from perfect search approach, this is a good task for SGD. Let's see what ML will give us.
