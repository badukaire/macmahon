#: processes a set of teams, settings and rounds and displays the standings according
#: to the settings
#:
#: usage: python p.py [<options>] <file>
#: options:
#:   -f <file> : files to read (by now just reading a file)
#:   -o <output file> : output file where the final table is sent
#:   -O : same as -o but the name is assigned automatically based on the options given
#:   -d <display> : display format: TABLE, TABLE_POS, SET, SET_GOALSFIRST
#:   -b <bye score> : bye score : IGNORE (reject game), DRAW (0-0), WIN (0-0)
#:   -s <sort> : sort by one of (commas indicate tiebreakers):
#:     * REGULAR : points, goal avg
#:     * REGULARSOS : points, SOS, SOSOS
#:     * WSOS : weighted SOS = points + SOS/remaining rounds, points
#:     * SOS : SOS/SOSOS, points
#:     * SOSOS : SOSOS/SOS, points
#:   -r <rounds> : number of league rounds - if not set it's assumed equal as the number of declared
#:                 rounds, and WSOS does not matter (weights 0.00% in the last round)
#:   -c <round #> : count up to round #
#:
#: file contains ...
from __future__ import print_function

import sys
import getopt

# TODO : use log print / error wrappers
# TODO : add option for being silent (using the log wrappers)

class Score :

  gsHeaderShort1 = " G  p |  GS -  GR = Gavg | SOS/SOSOS | PwSOS"
  gsSepHdrShort1 = "------|------------------|-----------|------"
  gsFormatShort1 = "%2d %2d | %3d - %3d = %3d  | %4d %4d | %3d"


  def __init__( self, iMatches = 0, iPoints = 0, iGoalsMade = 0, iGoalsRecv = 0, iSOS = 0, iSOSOS = 0, iPointsPlusWeightedSOS = 0 ) :

    self.set( iMatches, iPoints, iGoalsMade, iGoalsRecv, iSOS, iSOSOS, iPointsPlusWeightedSOS )


  def set( self, iMatches, iPoints, iGoalsMade, iGoalsRecv, iSOS, iSOSOS, iPointsPlusWeightedSOS ) :

    self.miMatches = iMatches
    self.miPoints = iPoints
    self.miGoalsMade = iGoalsMade
    self.miGoalsRecv = iGoalsRecv
    self.miSOS = iSOS
    self.miSOSOS = iSOSOS
    self.miPointsPlusWeightedSOS = iPointsPlusWeightedSOS


  @staticmethod
  def textFormat_short1( pScore ) :
    return Score.gsFormatShort1 % (
      pScore.miMatches,
      pScore.miPoints,
      pScore.miGoalsMade,
      pScore.miGoalsRecv,
      pScore.miGoalsMade - pScore.miGoalsRecv,
      pScore.miSOS,
      pScore.miSOSOS,
      pScore.miPointsPlusWeightedSOS
    )



