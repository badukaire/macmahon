import sys
from difflib import SequenceMatcher

def teamProperName( sTeam, pListTeams ) :
  lsBest = ""
  lfBestScore = 0.0
  for lsTeam in pListTeams :
    lfRatio = SequenceMatcher( None, sTeam, lsTeam ).ratio()
    #print( lsTeam, lfRatio )
    if lfRatio > lfBestScore :
      lsBest = lsTeam
      lfBestScore = lfRatio
  #print( "BEST:%s: (%f)" % ( lsBest, lfRatio ) )
  return lsBest


lListTeams = []
if len( sys.argv ) > 1 :
  lsTeams = sys.argv[ 1 ]
  liLenLongName = 0
  try :
    lFile = open( lsTeams )
    for line in lFile :
      lsTeam = line.split()[0]
      lListTeams.append( lsTeam )
      if len( lsTeam ) > liLenLongName :
         liLenLongName = len( lsTeam )
      #print( lsTeam )
    lFile.close()
  except :
    print( "cant open team names file %s" % lsTeams )

if len( lListTeams ) == 0 :
  print( "no valid list of teams read" )
else :
  print( lListTeams )

for line in sys.stdin :
  lss = line.split()
  #print lss
  iSplit = -1
  size = len( lss )
  for i, tok in enumerate( lss ) :
    if tok == '-' :
      iSplit = i
      if iSplit < 2 or iSplit > size - 2 :
         #print "this line has '-' in an invalid place, iSplit = %d" % iSplit
         iSplit = -1
         break; # not enough tokens
      lssTeam1 = lss[ : iSplit - 1 ]
      lssTeam2 = lss[ iSplit + 2 : ]
      lsScore1 = lss[ iSplit - 1 ]
      lsScore2 = lss[ iSplit + 1 ]
      #print( "team1:%s:, team2:%s:" % ( lssTeam1, lssTeam2 ) )
      lsTeam1 = ""
      for s in lssTeam1 : lsTeam1 += s
      lsTeam2 = ""
      for s in lssTeam2 : lsTeam2 += s
      if len( lListTeams ) == 0 :
        print( "%s %s - %s %s" % ( lsTeam1, lsScore1, lsScore2, lsTeam2 ) )
      else :
        lsTeam1proper = teamProperName( lsTeam1, lListTeams )
        lsPadding = (liLenLongName - len(lsTeam1proper)) * " "
        lsTeam2proper = teamProperName( lsTeam2, lListTeams )
        print( "%s%s %s - %s %s" % ( lsTeam1proper, lsPadding, lsScore1, lsScore2, lsTeam2proper ) )
  #print( "--" )

