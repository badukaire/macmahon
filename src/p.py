#: processes a set of teams, settings and rounds and displays the standings according
#: to the settings
#:
#: usage: python p.py [<options>] <file>
#: options:
#:   -f <file> : files to read (by now just reading a file)
#:   -d <display> : display format: TABLE, SET, SET_GOALSFIRST
#:   -b <bye score> : bye score : IGNORE (reject game), DRAW (0-0), WIN (0-0)
#:   -s <sort> : sort by: REGULAR (points/goal avg), HALFSOS (points+SOS/2)
#:
#: file contains ...
from __future__ import print_function

import sys
import getopt


class Score :
  
  gsHeaderShort1 = " p |  GS -  GR = Gavg | SOS/SOSOS | PhSOS"
  gsSepHdrShort1 = "---|------------------|-----------|------"
  gsFormatShort1 = "%2d | %3d - %3d = %3d  | %4d %4d | %3d"


  def __init__( self, iPoints = 0, iGoalsMade = 0, iGoalsRecv = 0, iSOS = 0, iSOSOS = 0, iPointsPlusHalfSOS = 0 ) :

    self.set( iPoints, iGoalsMade, iGoalsRecv, iSOS, iSOSOS, iPointsPlusHalfSOS )


  def set( self, iPoints, iGoalsMade, iGoalsRecv, iSOS, iSOSOS, iPointsPlusHalfSOS ) :

    self.miPoints = iPoints
    self.miGoalsMade = iGoalsMade
    self.miGoalsRecv = iGoalsRecv
    self.miSOS = iSOS
    self.miSOSOS = iSOSOS
    self.miPointsPlusHalfSOS = iPointsPlusHalfSOS


  @staticmethod
  def textFormat_short1( pScore ) :
    return Score.gsFormatShort1 % (
      pScore.miPoints,
      pScore.miGoalsMade,
      pScore.miGoalsRecv,
      pScore.miGoalsMade - pScore.miGoalsRecv,
      pScore.miSOS,
      pScore.miSOSOS,
      pScore.miPointsPlusHalfSOS
    )



class Teams :
  

  def __init__( self ) :

    self.mSet = set()


  def initialize( self ) :

    self.mDict = dict()
    for lsTeam in self.mSet :
      self.mDict[ lsTeam ] = Score()
    self.mSet = None


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


class Settings :
  pass

class Round :
  pass


