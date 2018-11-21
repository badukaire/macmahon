# macmahon

> Needless to say, this is a **work in progress** that has not yet reached alpha status.

Script to compute standings on team sports (football, hockey, etc) using Macmahon scores with points, SOS, SOSOS, goals (scored &amp; received).

This may be useful to know, when not all games in sport leagues have been played, which teams are performing better. It is not the same 2 wins against stronger teams than against weaker teams.

The script allows several options for computing the ratings:

- bye treatment: the byes can be treated as a LOSS/NOT-PLAYED/IGNORED, DRAW (a draw is awarded) and a WIN (a win is awarded).
- sorting criteria: so far there are 3 possible options: REGULAR (ignoring MacMahon stuff), REGULARSOS (same as REGULAR but Macmahon's SOS is a tiebreaker) and WSOS (the score is the points + the weighted SOS).

The input is a file with a list of the teams and the matches results, separated by rounds. See example in section _input_. And the output is a table with the games played, points, goals (scored, received, average), SOS, SOSOS and PhSOS (points + SOS/2). See example here (sorted by the REGULAR criterium):

```
round 4 / 16  => w (weighted SOS) = 75% -- PwSOS = P + w * SOS
bye treatment: IGNORE
sorting by: REGULAR
teams           G  p |  GS -  GR = Gavg | SOS/SOSOS | PwSOS
-------------- ------|------------------|-----------|------
junior          4 12 |  20 -   1 =  19  |   14   37 |  19
polo            4 10 |  32 -   5 =  27  |    3   20 |  11
athc            4 10 |  18 -   2 =  16  |   15   31 |  17
valles          3  7 |   5 -   3 =   2  |   10   23 |  12
terrassa        3  4 |   7 -   5 =   2  |   21   32 |  14
egara           4  3 |   9 -  16 =  -7  |   16   31 |  11
castelldefels   3  0 |   2 -  14 = -12  |    5    6 |   2
linia22         4  0 |   4 -  27 = -23  |   12   19 |   6
iluro           3  0 |   2 -  26 = -24  |   17   16 |   8
```

## concepts

The MacMahon scoring system was invented by Lee MacMahon for improving the quality of standings in go tournaments where it was not possible to play a full round-robin tournament. For that, it used the players rank as a base for the score, and also concepts such as SOS, SOSOS and SOSOS as tiebreakers.

In competitions where a league is played, at the end these scores are not useful, but in the early rounds it can be useful to know which teams have lower or greater potential. This is achieved by considering the SOS.

The SOS (Sum of Opponents Scores) is the sum of points of all the opponents a team (or player) has played.

A example is useful to understand it and how it is useful: If in round 2 of a league there is a team A with (4 points) has played against team B (with 2 points) and team C (with 5 points), team A's SOS will be 2 + 5 = 7. Then if there is a team F (also with 4 points as team A) which has played against team G (with 1 point) and team H (with 0 points), its SOS will be 1 + 0 = 1.

In this example, both teams A and F have 4 points. This means they both probably have 1 win and 1 draw. But it is quite obvious that team A's 4 points are more valuable that team F's 4 points, because these points have been achieved against stronger teams.

Another possibility is that team F has a better goal average than team A, because it has played against weaker teams. The SOS is in during earlier rounds a better indicator than the goal average of a team potential. At the end of the league, since all the teams will have the same SOS (all have played against each other), and then the goal average is a good tiebreaker.

The SOSOS is the sum of SOS of all the opponents of a given team. It is useful in case 2 teams have the same SOS. The SODOS is another tiebreaker that may be useful here only if the number of rounds is very small. It is the Sum of SOS of all the defeated opponents.

Finally this program includes a new concept: the PwSOS, or points + weighted SOS. It consists of the points plus the SOS, weighted by the number or remaining rounds. This means that in the first rounds it has a higher weight, and it is not considered in the last round. Actually, as it has already been said, in the last round all teams have the same SOS, therefore it makes no sense to consider it.


# options

The script accepts several command line options. Copying from the script:

```
  -f <file> : files to read (by now just reading a file)
  -o <output file> : output file where the final table is sent
  -O : same as -o but the name is assigned automatically based on the options given
  -d <display> : display format: TABLE, TABLE_POS, SET, SET_GOALSFIRST
  -b <bye score> : bye score : IGNORE (reject game), DRAW (0-0), WIN (0-0)
  -s <sort> : sort by one of (commas indicate tiebreakers):
    * REGULAR : points, goal avg
    * REGULARSOS : points, SOS, SOSOS
    * WSOS : weighted SOS = points + SOS/remaining rounds, points
    * SOS : SOS/SOSOS, points
  -r <rounds> : number of league rounds - if not set it's assumed equal as the number of declared
                rounds, and WSOS does not matter (weights 0.00% in the last round)
  -c <round #> : count up to round #
```


## examples

The table above was generated with the following command, that sort with the regular way (points / goal average) and treats byes as losses (does not count them):
```bash
python p.py -f ..\testData\test1.txt -d TABLE -s REGULAR -b IGNORE
```
With the following command, the table is now sorted with points and the tiebreaker is the SOS score (option `-b REGULARSOS`):
```bash
python p.py -f ..\testData\test1.txt -d TABLE -s REGULARSOS -b IGNORE
```
Which yields the following table:
```
bye treatment: IGNORE
sorting by: REGULARSOS
teams           G  p |  GS -  GR = Gavg | SOS/SOSOS | PwSOS
-------------- ------|------------------|-----------|------
junior          4 12 |  20 -   1 =  19  |   14   37 |  19
athc            4 10 |  18 -   2 =  16  |   15   31 |  17
polo            4 10 |  32 -   5 =  27  |    3   20 |  11
valles          3  7 |   5 -   3 =   2  |   10   23 |  12
terrassa        3  4 |   7 -   5 =   2  |   21   32 |  14
egara           4  3 |   9 -  16 =  -7  |   16   31 |  11
iluro           3  0 |   2 -  26 = -24  |   17   16 |   8
linia22         4  0 |   4 -  27 = -23  |   12   19 |   6
castelldefels   3  0 |   2 -  14 = -12  |    5    6 |   2
```
This changes something, but not much: Only 2 pairs of teams which were tied by points get their standings reverted. Which makes sense since you would score more goals to a weaker team. In other words, teams who score more is because have played against weaker teams.

And now, this command sorts by _points + SOS/2_ (option `-b WSOS`):

```bash
python p.py -f ..\testData\test1.txt -d TABLE -s WSOS -b IGNORE
```
Which yields the following table, where it can be seen that many things have changed:
```
bye treatment: IGNORE
sorting by: WSOS
teams           G  p |  GS -  GR = Gavg | SOS/SOSOS | PwSOS
-------------- ------|------------------|-----------|------
junior          4 12 |  20 -   1 =  19  |   14   37 |  19
athc            4 10 |  18 -   2 =  16  |   15   31 |  17
terrassa        3  4 |   7 -   5 =   2  |   21   32 |  14
valles          3  7 |   5 -   3 =   2  |   10   23 |  12
polo            4 10 |  32 -   5 =  27  |    3   20 |  11
egara           4  3 |   9 -  16 =  -7  |   16   31 |  11
iluro           3  0 |   2 -  26 = -24  |   17   16 |   8
linia22         4  0 |   4 -  27 = -23  |   12   19 |   6
castelldefels   3  0 |   2 -  14 = -12  |    5    6 |   2
```
It can be seen that amongst other things, the team that was 2nd in the first table, has gone down to the 5th place, and the team that was 5th is now 3rd.

# input format

The input consists on a (DOS-format) file that is divided into 3 sections: teams declaration, settings, and rounds. Team declaration section is always done at the beginning. The settings section is optional and if exists should be between the teams and before any round. It is declared by the `:settings` tag. Rounds come afterwards and each one starts with the `:round` tag. The round number is never declared, it is calculated implicitly.

Lines starting with `#` are considered comments. Actually everything after a `#` is considered a comment.

TODO describe input
