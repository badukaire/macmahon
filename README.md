# macmahon

> Needless to say, this is a **work in progress** that has not yet reached alpha status.

Script to compute standings on team sports (football, hockey, etc) using Macmahon scores with points, SOS, SOSOS, goals (scored &amp; received).

This may be useful to know, when not all games in sport leagues have been played, which teams are performing better. It is not the same 2 wins against stronger teams than against weaker teams.

The script allows several options for computing the ratings:

- bye treatment: the byes can be treated as a LOSS/NOT-PLAYED/IGNORED, DRAW (a draw is awarded) and a WIN (a win is awarded).
- sorting criteria: so far there are 3 possible options: REGULAR (ignoring MacMahon stuff), REGULARSOS (same as REGULAR but Macmahon's SOS is a tiebreaker) and WSOS (the score is the points + the weighted SOS).

The input is a file with a list of the teams and the matches results, separated by rounds. See example in section _input_. And the output is a table with the games played, points, goals (scored, received, average), SOS, SOSOS and PhSOS (points + SOS/2). See example here (sorted by the REGULAR criterium):

```
round 4 / 8  => w (weighted SOS) = 50% -- PwSOS = P + w * SOS
bye treatment: IGNORE
sorting by: REGULAR
team            G  p |  GS -  GR = avg | SOS/SOSOS | PwSOS
-------------- ------|-----------------|-----------|------
junior          4 12 |  20 -   1 =  19 |    7  122 |  12
polo            4 10 |  32 -   5 =  27 |    7  110 |  10
athc            4 10 |  18 -   2 =  16 |   10  110 |  15
valles          3  7 |   5 -   3 =   2 |   10   78 |   7
terrassa        3  4 |   7 -   5 =   2 |   22   31 |   5
egara           4  3 |   9 -  16 =  -7 |   32   41 |   3
castelldefels   3  0 |   2 -  14 = -12 |   29   27 |   4
linia22         4  0 |   4 -  27 = -23 |   39   34 |   1
iluro           3  0 |   2 -  26 = -24 |   17   61 |   0
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
  -h : help, displays this information
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
    * SOSOS : SOSOS/SOS, points
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
round 4 / 8  => w (weighted SOS) = 50% -- PwSOS = P + w * SOS
bye treatment: IGNORE
sorting by: REGULARSOS
team            G  p |  GS -  GR = avg | SOS/SOSOS | PwSOS
-------------- ------|-----------------|-----------|------
junior          4 12 |  20 -   1 =  19 |    7  122 |  12
athc            4 10 |  18 -   2 =  16 |   10  110 |  15
polo            4 10 |  32 -   5 =  27 |    7  110 |  10
valles          3  7 |   5 -   3 =   2 |   10   78 |   7
terrassa        3  4 |   7 -   5 =   2 |   22   31 |   5
egara           4  3 |   9 -  16 =  -7 |   32   41 |   3
linia22         4  0 |   4 -  27 = -23 |   39   34 |   1
castelldefels   3  0 |   2 -  14 = -12 |   29   27 |   4
iluro           3  0 |   2 -  26 = -24 |   17   61 |   0
```
This changes something, but not much: Only 2 pairs of teams which were tied by points get their standings reverted. Which makes sense since you would score more goals to a weaker team. In other words, teams who score more is because have played against weaker teams.

And now, this command sorts by _points + SOS/2_ (option `-b WSOS`):

```bash
python p.py -f ..\testData\test1.txt -d TABLE -s WSOS -b IGNORE
```
Which yields the following table, where it can be seen that many things have changed:
```
round 4 / 8  => w (weighted SOS) = 50% -- PwSOS = P + w * SOS
bye treatment: IGNORE
sorting by: WSOS
team            G  p |  GS -  GR = avg | SOS/SOSOS | PwSOS
-------------- ------|-----------------|-----------|------
athc            4 10 |  18 -   2 =  16 |   10  110 |  15
junior          4 12 |  20 -   1 =  19 |    7  122 |  12
polo            4 10 |  32 -   5 =  27 |    7  110 |  10
valles          3  7 |   5 -   3 =   2 |   10   78 |   7
terrassa        3  4 |   7 -   5 =   2 |   22   31 |   5
castelldefels   3  0 |   2 -  14 = -12 |   29   27 |   4
egara           4  3 |   9 -  16 =  -7 |   32   41 |   3
linia22         4  0 |   4 -  27 = -23 |   39   34 |   1
iluro           3  0 |   2 -  26 = -24 |   17   61 |   0
```
It can be seen that amongst other things, the team was 2nd in the first table, has gone down to the 3rd place, and the team that was 3rd is now 1st.


# input format

The input consists on a (DOS-fileformat) file that is divided into 3 sections: teams declaration, settings, and rounds. Team declaration section is always done at the beginning. The settings section is optional and if exists should be between the teams and before any round. It is declared by the `:settings` tag. Rounds come afterwards and each one starts with the `:round` tag.

Lines starting with `#` are considered comments. Actually everything after a `#` is considered a comment.

## team declaration section

The teams section at the beginning simply consists on the declaration of the list of teams. In case the league has an odd number of participants and includes a BYE team/player, such a BYE player **should not** be declared.

Team names by now must be formed only by a word. In the future perhaps it will be allowed to use longer names, or to use aliases.


## settings section

After the team declaration it is posssible to set some settings. This is not yet implemented but it would include stuff such as the bye treatment and the sorting criterium. These options would be overridden by the command line options, their only use would be to deploy self contained files for users who do not want to use the command line.

## rounds sections

Then come the rounds, each one starting with the `:round` tag. The round number is never declared, it is calculated implicitly.

In these rounds there are the matches. Each match consist

## match formats

In order to facilitate copying and pasting from web sites, the matches can be entered in a number of different formats. These formats are as follows:

- team1 1 - 0 team2
- team1 1 - team2 0
- team1 vs team2 : 1 - 0 : not yet implemented
- team1 - team2 : 1 - 0  : not yet implemented

Therefore, the team name in 1 word, and the result can be in several orders.

