#: processes a set of teams, settings and rounds and displays the standings according
#: to the settings
#:
#: usage: python macmahon.py [<options>] <file>
#: options:
#:   -h : help, displays this information
#:   -f <file> : files to read (by now just reading a file)
#:   -o <output file> : output file where the final table is sent
#:   -O : same as -o but the name is assigned automatically based on the options given
#:   -d <display> : display format: TABLE, TABLE_POS, SET, SET_GOALSFIRST
#:   -b <bye score> : bye score : IGNORE (reject game), DRAW (0-0), WIN (0-0)
#:   -s <sort> : sort by one of (commas indicate tiebreakers). If not set, the order is undeterminated.
#:     * REGULAR : points, goal avg
#:     * REGULARSOS : points, SOS, SOSOS
#:     * GOALAVG : goal avg, points
#:     * WSOS : weighted SOS = points + SOS/remaining rounds, points
#:     * SOS : SOS/SOSOS, points
#:     * SOSOS : SOSOS/SOS, points
#:     * NAME : team name
#:   -r <rounds> : number of league rounds - if not set it's assumed equal as the number of declared
#:                 rounds, and WSOS does not matter (weights 0.00% in the last round)
#:   -c <round #> : count up to round #
#:
#: See the README.md file for information about the scoring system, its
#: concepts like SOS, PwSOS etc, and the input format.

from __future__ import print_function

import sys
import getopt

# TODO : use log print / error wrappers
# TODO : add option for being silent (using the log wrappers)

# TODO : move options treatment to Settings class?

# TODO : fix doc -b => -s, s liSODOS,ort => sorts, 'This may be' => 'The script may be', 'is not played' => 'is not playing'
# TODO : autoname should consider '\' as folders (os.name == 'nt' / 'posix')
# TODO : implement weighted SODOS (draw*1, win*3)
# TODO : consider setting the value of a win and a loss (0, 1, 2) instead of (0, 1, 3)
# TODO : change team names in doc so that no junior/polo/athc appear
# TODO : display pairings (as with gerlach's sw)
# TODO : make the team declaration section optional, but reject teams after 1st round (BYE is mandatory if odd)
# TODO : allow long team names, with more than 1 word
# TODO : allow team names with unicode

# TODO : output tables:
# - very short: only goals
# - short: goals + SOS + PwSOS
# - extended: goals + SOS + SOSOS + PwSOS
# - extended2: goals + SOS + SODOS +SODOS + PwSOS
# - detailed: with pairings


gsVersion = "0.2.1"



