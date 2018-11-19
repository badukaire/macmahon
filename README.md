# macmahon

> Needless to say, this is a **work in progress** that has not yet reached alpha status.

Script to compute standings on team sports (football, hockey, etc) using Macmahon scores with points, SOS, SOSOS, goals (scored &amp; received).

This may be useful to know, when not all games in sport leagues have been played, which teams are performing better. It is not the same 2 wins against stronger teams than against weaker teams.

The script allows several options for computing the ratings:

- bye treatment: the byes can be treated as a LOSS/NOT-PLAYED/IGNORED, DRAW (a draw is awarded) and a WIN (a win is awarded).
- sorting criteria: so far there are 3 possible options: REGULAR (ignoring MacMahon stuff), REGULARSOS (same as REGULAR but Macmahon's SOS is a tiebreaker) and HALFSOS (the score is the points + half the SOS). This last one seems to be a good method but I have no demonstration to prove that, if you know of a better way let me know.

The input is a file with a list of the teams and the matches results, separated by rounds. See example in section _input_. And the output is a table with the games played, points, goals (scored, received, average), SOS, SOSOS and PhSOS (points + SOS/2). See example here (sorted by the REGULAR criterium):

```
bye treatment: IGNORE
sorting by: REGULAR
teams           G  p |  GS -  GR = Gavg | SOS/SOSOS | PhSOS
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

# options

The script accepts several command line options

TODO describe options

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
teams           G  p |  GS -  GR = Gavg | SOS/SOSOS | PhSOS
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

And now, this command sorts by _points + SOS/2_ (option `-b HALFSOS`):

```bash
python p.py -f ..\testData\test1.txt -d TABLE -s HALFSOS -b IGNORE
```
Which yields the following table, where it can be seen that many things have changed:
```
bye treatment: IGNORE
sorting by: HALFSOS
teams           G  p |  GS -  GR = Gavg | SOS/SOSOS | PhSOS
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