class Teams :

  def __init__( self ) :

    self.mSet = set()
    self.mListSortedTeams = None


  def initialize( self ) :

    self.add( Macmahon.TEXT_BYE )

    self.mDict = dict()
    for lsTeam in self.mSet :
      self.mDict[ lsTeam ] = Score()
    self.mSet = None
    self.mListSortedTeams = None


  def add( self, sTeam ) :
    """ adds to set of teams, returns 0 if not added """

    liLen1 = len( self.mSet )
    self.mSet.add( sTeam )
    return len( self.mSet ) - liLen1


  def size( self ) :
    return len( self.mSet )


  def getScore( self, sTeam ) :

    try :
      lRet = self.mDict[ sTeam ]
    except :
      lRet = None
    return lRet


  def setScore( self, sTeam, pScore ) :

    try :
      self.mDict[ sTeam ] = pScore
      lRet = pScore
    except :
      print( "team %s NOT found, cant be updated" % sTeam )
      lRet = None
    return lRet


  def sort( self, iOptSort ) :

    if iOptSort == Macmahon.SORT_REGULAR :
      print( "sorting by: %s" % Macmahon.OPT_SORT_REGULAR )
      self.mListSortedTeams = sorted(
        self.mDict,
        key = lambda team : (
          self.mDict[ team ].miPoints,
          self.mDict[ team ].miGoalsMade - self.mDict[ team ].miGoalsRecv,
        ),
        reverse = True )
    elif iOptSort == Macmahon.SORT_REGULARSOS :
      print( "sorting by: %s" % Macmahon.OPT_SORT_REGULARSOS )
      self.mListSortedTeams = sorted(
        self.mDict,
        key = lambda team : (
          self.mDict[ team ].miPoints,
          self.mDict[ team ].miSOS,
          self.mDict[ team ].miSOSOS,
          self.mDict[ team ].miGoalsMade - self.mDict[ team ].miGoalsRecv,
        ),
        reverse = True )
    elif iOptSort == Macmahon.SORT_WSOS :
      print( "sorting by: %s" % Macmahon.OPT_SORT_WSOS )
      self.mListSortedTeams = sorted(
        self.mDict,
        key = lambda team : (
          self.mDict[ team ].miPointsPlusWeightedSOS,
          self.mDict[ team ].miPoints,
          self.mDict[ team ].miSOS,
          self.mDict[ team ].miSOSOS,
          self.mDict[ team ].miGoalsMade - self.mDict[ team ].miGoalsRecv,
        ),
        reverse = True )
    elif iOptSort == Macmahon.SORT_SOS :
      print( "sorting by: %s" % Macmahon.OPT_SORT_SOS )
      self.mListSortedTeams = sorted(
        self.mDict,
        key = lambda team : (
          self.mDict[ team ].miSOS,
          self.mDict[ team ].miSOSOS,
          self.mDict[ team ].miPoints,
          self.mDict[ team ].miGoalsMade - self.mDict[ team ].miGoalsRecv,
        ),
        reverse = True )
    elif iOptSort == Macmahon.SORT_SOSOS :
      print( "sorting by: %s" % Macmahon.OPT_SORT_SOSOS )
      self.mListSortedTeams = sorted(
        self.mDict,
        key = lambda team : (
          self.mDict[ team ].miSOSOS,
          self.mDict[ team ].miSOS,
          self.mDict[ team ].miPoints,
          self.mDict[ team ].miGoalsMade - self.mDict[ team ].miGoalsRecv,
        ),
        reverse = True )
    else : # unsorted
      print( "sorting by: unsorted" )
      self.mListSortedTeams = self.mDict.keys()


class Settings :
  pass

class Round :
  pass