class Score : # TODO : rename as something like 'team data'

  gsHeaderShort1 = " G  p |  GS -  GR = avg | SOS, SO[S/D]OS | PwSOS"
  gsSepHdrShort1 = "------|-----------------|----------------|------"
  gsFormatShort1 = "%2d %2d | %3d - %3d = %3d | %4d %4d %4d | %3d"


  def __init__( self, iMatches = 0, iPoints = 0, iGoalsMade = 0, iGoalsRecv = 0, iSOS = 0, iSOSOS = 0, iSODOS = 0, iPointsPlusWeightedSOS = 0 ) :

    self.set( iMatches, iPoints, iGoalsMade, iGoalsRecv, iSOS, iSOSOS, iSODOS, iPointsPlusWeightedSOS )


  def set( self, iMatches, iPoints, iGoalsMade, iGoalsRecv, iSOS = 0, iSOSOS = 0, iSODOS = 0, iPointsPlusWeightedSOS = 0 ) :

    self.miMatches = iMatches
    self.miPoints = iPoints
    self.miGoalsMade = iGoalsMade
    self.miGoalsRecv = iGoalsRecv
    self.miSOS = iSOS
    self.miSOSOS = iSOSOS
    self.miSODOS = iSODOS
    self.miPointsPlusWeightedSOS = iPointsPlusWeightedSOS


  def toString( self ) :

    return "m:%d p:%d GS:%d GR:%d SOS:%d SOSOS:%d SODOS:%d PwSOS:%s" % (
      self.miMatches,
      self.miPoints,
      self.miGoalsMade,
      self.miGoalsRecv,
      self.miSOS,
      self.miSOSOS,
      self.miSODOS,
      self.miPointsPlusWeightedSOS,
    )


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
      pScore.miSODOS,
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
    print("total number of added teams = %d" % len( self.mSet ) )
    self.mSet = None
    self.mListSortedTeams = None
    self.mDictOpponents = dict()


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


  def addOpponent( self, sTeam, sTeamOpponent ) :

    #print("adding opponent for team %s : %s" % ( sTeam, sTeamOpponent ) )
    try :
      lList = self.mDictOpponents[ sTeam ]
      #print("  found %d opponents" % len(lList) )
    except :
      #print("  no opponents found" )
      lList = []
    lList.append( sTeamOpponent )
    self.mDictOpponents[ sTeam ] = lList
    #print("  opponents now = %d" % len( self.mDictOpponents[ sTeam ] ) )

    #self.mDictOpponents[ sTeam ] = [ sTeamOpponent, ]

  def getOpponentsList( self, sTeam ) :

    try :
      lList = self.mDictOpponents[ sTeam ]
    except :
      lList = []

    return lList


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
    elif iOptSort == Macmahon.SORT_GOALAVG :
      print( "sorting by: %s" % Macmahon.OPT_SORT_GOALAVG )
      self.mListSortedTeams = sorted(
        self.mDict,
        key = lambda team : (
          self.mDict[ team ].miGoalsMade - self.mDict[ team ].miGoalsRecv,
          self.mDict[ team ].miPoints,
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
    elif iOptSort == Macmahon.SORT_NAME :
      print( "sorting by: %s" % Macmahon.OPT_SORT_NAME )
      self.mListSortedTeams = sorted( self.mDict.keys() )
    else : # unsorted
      print( "sorting by: unsorted" )
      self.mListSortedTeams = self.mDict.keys()


class Settings :
  pass


class Match :

  def __init__( self, sHomeTeam, sAwayTeam, iHomeTeamGoals, iAwayTeamGoals ) :

    self.msHomeTeam = sHomeTeam
    self.msAwayTeam = sAwayTeam
    self.miHomeTeamGoals = iHomeTeamGoals
    self.miAwayTeamGoals = iAwayTeamGoals


  @staticmethod
  def isTeamHomeInMatch( pMatch, sTeam ) :
    lbRet = False
    if pMatch.msHomeTeam == sTeam :
      lbRet = True
    return lbRet

  @staticmethod
  def isTeamAwayInMatch( pMatch, sTeam ) :
    lbRet = False
    if pMatch.msAwayTeam == sTeam :
      lbRet = True
    return lbRet

  @staticmethod
  def isTeamInMatch( pMatch, sTeam ) :
    lbRet = False
    if pMatch.msHomeTeam == sTeam or pMatch.msAwayTeam == sTeam :
      lbRet = True
    return lbRet

  # TODO : add more similar methods
  @staticmethod
  def isTeamWinnerInMatch( pMatch, sTeam ) :
    lbRet = False
    if Match.isTeamHomeInMatch( pMatch, sTeam ) :
      if pMatch.miHomeTeamGoals > pMatch.miAwayTeamGoals :
        lbRet = True
    elif Match.isTeamAwayInMatch( pMatch, sTeam ) :
      if pMatch.miHomeTeamGoals < pMatch.miAwayTeamGoals :
        lbRet = True
    return lbRet

  @staticmethod
  def getTeamPointsInMatch( pMatch, sTeam ) :
    liRet = None
    if Match.isTeamInMatch( pMatch, sTeam ) :
      if pMatch.miHomeTeamGoals == pMatch.miAwayTeamGoals : # draw
        liRet = 1
      else : # win / loss
        if pMatch.miHomeTeamGoals > pMatch.miAwayTeamGoals : # home win
          liRet = 3 if Match.isTeamHomeInMatch( pMatch, sTeam ) else 0
        else : # away win
          liRet = 3 if Match.isTeamAwayInMatch( pMatch, sTeam ) else 0
    else :
      print( "FATAL: Match.getTeamPointsInMatch, team %s not in match %s" % ( sTeam, pMatch.toString() ) )
      sys.exit(1)
    return liRet


  def toString( self ) :

    return "%d - %d [ %s vs %s ]" % (
      self.miHomeTeamGoals,
      self.miAwayTeamGoals,
      self.msHomeTeam,
      self.msAwayTeam )


class Round :

  def __init__( self ) :

    self.miNumber = None
    self.mListMatches = []


  def addMatch( self, pMatch ) :

    self.mListMatches.append( pMatch )


  def getMatch( self, sTeam ) :

    lRet = None
    for lMatch in self.mListMatches :
      if Match.isTeamInMatch( lMatch, sTeam ) :
        lRet = lMatch
        break
    return lRet



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
  OPT_SORT_NAME = "NAME"
  OPT_SORT_GOALAVG = "GOALAVG"
  SORT_NONE = 0
  SORT_REGULAR = 1
  SORT_REGULARSOS = 2
  SORT_WSOS = 3
  SORT_SOS = 4
  SORT_SOSOS = 5
  SORT_NAME = 6
  SORT_GOALAVG = 7

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
    OPT_SORT_NAME : SORT_NAME,
    OPT_SORT_GOALAVG : SORT_GOALAVG,
  }

  @staticmethod
  def usage() :
    liLine = 0
    print( "" )
    #print( sys.argv[ 0 ] )
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

    Macmahon.displayVersion()

    self.miOptFormat = Macmahon.FORMAT_TABLE
    self.miOptSort = Macmahon.SORT_NONE
    self.miOptBye = Macmahon.BYE_IGNORE
    self.msFile = None
    self.msOptOutputfile = None
    self.mbOptOutputfileAuto = False
    self.miOptRounds = 0
    self.miOptCountRound = 0

    self.miState = Macmahon.STATE_TEAMS # initial: if error, will be STATE_NONE
    self.miRound = 0

    self.mTeams = Teams()
    self.mListRounds = []
    self.mCurrentRound = None



  @staticmethod
  def eprint( sErrorMsg ) :
    print( sErrorMsg, file=sys.stderr )


  @staticmethod
  def displayVersion() :
    print( "MacMahon for teams, v%s" % gsVersion )


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

        if self.miRound >= 1 :
          print( "processing SOS for round %d" % self.miRound )
          self.processRoundSos()
          self.processRoundSosos()
          self.standings()

        self.miRound += 1
        self.mCurrentRound = Round()
        self.mListRounds.append( self.mCurrentRound ) # add to list of rounds

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

    #print( "team:%s, score:%d" % ( lsTeam, liScore ) )
    return lsTeam, liScore


  def parseLineTeam( self, sLine0 ) :

    lss = sLine0.split()
    if lss[ 0 ] == Macmahon.TEXT_BYE :
      print( "error team %s is not a valid name (it is added automatically)" % lss[ 0 ] )
      sys.exit(1)
    # TODO debug-level trace
    # print( "adding team %s" % lss[ 0 ] )
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
        #print( "BYE match, ignoring" )
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

    lNewScoreHome = Score( liMatchesHome, liPointsHome, liGoalsMadeHome, liGoalsRecvHome )
    lNewScoreAway = Score( liMatchesAway, liPointsAway, liGoalsMadeAway, liGoalsRecvAway )

    self.mTeams.setScore( lsTeamHome, lNewScoreHome )
    self.mTeams.setScore( lsTeamAway, lNewScoreAway )

    self.mTeams.addOpponent( lsTeamHome, lsTeamAway )
    self.mTeams.addOpponent( lsTeamAway, lsTeamHome )

    self.mCurrentRound.addMatch( Match( lsTeamHome, lsTeamAway, liGoalsHome, liGoalsAway ) )


  def processRoundSos( self ) :

    #print("====")
    liRounds = self.miOptRounds if self.miOptRounds > 0 else self.miRound
    liWeightedSOS = (liRounds - self.miRound) * 100 / liRounds
    #print( "processRoundSos, round %d / %d => SOS weight = %d%%" % ( self.miRound, liRounds, liWeightedSOS ) )
    for lsTeam in self.mTeams.mDict.keys() :
      # TODO : ignore BYE if IGNORE/LOSS
      #print( "calculating SOS for team %s" % lsTeam )
      lListOpponents = self.mTeams.getOpponentsList( lsTeam )
      #print( "has played against %d teams: %s" % ( len( lListOpponents ), str( lListOpponents ) ) )
      lScore = self.mTeams.mDict[ lsTeam ]
      liSOS = 0
      for lsTeamOpp in lListOpponents :
        lScoreOpp = self.mTeams.mDict[ lsTeamOpp ]
        liPoints = lScoreOpp.miPoints
        #print( "  point of opponent %s: %d" % ( lsTeamOpp, liPoints ) )
        liSOS += liPoints
        #print("-")
      #print( "SOS for team %s = %d" % ( lsTeam, liSOS ) )
      liWeightedSOS = lScore.miPoints + ( liWeightedSOS * liSOS ) / 100
      #print( "WSOS for team %s = %d" % ( lsTeam, liWeightedSOS ) )

      lNewScore = Score( lScore.miMatches, lScore.miPoints, lScore.miGoalsMade, lScore.miGoalsRecv, liSOS, lScore.miSODOS, liWeightedSOS )
      self.mTeams.setScore( lsTeam, lNewScore )
      #print("--")



  def processRoundSosos( self ) :

    #print("====")
    #print( "processRoundSosos, round %d" % ( self.miRound ) )
    for lsTeam in self.mTeams.mDict.keys() :
      # TODO : ignore BYE if IGNORE/LOSS
      #print( "calculating SOS for team %s" % lsTeam )
      lListOpponents = self.mTeams.getOpponentsList( lsTeam )
      #print( "has played against %d teams: %s" % ( len( lListOpponents ), str( lListOpponents ) ) )
      lScore = self.mTeams.mDict[ lsTeam ]
      liSOSOS = 0
      liSODOS = 0
      for lsTeamOpp in lListOpponents :
        lScoreOpp = self.mTeams.mDict[ lsTeamOpp ]
        liSOS = lScoreOpp.miSOS
        print( "  SOS of opponent %s: %d" % ( lsTeamOpp, liSOS ) )
        liSOSOS += liSOS

        lMatch = self.mCurrentRound.getMatch( lsTeamOpp )
        if lMatch == None :
          print( "  SODOS. NO match found with opponent %s for team %s" % ( lsTeamOpp, lsTeam ) )
          print("-")
          continue

        print( "  SODOS. match of opponent %s: %s" % ( lsTeamOpp, lMatch.toString() ) )
        
        if not Match.isTeamInMatch( lMatch, lsTeam ) :
	  continue
        liWeightSODOS = Match.getTeamPointsInMatch( lMatch, lsTeam )
        print( "  SODOS. match points against opponent %s: %d" % ( lsTeamOpp, liWeightSODOS ) )
        liSODOSold = liSODOS
        liSODOS += liWeightSODOS * liSOS
        print( "  SODOS. SODOS %d => %d (+ %d * %d)" % ( liSODOSold, liSODOS, liWeightSODOS, liSOS) )

        print("-")
      print( "SOSOS for team %s = %d" % ( lsTeam, liSOSOS ) )
      print( "SODOS for team %s = %d" % ( lsTeam, liSODOS ) )

      lNewScore = Score( lScore.miMatches, lScore.miPoints, lScore.miGoalsMade, lScore.miGoalsRecv, lScore.miSOS, liSOSOS, liSODOS, lScore.miPointsPlusWeightedSOS )
      print( lNewScore.toString() )
      self.mTeams.setScore( lsTeam, lNewScore )
      lScoreGet = self.mTeams.getScore( lsTeam )
      print( lScoreGet.toString() )
      print("--")



  def parseLineMatch( self, sLine0 ) :
    teamHome, teamAway = None, None
    lss = sLine0.split()
    if len( lss ) == 5 :
      if lss[2] == "-" :
        teamHome = Macmahon.teamScore( lss[0], lss[1] )
        teamAway = Macmahon.teamScore( lss[3], lss[4] )

    if teamHome == None and teamAway == None :
      print( "ERROR parsing match result" )
      print( lss )
      sys.exit(1)

    self.processMatch(teamHome, teamAway)
    #print( "--" )


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
        lSet = ( lScore.miPoints, lScore.miGoalsMade, lScore.miGoalsRecv, lScore.miSOS, lScore.miSOSOS, lScore.miSODOS, lScore.miPointsPlusWeightedSOS )
      else :
        lSet = ( lScore.miPoints, lScore.miSOS, lScore.miSOSOS, lScore.miSODOS, lScore.miGoalsMade, lScore.miGoalsRecv, lScore.miPointsPlusWeightedSOS )
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

    liRounds = self.miOptRounds if self.miOptRounds > 0 else self.miRound
    print("round %d / %d  => w (weighted SOS) = %d%% -- PwSOS = P + w * SOS" % (
      self.miRound,
      self.miOptRounds if self.miOptRounds > 0 else self.miRound,
      (liRounds - self.miRound) * 100 / liRounds )
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
      lsName += "pos_" if self.miOptFormat == Macmahon.FORMAT_TABLE_POS else ""

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
    elif self.miOptSort == Macmahon.SORT_NAME :
      lsName += "sortNAME_"

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
        print( "FATAL, could not open file " + self.msFile )
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
        # TODO : delete added round
        # self.mListRounds. ...
        break
    self.processRoundSos()
    self.processRoundSosos()
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
      lOptList, lList = getopt.getopt( pListParams, 'f:r:c:d:b:s:o:Oh' )

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
      if lOpt[0] == '-h' :
          print( "Displaying help, see README.md for more info." )
          Macmahon.usage()
          sys.exit( 0 )
      elif lOpt[0] == '-d' :
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
          print( "ERROR: %d must have a value between 1 and 20" % self.miOptCountRound )
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

  Macmahon.displayVersion()

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