class Macmahon :

  LINE_MIN_LEN = 4

  TEXT_STATE_TEAMS = "teams"
  TEXT_STATE_SETTINGS = "settings"
  TEXT_STATE_ROUND = "round"
  STATE_NONE = 0
  STATE_TEAMS = 1
  STATE_SETTINGS = 2
  STATE_ROUND = 3

  OPT_FORMAT_SET = "SET"
  OPT_FORMAT_SET_GOALSFIRST = "SET_GOALSFIRST"
  OPT_FORMAT_TABLE = "TABLE"
  FORMAT_NONE = 0
  FORMAT_SET = 1
  FORMAT_SET_GOALSFIRST = 2
  FORMAT_TABLE = 11

  OPT_BYE_IGNORE = "IGNORE"
  OPT_BYE_DRAW = "DRAW"
  OPT_BYE_WIN = "WIN"
  BYE_NONE = 0
  BYE_IGNORE = 1
  BYE_DRAW = 2
  BYE_WIN = 3

  OPT_SORT_REGULAR = "REGULAR"
  OPT_SORT_HALFSOS = "HALFSOS"
  SORT_NONE = 0
  SORT_REGULAR = 1
  SORT_HALFSOS = 2

  gOptDict_Format = {
    OPT_FORMAT_SET : FORMAT_SET,
    OPT_FORMAT_SET_GOALSFIRST : FORMAT_SET_GOALSFIRST,
    OPT_FORMAT_TABLE : FORMAT_TABLE,
  }

  gOptDict_Bye = {
    OPT_BYE_IGNORE : BYE_IGNORE,
    OPT_BYE_DRAW : BYE_DRAW,
    OPT_BYE_WIN : BYE_WIN,
  }

  gOptDict_Sort = {
    OPT_SORT_REGULAR : SORT_REGULAR,
    OPT_SORT_HALFSOS : SORT_HALFSOS,
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

    self.miOptFormat = Macmahon.FORMAT_NONE
    self.miOptSort = Macmahon.SORT_NONE
    self.miOptBye = Macmahon.BYE_NONE

    self.miState = Macmahon.STATE_NONE
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
    if iState == Macmahon.STATE_TEAMS :
      if self.miState == Macmahon.STATE_NONE :
        self.miState = iState

    elif iState == Macmahon.STATE_SETTINGS :
      if self.miState == Macmahon.STATE_NONE or self.miState == Macmahon.STATE_TEAMS :
        self.miState = iState

    elif iState == Macmahon.STATE_ROUND :
      if not self.miState == Macmahon.STATE_NONE :
        self.miState = iState

        self.standings()
        self.miRound += 1
        #if self.miRound == 3 :
        #  sys.exit(0)

    if liState == Macmahon.STATE_TEAMS : # close teams definition
      self.mTeams.initialize()

    return liState == self.miState and not self.miState == Macmahon.STATE_ROUND



  @staticmethod
  def valTeam( sVal ) :
    liRet = 0 # OK, default
    liLen = len( sVal )
    if liLen > 1 : # TODO
      liRet = 1
      Macmahon.eprint( 'account name %s too long (%d), max is %d' % ( sVal, liLen, Acct.W_ACCT ) )
    else : # TODO
      liRet = 1
      Macmahon.eprint( 'account name %s not valid, must start by %s' % ( sVal, Acct.gssTypes ) )
    return liRet


  @staticmethod
  def valMatch( sMatch ) :
    liRet = 1
    return liRet


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
    print( "adding team %s" % lss[ 0 ] )
    if self.mTeams.add( lss[ 0 ] ) == 0 :
      print( "error adding team %s, is it already added?" % lss[ 0 ] )
    # TODO : add initial values


  def parseLineSetting( self, sLine0 ) :
    pass


  def processMatch( self, teamHome, teamAway ) :

    lsTeamHome = teamHome[ 0 ]
    lsTeamAway = teamAway[ 0 ]

    lScoreHome = self.mTeams.getScore( lsTeamHome )
    if lScoreHome == None :
      print( "home team %s NOT found" % lsTeamHome )
      print( self.mTeams.mDict )
      sys.exit( 1 )

    lScoreAway = self.mTeams.getScore( lsTeamAway )
    if lScoreAway == None :
      print( "away team %s NOT found" % lsTeamAway )
      sys.exit( 1 )

    liGoalsHome = teamHome[ 1 ]
    liGoalsAway = teamAway[ 1 ]

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

    liPointSosHome = liPointsHome + liSosHome / 2
    liPointSosAway = liPointsAway + liSosAway / 2

    lNewScoreHome = Score( liPointsHome, liGoalsMadeHome, liGoalsRecvHome, liSosHome, liSososHome, liPointSosHome )
    lNewScoreAway = Score( liPointsAway, liGoalsMadeAway, liGoalsRecvAway, liSosAway, liSososAway, liPointSosAway )

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
      print( "line lenght %d not enough, minimum %d" % ( liLen, Acct.W_BAL_LINE ) )
      liRet = 1
    else : # now a real line
      lsL = sLine0[ : -1 ] # -2, assuming windows fileformat
      if lsL[ 0 ] == ":" : # tag line
        lss = lsL[ 1 : ].split()
        if lss[ 0 ] == Macmahon.TEXT_STATE_TEAMS :
          lbState = self.state( Macmahon.STATE_TEAMS )
        elif lss[ 0 ] == Macmahon.TEXT_STATE_SETTINGS :
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
      print( "%-14s %s" % ( Macmahon.TEXT_STATE_TEAMS, Score.gsHeaderShort1 ) )
      print( "%s %s"    % ( "-" * 14, Score.gsSepHdrShort1 ) )
    for lsTeam in self.mTeams.mDict.keys() :
      lsRow = Score.textFormat_short1( self.mTeams.mDict[ lsTeam ] )
      print( "%-14s %s" % ( lsTeam, lsRow ) )


  def standings_set( self, bGoalsFirst = True ) :
    for lsTeam in self.mTeams.mDict.keys() :
      print( "----" )
      print( lsTeam )
      lScore = self.mTeams.mDict[ lsTeam ]
      if bGoalsFirst == True :
        lSet = ( lScore.miPoints, lScore.miGoalsMade, lScore.miGoalsRecv, lScore.miSOS, lScore.miSOSOS, lScore.miPointsPlusHalfSOS )
      else :
        lSet = ( lScore.miPoints, lScore.miSOS, lScore.miSOSOS, lScore.miGoalsMade, lScore.miGoalsRecv, lScore.miPointsPlusHalfSOS )
      print( lSet )


  def standings( self, iFormat = FORMAT_NONE, bHeader = True ) :

    if iFormat == Macmahon.FORMAT_NONE :
      iFormat = self.miOptFormat

    if iFormat == Macmahon.FORMAT_NONE or iFormat == Macmahon.FORMAT_TABLE :
      self.standings_short1( bHeader = True )
    elif iFormat == Macmahon.FORMAT_SET :
      self.standings_set( bGoalsFirst = False )
    elif iFormat == Macmahon.FORMAT_SET_GOALSFIRST :
      self.standings_set()


  def readFile( self, sFile = None ) :
    if sFile == None :
      self.mFile = sys.stdin
      print( "reading from stdin" )
    else :
      print( "reading from file %s" % sFile )
      try :
        self.mFile = open( sFile )
      except :
        print( "FATAL, could not open file " + sFile )
        sys.exit( 1 )

    liLines = 0
    liErrors = 0
    print( "----------" )
    for lsLine in self.mFile :
      liLines += 1
      liErrors += self.parseLine( lsLine )
    print( "file processed, lines=%d, lines with errors: %d" % ( liLines, liErrors ) )
    if not sFile == None :
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
      lOptList, lList = getopt.getopt( pListParams, 'f:d:b:s:' )

    except getopt.GetoptError:
      Macmahon.eprint( "FATAL : error analyzing command line options" )
      Macmahon.eprint( "" )
      Macmahon.usage()
      sys.exit( 1 )

    # TODO : use shift / setenv --

    Macmahon.gsFileInitialBalance = None
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
      elif lOpt[0] == '-f':
        lsVal = lOpt[1]
        Macmahon.gsFile = lsVal
        print( "option '%s' (file) : %s" % ( lOpt[0], lsVal ) )

    Macmahon.gsFiles = lList
    Macmahon.gTupDateRange = lDateRange



if __name__ == "__main__" :

  lMacmahon = Macmahon()
  lMacmahon.checkOptions( sys.argv[ 1 : ] )
  lMacmahon.readFile( Macmahon.gsFile )

  """
  if not Macmahon.gsFileInitialBalance == None :
    lMacmahon.readBalance( Macmahon.gsFileInitialBalance )
  if len( Macmahon.gsFiles ) == 0 :
    # use stdin
    lMacmahon.readMovs()
  else :
    for lsFile in Macmahon.gsFiles :
      lMacmahon.readMovs( lsFile )
  """

  lMacmahon.standings()