class Macmahon :

  LINE_MIN_LEN = 3

  TEXT_TEAM = "team"
  TEXT_BYE = "[BYE]"

  TEXT_STATE_SETTINGS = "settings"
  TEXT_STATE_ROUND = "round"
  STATE_NONE = 0
  STATE_TEAMS = 1
  STATE_SETTINGS = 2
  STATE_ROUND = 3

  OPT_FORMAT_SET = "SET"
  OPT_FORMAT_SET_GOALSFIRST = "SET_GOALSFIRST"
  OPT_FORMAT_TABLE = "TABLE"
  OPT_FORMAT_TABLE_POS = "TABLE_POS"
  FORMAT_NONE = 0
  FORMAT_SET = 1
  FORMAT_SET_GOALSFIRST = 2
  FORMAT_TABLE = 11
  FORMAT_TABLE_POS = 12

  OPT_BYE_IGNORE = "IGNORE"
  OPT_BYE_DRAW = "DRAW"
  OPT_BYE_WIN = "WIN"
  BYE_NONE = 0
  BYE_IGNORE = 1
  BYE_DRAW = 2
  BYE_WIN = 3

  OPT_SORT_REGULAR = "REGULAR"
  OPT_SORT_REGULARSOS = "REGULARSOS"
  OPT_SORT_WSOS = "WSOS"
  OPT_SORT_SOS = "SOS"
  OPT_SORT_SOSOS = "SOSOS"
  SORT_NONE = 0
  SORT_REGULAR = 1
  SORT_REGULARSOS = 2
  SORT_WSOS = 3
  SORT_SOS = 4
  SORT_SOSOS = 5

  gOptDict_Format = {
    OPT_FORMAT_SET : FORMAT_SET,
    OPT_FORMAT_SET_GOALSFIRST : FORMAT_SET_GOALSFIRST,
    OPT_FORMAT_TABLE : FORMAT_TABLE,
    OPT_FORMAT_TABLE_POS : FORMAT_TABLE_POS,
  }

  gOptDict_Bye = {
    OPT_BYE_IGNORE : BYE_IGNORE,
    OPT_BYE_DRAW : BYE_DRAW,
    OPT_BYE_WIN : BYE_WIN,
  }

  gOptDict_Sort = {
    OPT_SORT_REGULAR : SORT_REGULAR,
    OPT_SORT_REGULARSOS : SORT_REGULARSOS,
    OPT_SORT_WSOS : SORT_WSOS,
    OPT_SORT_SOS : SORT_SOS,
    OPT_SORT_SOSOS : SORT_SOSOS,
  }

  @staticmethod
  def usage() :
    liLine = 0
    print( "" )
    print( sys.argv[ 0 ] )
    lF = open( sys.argv[ 0 ], 'r' )
    lbFirstComm = True
    lsL = lF.readline()
    while lsL and lbFirstComm == True :
      liLine += 1
      if lsL.startswith( "#:" ) :
        print( lsL[ 3 : -1 ] )
        lsL = lF.readline()
      else :
        break
    lF.close()


  def __init__( self ) :

    self.miOptFormat = Macmahon.FORMAT_TABLE
    self.miOptSort = Macmahon.SORT_NONE
    self.miOptBye = Macmahon.BYE_IGNORE
    self.msFile = None
    self.msOptOutputfile = None
    self.mbOptOutputfileAuto = False
    self.miOptRounds = 0
    self.miOptCountRound = 0

    self.miWeightedSOS = -1
    self.miState = Macmahon.STATE_TEAMS # initial: if error, will be STATE_NONE
    self.miRound = 0

    self.mTeams = Teams()



  @staticmethod
  def eprint( sErrorMsg ) :
    print( sErrorMsg, file=sys.stderr )



  def state( self, iState ) :
    """Set state
    Return True if changed successfully
    """

    liState = self.miState
    liError = 0 # OK

    if iState == Macmahon.STATE_SETTINGS :
      if self.miState == Macmahon.STATE_TEAMS :
        self.miState = iState

    elif iState == Macmahon.STATE_ROUND :
      if not self.miState == Macmahon.STATE_NONE :
        self.miState = iState

        self.standings()
        self.miRound += 1

    if liState == Macmahon.STATE_TEAMS : # close teams definition
      self.mTeams.initialize()

    return liState == self.miState and not self.miState == Macmahon.STATE_ROUND



  @staticmethod
  def teamScore( p0, p1 ) :

    try :
      liScore = int( p0 )
      lsTeam = p1
    except :
      try :
        liScore = int( p1 )
        lsTeam = p0
      except :
        return None

    print( "team:%s, score:%d" % ( lsTeam, liScore ) )
    return lsTeam, liScore


  def parseLineTeam( self, sLine0 ) :

    lss = sLine0.split()
    if lss[ 0 ] == Macmahon.TEXT_BYE :
      print( "error team %s is not a valid name (it is added automatically)" % lss[ 0 ] )
      sys.exit(1)
    print( "adding team %s" % lss[ 0 ] )
    if self.mTeams.add( lss[ 0 ] ) == 0 :
      print( "error adding team %s, was it already added?" % lss[ 0 ] )
      sys.exit(1)
    # TODO : add initial values


  def parseLineSetting( self, sLine0 ) :
    pass


  def processMatch( self, teamHome, teamAway ) :

    lsTeamHome = teamHome[ 0 ]
    lsTeamAway = teamAway[ 0 ]

    if self.miOptBye == Macmahon.BYE_IGNORE :
      if Macmahon.TEXT_BYE in ( lsTeamHome, lsTeamAway ) :
        print( "BYE match, ignoring" )
        return

    lScoreHome = self.mTeams.getScore( lsTeamHome )
    if lScoreHome == None :
      print( "home team %s NOT found" % lsTeamHome )
      print( self.mTeams.mDict )
      sys.exit( 1 )

    lScoreAway = self.mTeams.getScore( lsTeamAway )
    if lScoreAway == None :
      print( "away team %s NOT found" % lsTeamAway )
      sys.exit( 1 )

    liMatchesHome = lScoreHome.miMatches + 1
    liMatchesAway = lScoreAway.miMatches + 1

    liGoalsHome = teamHome[ 1 ]
    liGoalsAway = teamAway[ 1 ]

    lbScoreProcessed = False
    if Macmahon.TEXT_BYE in ( lsTeamHome, lsTeamAway ) :
      if self.miOptBye == Macmahon.BYE_WIN :
        if lsTeamHome == Macmahon.TEXT_BYE :
          liPointsHome = lScoreHome.miPoints + 0
          liPointsAway = lScoreAway.miPoints + 3
        else :
          liPointsHome = lScoreHome.miPoints + 3
          liPointsAway = lScoreAway.miPoints + 0
        liGoalsMadeHome = lScoreHome.miGoalsMade
        liGoalsMadeAway = lScoreAway.miGoalsMade
        liGoalsRecvHome = lScoreHome.miGoalsRecv
        liGoalsRecvAway = lScoreAway.miGoalsRecv
        lbScoreProcessed = True
      elif self.miOptBye == Macmahon.BYE_DRAW :
        pass # this is processed below

    if lbScoreProcessed == False :
      if liGoalsHome > liGoalsAway :
        liPointsHome = lScoreHome.miPoints + 3
        liPointsAway = lScoreAway.miPoints + 0
      elif liGoalsHome < liGoalsAway :
        liPointsHome = lScoreHome.miPoints + 0
        liPointsAway = lScoreAway.miPoints + 3
      else : # ==
        liPointsHome = lScoreHome.miPoints + 1
        liPointsAway = lScoreAway.miPoints + 1

      liGoalsMadeHome = lScoreHome.miGoalsMade + liGoalsHome
      liGoalsMadeAway = lScoreAway.miGoalsMade + liGoalsAway

      liGoalsRecvHome = lScoreHome.miGoalsRecv + liGoalsAway
      liGoalsRecvAway = lScoreAway.miGoalsRecv + liGoalsHome

    liSosHome = lScoreAway.miSOS + liPointsAway
    liSosAway = lScoreHome.miSOS + liPointsHome

    liSososHome = lScoreAway.miSOSOS + liSosAway
    liSososAway = lScoreHome.miSOSOS + liSosHome

    liRounds = self.miOptRounds if self.miOptRounds > 0 else self.miRound
    liPointSosHome = liPointsHome + (liRounds - self.miRound) * liSosHome / liRounds
    liPointSosAway = liPointsAway + (liRounds - self.miRound) * liSosAway / liRounds
    self.miWeightedSOS = (liRounds - self.miRound) * 100 / liRounds

    lNewScoreHome = Score( liMatchesHome, liPointsHome, liGoalsMadeHome, liGoalsRecvHome, liSosHome, liSososHome, liPointSosHome )
    lNewScoreAway = Score( liMatchesAway, liPointsAway, liGoalsMadeAway, liGoalsRecvAway, liSosAway, liSososAway, liPointSosAway )

    self.mTeams.setScore( lsTeamHome, lNewScoreHome )
    self.mTeams.setScore( lsTeamAway, lNewScoreAway )



  def parseLineMatch( self, sLine0 ) :
    teamHome, teamAway = None, None
    lss = sLine0.split()
    if len( lss ) == 5 :
      if lss[2] == "-" :
        teamHome = Macmahon.teamScore( lss[0], lss[1] )
        teamAway = Macmahon.teamScore( lss[3], lss[4] )
        print( "--" )

    if teamHome == None and teamAway == None :
      print( "ERROR parsing match result" )
      print( lss )
      sys.exit(1)

    self.processMatch(teamHome, teamAway)


  def parseLine( self, sLine0 ) :

    liRet = 0 # OK
    # discard comment
    sLine = sLine0.split( '#' )[ 0 ]
    liLen = len( sLine )
    if liLen <= 1 : pass # OK, empty or comment line
    elif liLen < Macmahon.LINE_MIN_LEN :
      # TODO : use error method
      #print( "line lenght %d not enough, minimum %d including 2 EOL chars" % ( liLen, Macmahon.LINE_MIN_LEN ) )
      #liRet = 1
      pass
    else : # now a real line
      lsL = sLine0[ : -1 ] # -2, assuming windows fileformat
      if lsL[ 0 ] == ":" : # tag line
        lss = lsL[ 1 : ].split()
        if lss[ 0 ] == Macmahon.TEXT_STATE_SETTINGS :
          lbState = self.state( Macmahon.STATE_SETTINGS )
        elif lss[ 0 ] == Macmahon.TEXT_STATE_ROUND :
          lbState = self.state( Macmahon.STATE_ROUND )
          print( "=> round %d" % self.miRound )
        else :
          print( "unknown TAG " + lss[ 0 ] )
          sys.exit( 1 )
        if lbState :
          print( "ERROR changing to state %s" % lss[ 0 ] )
        else :
          print( "changed to state %s" % lss[ 0 ] )
      else : # content
        if self.miState == Macmahon.STATE_TEAMS :
          self.parseLineTeam( lsL )
        elif self.miState == Macmahon.STATE_SETTINGS :
          self.parseLineSetting( lsL )
        elif self.miState == Macmahon.STATE_ROUND :
          self.parseLineMatch( lsL )

    return liRet


  def standings_short1( self, bHeader = True ) :

    if bHeader :
      print( "%-14s %s" % ( Macmahon.TEXT_TEAM, Score.gsHeaderShort1 ) )
      print( "%s %s"    % ( "-" * 14, Score.gsSepHdrShort1 ) )
    for lsTeam in self.mTeams.mListSortedTeams :
      if self.miOptBye == Macmahon.BYE_IGNORE :
        if lsTeam == Macmahon.TEXT_BYE :
          continue
      lsRow = Score.textFormat_short1( self.mTeams.mDict[ lsTeam ] )
      print( "%-14s %s" % ( lsTeam, lsRow ) )


  def standings_short2( self, bHeader = True ) :

    if bHeader :
      print( "pl %-14s %s" % ( Macmahon.TEXT_TEAM, Score.gsHeaderShort1 ) )
      print( "%s %s"    % ( "-" * 17, Score.gsSepHdrShort1 ) )
    liPos = 0
    for lsTeam in self.mTeams.mListSortedTeams :
      liPos += 1
      if self.miOptBye == Macmahon.BYE_IGNORE :
        if lsTeam == Macmahon.TEXT_BYE :
          continue
      lsRow = Score.textFormat_short1( self.mTeams.mDict[ lsTeam ] )
      print( "%2d %-14s %s" % ( liPos, lsTeam, lsRow ) )


  def standings_set( self, bGoalsFirst = True ) :

    for lsTeam in self.mTeams.mListSortedTeams :
      if self.miOptBye == Macmahon.BYE_IGNORE :
        if lsTeam == Macmahon.TEXT_BYE :
          continue
      print( "----" )
      print( lsTeam )
      lScore = self.mTeams.mDict[ lsTeam ]
      if bGoalsFirst == True :
        lSet = ( lScore.miPoints, lScore.miGoalsMade, lScore.miGoalsRecv, lScore.miSOS, lScore.miSOSOS, lScore.miPointsPlusWeightedSOS )
      else :
        lSet = ( lScore.miPoints, lScore.miSOS, lScore.miSOSOS, lScore.miGoalsMade, lScore.miGoalsRecv, lScore.miPointsPlusWeightedSOS )
      print( lSet )


  def displayBye( self ) :

    if self.miOptBye == Macmahon.BYE_IGNORE :
      ls = Macmahon.OPT_BYE_IGNORE
    elif self.miOptBye == Macmahon.BYE_DRAW :
      ls = Macmahon.OPT_BYE_DRAW
    elif self.miOptBye == Macmahon.BYE_WIN :
      ls = Macmahon.OPT_BYE_WIN
    else :
      ls = "(none)"
    print( "bye treatment: %s" % ls )


  def standings( self, iFormat = FORMAT_NONE, bHeader = True ) :

    print("round %d / %d  => w (weighted SOS) = %d%% -- PwSOS = P + w * SOS" % (
      self.miRound,
      self.miOptRounds if self.miOptRounds > 0 else self.miRound,
      self.miWeightedSOS )
    )
    self.displayBye()
    self.mTeams.sort( self.miOptSort )

    if iFormat == Macmahon.FORMAT_NONE :
      iFormat = self.miOptFormat

    if iFormat == Macmahon.FORMAT_NONE or iFormat == Macmahon.FORMAT_TABLE :
      self.standings_short1( bHeader = True )
    if iFormat == Macmahon.FORMAT_TABLE_POS :
      self.standings_short2( bHeader = True )
    elif iFormat == Macmahon.FORMAT_SET :
      self.standings_set( bGoalsFirst = False )
    elif iFormat == Macmahon.FORMAT_SET_GOALSFIRST :
      self.standings_set()


  def setAutoOutputfile( self ) :

    if self.msFile == None :
      lsName = "STDIN"
    else :
      lsName = self.msFile.split("/")[-1] # remove directories
      lsName = lsName.split(".")[0] # remove extension
    lsName += "_"
    if not self.miOptFormat == Macmahon.FORMAT_TABLE and not self.miOptFormat == Macmahon.FORMAT_TABLE_POS :
      lsName += "RAW_"
    else :
      lsName = "pos_" if self.miOptFormat == Macmahon.FORMAT_TABLE_POS else ""
    if self.miOptSort == Macmahon.SORT_NONE :
      lsName += "unsorted_"
    elif self.miOptSort == Macmahon.SORT_REGULAR :
      lsName += "sortRegular_"
    elif self.miOptSort == Macmahon.SORT_REGULARSOS :
      lsName += "sortRegularSOS_"
    elif self.miOptSort == Macmahon.SORT_WSOS :
      lsName += "sortWeightedSOS_"
    elif self.miOptSort == Macmahon.SORT_SOS :
      lsName += "sortSOS_"
    elif self.miOptSort == Macmahon.SORT_SOSOS :
      lsName += "sortSOSOS_"
    if self.miOptBye == Macmahon.BYE_IGNORE :
      lsName += "byeIgnore_"
    if self.miOptBye == Macmahon.BYE_DRAW :
      lsName += "byeDraw_"
    if self.miOptBye == Macmahon.BYE_WIN :
      lsName += "byeWin_"
    liRounds = self.miOptRounds if self.miOptRounds > 0 else self.miRound
    lsName += "r%d_%d" % ( self.miRound, liRounds )
    lsName += ".txt"
    lMacmahon.msOptOutputfile = lsName


  def readFile( self ) :
    if self.msFile == None :
      self.mFile = sys.stdin
      print( "reading from stdin" )
    else :
      print( "reading from file %s" % self.msFile )
      try :
        self.mFile = open( self.msFile )
      except :
        print( "FATAL, could not open file " + msFile )
        sys.exit( 1 )

    liLines = 0
    liErrors = 0
    print( "----------" )
    for lsLine in self.mFile :
      liLines += 1
      liErrors += self.parseLine( lsLine )
      if not self.miOptCountRound == 0 and self.miRound > self.miOptCountRound :
        print( "reached max round count %d, stopping .." % self.miOptCountRound )
        self.miRound -= 1
        break
    print( "file %s processed, lines=%d, lines with errors: %d" % ( self.msFile, liLines, liErrors ) )
    if not self.msFile == None :
      self.mFile.close()


  def readBalance( self, sFile ) :
    print( "----" )
    print( "reading balance file " + sFile )
    try :
      lFile = open( sFile, "r" )
    except :
      lFile = open( sFile, "r" )
      print( "FATAL, could not open balance file " + sFile )
      sys.exit( 1 )
    liErrors = 0
    for lsLine in lFile :
      liErrors += self.parseBalLine( lsLine )
    print( "balance file processed, lines with errors: %d" % liErrors )
    lFile.close()


  def checkOptions( self, pListParams ) :

    #print( "checkOptions, args:", pListParams )
    try:
      lOptList, lList = getopt.getopt( pListParams, 'f:r:c:d:b:s:o:O' )

    except getopt.GetoptError:
      Macmahon.eprint( "FATAL : error analyzing command line options" )
      Macmahon.eprint( "" )
      Macmahon.usage()
      sys.exit( 1 )

    # TODO : use shift / setenv --

    """
    Macmahon.msFileInitialBalance = None
    """
    #print( lOptList )
    #print( lList )
    lDateRange = None
    for lOpt in lOptList :
      #print( 'lOpt :' + str( lOpt ) )
      if lOpt[0] == '-d' :
        lsVal = lOpt[1]
        if lsVal not in Macmahon.gOptDict_Format.keys() :
          print( "FATAL: wrong value '%s' for option '%s'" % ( lsVal, lOpt[0] ) )
          Macmahon.usage()
          sys.exit( 1 )
        else :
          self.miOptFormat = Macmahon.gOptDict_Format[ lsVal ]
          print( "option '%s' (format) : %s (%d)" % ( lOpt[0], lsVal, self.miOptFormat ) )
      elif lOpt[0] == '-b' :
        lsVal = lOpt[1]
        if lsVal not in Macmahon.gOptDict_Bye.keys() :
          print( "FATAL: wrong value '%s' for option '%s'" % ( lsVal, lOpt[0] ) )
          Macmahon.usage()
          sys.exit( 1 )
        else :
          self.miOptBye = Macmahon.gOptDict_Bye[ lsVal ]
          print( "option '%s' (bye) : %s (%d)" % ( lOpt[0], lsVal, self.miOptBye ) )
      elif lOpt[0] == '-s' :
        lsVal = lOpt[1]
        if lsVal not in Macmahon.gOptDict_Sort.keys() :
          print( "FATAL: wrong value '%s' for option '%s'" % ( lsVal, lOpt[0] ) )
          Macmahon.usage()
          sys.exit( 1 )
        else :
          self.miOptSort = Macmahon.gOptDict_Sort[ lsVal ]
          print( "option '%s' (sort) : %s (%d)" % ( lOpt[0], lsVal, self.miOptSort ) )
      elif lOpt[0] == '-r':
        lsVal = lOpt[1]
        print( "option '%s' (rounds) : %s" % ( lOpt[0], lsVal ) )
        try :
          self.miOptRounds = int( lsVal )
        except :
          print( "ERROR: %s not a valid number" %  lsVal )
          sys.exit(1)
        if self.miOptRounds < 2 or self.miOptRounds > 20 :
          print( "ERROR: %d must have a value between 2 and 20" % self.miOptRounds )
          sys.exit(1)
      elif lOpt[0] == '-c':
        lsVal = lOpt[1]
        print( "option '%s' (count up to round #) : %s" % ( lOpt[0], lsVal ) )
        try :
          self.miOptCountRound = int( lsVal )
        except :
          print( "ERROR: %s not a valid number" %  lsVal )
          sys.exit(1)
        if self.miOptCountRound < 1 or self.miOptCountRound > 20 :
          print( "ERROR: %d must have a value between 2 and 20" % self.miOptCountRound )
          sys.exit(1)
      elif lOpt[0] == '-f':
        lsVal = lOpt[1]
        self.msFile = lsVal
        print( "option '%s' (file) : %s" % ( lOpt[0], lsVal ) )
      elif lOpt[0] == '-o':
        lsVal = lOpt[1]
        self.msOptOutputfile = lsVal
        print( "option '%s' (output file) : %s" % ( lOpt[0], lsVal ) )
      elif lOpt[0] == '-O':
        self.mbOptOutputfileAuto = True
        print( "option '%s' (autonamed output file) set" % lOpt[0] )

    if self.mbOptOutputfileAuto and not self.msOptOutputfile == None :
      print( "ERROR: options '-o' and '-O' are mutually incompatible" )
      Macmahon.usage()
      sys.exit( 1 )

    Macmahon.msFiles = lList
    Macmahon.gTupDateRange = lDateRange




if __name__ == "__main__" :

  lMacmahon = Macmahon()
  lMacmahon.checkOptions( sys.argv[ 1 : ] )
  lMacmahon.readFile()

  """
  if not lMacmahon.msFileInitialBalance == None :
    lMacmahon.readBalance( lMacmahon.msFileInitialBalance )
  if len( lMacmahon.msFiles ) == 0 :
    # use stdin
    lMacmahon.readMovs()
  else :
    for lsFile in lMacmahon.msFiles :
      lMacmahon.readMovs( lsFile )
  """

  lMacmahon.standings()

  if lMacmahon.mbOptOutputfileAuto :
    lMacmahon.setAutoOutputfile()

  if not lMacmahon.msOptOutputfile == None :
    print("--")
    print("redirecting stdout to %s" % lMacmahon.msOptOutputfile )
    oldStdout = sys.stdout
    sys.stdout = open( lMacmahon.msOptOutputfile, "w" )
    lMacmahon.standings()
    sys.stdout.close()
    sys.stdout = oldStdout
    print("restored stdout")

