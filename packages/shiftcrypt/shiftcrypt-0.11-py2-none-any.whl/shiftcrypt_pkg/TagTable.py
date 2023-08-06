"""
Classes for dealing with STAR syntax
"""

__author__    = "$Author: jurgenfd $"
___revision__ = "$Revision: 1.10.4.1 $"
___date__     = "$Date: 2011-04-06 09:00:38 $"
 
"""
$Log: not supported by cvs2svn $
Revision 1.10  2007/07/09 12:22:26  wimvranken
Merge with branch 4.

Revision 1.9.4.1.4.4  2007/06/22 10:21:43  wimvranken
Fixed small string formatting bug

Revision 1.9.4.1.4.3  2007/06/13 08:35:52  wimvranken
Removed copyright - is not CCPN

Revision 1.9.4.1.4.2  2006/10/31 16:04:44  wimvranken
Removed crap char

Revision 1.9.4.1.4.1  2006/10/31 12:44:41  wimvranken
Output now formatted

Revision 1.9.4.1  2006/07/21 17:29:01  wimvranken
Now only contain full path imports

Revision 1.9  2005/11/03 14:07:19  wimvranken
Added extra error message printout

Revision 1.8  2005/06/27 16:43:42  wb104
Updated licenses.

Revision 1.7  2004/12/15 17:57:20  tjs23
TJS: Updated licenses.

Revision 1.6  2003/10/03 11:42:56  wfv20
Removed loose print statement

Revision 1.5  2003/09/25 12:12:49  wfv20
Adapted for better handling of quotes

Revision 1.4  2003/08/08 12:46:28  wfv20
Esthetic changes only

Revision 1.3  2003/07/24 15:28:53  wfv20
Debug code for loop crash added

Revision 1.2  2003/07/14 09:34:32  wfv20
Modified so list references are not carried through class initialization

Revision 1.1  2003/07/01 12:56:19  wfv20
Jurgen Doreleijers modified Python nmrStar reader. Bug fixes and additions (notably for reading nmrView star files) have been made.

RRevision 1.1.1.1  2001/11/02 20:16:40  jurgen
IInitial package capable of read/write access to STAR files without nested loops

"""
## Standard modules
import types

from Text           import * 
from Utils          import * 


"""
Looped and free tags can not be mixed in same object.
"""
class TagTable (Lister):
    """
    In initializing the class a content has to be given!!!
    If not then the class will make something up and it won't
    be pretty but it will be following legal syntax. Usual
    case is to call the parse method with some text and position.
    """
    
    floatPatt = re.compile("^(\-?\d+)\.?(\d*)$")
    integerPatt = re.compile("^\d+$")
    
    colspacer = 3 * ' '
    
    def __init__( self,
                  free      = None,
                  title     = '',
                  tagnames  =  None,
                  tagvalues =  None,
                  verbosity = 2
                  ):
        self.free       = free
        self.title      = title
        
        # Modified tagnames, tagvalues initialization so list references
        # are not carried through (Wim 14/07/2002)
        
        self.tagnames = tagnames
        if self.tagnames == None:
          self.tagnames  = [ '_Dummy_tag' ]
          
        self.tagvalues = tagvalues
        if self.tagvalues == None:
          self.tagvalues  = [ [None] ]
          
        self.verbosity  = verbosity
    
    "Returns the STAR text representation"
    def star_text ( self,
                    flavor                  = 'NMR-STAR'
                   ):
                   
        #
        # Code modified for better output formatting - Wim 2006/10/25
        #           
        
        ## Info herein can be transferred to a STAR reference file too
        if flavor == None or flavor == 'NMR-STAR':
            # Number of spaces before the loop_ tag. 0 in CIF
            loop_ident_size     = 3
            free_ident_size     = loop_ident_size     #@UnusedVariable
            tagnames_ident_size = loop_ident_size + 3 #@UnusedVariable
            show_stop_tag       = 1 #@UnusedVariable
        elif flavor == 'mmCIF':
            loop_ident_size     = 0
            tagnames_ident_size = 0 #@UnusedVariable
            show_stop_tag       = None #@UnusedVariable
        else:
            print 'ERROR: Unknown flavor of STAR given', flavor
            return 1
                
        loop_ident_size         = 3
        free_ident_size         = loop_ident_size
        tagnames_ident_size     = loop_ident_size + 3
        show_stop_tag           = 1
        
        starString  = ''
        count       = -1
        count_hash  = 100000 # Show progress hashes while composing text for each count_hash number of values approximately
        
        ## Free tags here
        if self.free:
            i = 0
            
            # Add some formatting...
            maxTagName = 0
            for tagName in self.tagnames:
              if len(tagName) > maxTagName:
                maxTagName = len(tagName)
            
            tagNameFormat = "%-" + str(maxTagName + 2) + "s"
            
            for tagname in self.tagnames:
                ## Just format it such that it will take the least space
                if pattern_quotes_needed.search( self.tagvalues[i][0] ):
                    tagvalue = quotes_add( self.tagvalues[i][0] )
                else:
                    tagvalue = self.tagvalues[i][0]
                starString += free_ident_size * ' ' + (tagNameFormat % tagname) + " %s" % ( tagvalue )
                if tagvalue[ -1 ] != '\n':
                    starString += '\n'
                i = i + 1
            return starString
        
        ## Loop tags here
        starString += loop_ident_size * ' ' + 'loop_\n'

        for tagname in self.tagnames:
            ## Just format it such that it will take the least space
            starString += tagnames_ident_size * ' ' + '%s\n' % tagname
        starString += '\n'
            
        col_count = len( self.tagnames )
        row_count = len( self.tagvalues[0] )
        col_range = range( col_count )
        row_range = range( row_count )

        str_row = []
        row_id = 0
        tag_id = 0
        
        #
        # Wim modifications
        # Get formatting information sorted...
        # Would be much easier if I just set it as a float/integer/whatever! 
        #
        
        colFormats = []
        colDataFuncs = []
        
        for tagvalues_column in self.tagvalues:
          isFloat = [0,0]
          isInteger = True
          maxLen = 0
          
          for tagvalue in tagvalues_column:
            
            if not tagvalue:
              continue
            
            if isFloat:
              floatSearch = self.floatPatt.search(tagvalue)
              if not floatSearch:
                isFloat = False
              else:
                numbers = len(floatSearch.group(1))
                decimals = len(floatSearch.group(2))
                if numbers > isFloat[0]:
                  isFloat[0] = numbers
                if decimals > isFloat[1]:
                  isFloat[1] = decimals
          
            if isInteger and not self.integerPatt.search(tagvalue):
              isInteger = False
              
            if maxLen < len(tagvalue):
              maxLen = len(tagvalue)
          
          if isInteger:
            colFormats.append(self.colspacer + "%" + str(maxLen) + "s")
            colDataFuncs.append(None)
          elif isFloat:
            colFormats.append(self.colspacer + "%" + str(isFloat[0] + isFloat[1] + 1) + "." + str(isFloat[1]) + "f")
            colDataFuncs.append(float)
          else:
            colFormats.append(self.colspacer + "%-" + str(maxLen + 2) + "s")
            colDataFuncs.append(None)
          
                
        ## This will quicken further actions and in itself is rather
        ## quick as we're using build in functions. I need to do this because
        ## I don't know of any splicing method that can get me a row from
        ## the table. The command below clocked 0.2 sec. on 0.6 Mb table (including
        ## spaces before parsing it was 1 Mb)
        ## Any quicker method in other modules?
        tagvalues_tr = transpose( self.tagvalues )
        
        for row_id in row_range:

            str_tmp = string.join( tagvalues_tr[row_id], ',' )

            ## Are quotes needed? Do it per row first to get some speed perhaps
            str_tmp = ''
            for col_id in col_range:
                colFormat = colFormats[col_id]
                ## Just format it such that it will take the least space
                if pattern_quotes_needed.search( self.tagvalues[col_id][row_id] ):
                    str_tmp = str_tmp + colFormat % quotes_add( self.tagvalues[col_id][row_id] )
                else:
                    tagvalue = self.tagvalues[col_id][row_id]
                    if colDataFuncs[col_id]:
                        tagvalue = colDataFuncs[col_id](tagvalue)
                    str_tmp = str_tmp + colFormat % tagvalue

            str_row.append( str_tmp )

            ## Perhaps delete for speed later on...
            if self.verbosity > 1:
                tag_id = tag_id + col_count
                if tag_id - count > count_hash:
                    count = tag_id
                    print '##### %s looped tag values collected ######' % count_hash
                                
        if show_stop_tag:
            str_row.append( '\n' + loop_ident_size * ' ' + 'stop_\n' )

        starString += string.join( str_row, '\n')

        # Save some space
        del tagvalues_tr
        
        return starString
    
    """
    A title identifing a tagtable by its tagnames
    simply the space separated concatenation of the tag names
    """
    def set_title ( self ):
        if self.verbosity >= 9:
            print 'Setting title of tagtable'
        self.title = string.join( self.tagnames )

                
    """
    Size and type checks to be extended
    0 Only fast checks
    9 Type checks of each element
    """
    def check_integrity( self, check_type=0 ):                

        names_length    = len(self.tagnames)
        values_length   = len(self.tagvalues)

        if names_length != values_length:
            print "ERROR: names_length[%s] != values_length[%s]:" % (
                names_length, values_length )
            print "ERROR: names:", self.tagnames
            return 1

        column_length_first = len( self.tagvalues[ 0 ] )            
        for tag_id in range( values_length ):
            if len( self.tagvalues[ tag_id ] ) != column_length_first:
                print "ERROR: length column[%s](%s) is not the same as" % (
                            self.tagnames[ tag_id],
                            len( self.tagvalues[ tag_id ] ) )
                print "ERROR: length column[%s](%s)" % (
                            self.tagnames[ 0],
                            column_length_first )
                return 1

        if check_type >= 9:
            cols = range( names_length )
            rows = range( column_length_first )
            for row_id in rows:
                for col_id in cols:
                    val_type = type(self.tagvalues[col_id][row_id])
                    if val_type !=  types.StringType:
                        print "ERROR: type %s is not allowed as a value in a tagtable" % val_type
                        print "ERROR: found for tagtable[%s][%s]" % ( self.tagnames[ col_id ], row_id )
                        return 1

        if self.verbosity >= 9:
            print 'Checked integrity of TagTable (%2s names %4s values each): OK [%s]' % (
                names_length, column_length_first, self.title )
        return 0
        

    """
    - Parses text into a tagtable.
    - Returns the position in the string with the first non-white space
    character after the tagtable or the length of the text in case all
    was parsed. Just to be verbose, if the tagtable is ended by a save_
    then the starting position of the save_ will be returned.
    - Assumptions here is that ;; blocks are collapsed, see Text functions
    - For speed purposes I scan ahead to see how far I can go before
    hitting a quoted tag value. I estimate in the large tables only 1 in
    1000 has a ;; block and only 1 in 5-10 has '' or "" block. For the part
    that is not quoted the parsing can be really fast.
    """
    def parse(  self,
                text      = '',
                pos       = 0 ):
        ## Parse free tagtable reading all tag name/value pairs
        if self.free:
            pos = self._tagtable_free_parse( text, pos )
            if pos == None:
                print "ERROR: tagtable_free_parse returned with ERROR"
                return None
            else:
                return pos
            if self.check_integrity():
                print "ERROR: integrity of parsed table is not ok"
                return None
            
        ## Parse looped tagtable        
        # Tag names
        match_tags_loop = pattern_tags_loop.search(text, pos)
        if not match_tags_loop:
            print "ERROR: No tag names found for looped tagtable"
            return None

        ## Do a limited search with findall for tag names
        match_tags_loop_2 = pattern_tags_loop_2.findall(text,
                                pos,
                                match_tags_loop.end() )
        for m in match_tags_loop_2:
            self.tagnames.append( m )
        pos = match_tags_loop.end()

        # End of loop
        ## There is no escaping these expensive searches if we can't depend
        ## on a stop sign
        ## Can be optimized further... by looking only up to the
        ## position already know to have a stop sign. Problem is that this
        ## is different for NMR-STAR (\sstop_) and mmCIF (\sloop_ or \s_\S)
        ## The (\ssave_) is included for when there are more flavors...
    
        text_length = len(text)
        if pos == text_length:
            print "ERROR: No tag values found for looped tagtable"
            return None

##        pos_sf_begin_or_end_nws = pattern_unquoted_find(text, pattern_sf_begin_or_end, pos)        
        pos_tagtable_loop = pattern_unquoted_find(text, pattern_tagtable_loop_2, pos)
        pos_tagtable_stop = pattern_unquoted_find(text, pattern_tagtable_stop_2, pos)
        pos_tagname       = pattern_unquoted_find(text, pattern_tagname_2, pos)

        ## Find the first one and set the end postion to the beginning of
        ## the match excluding the beginning white space character
        pos_end = text_length
        if pos_tagtable_loop != -1 and pos_tagtable_loop<pos_end:
            pos_end = pos_tagtable_loop + 1
        if pos_tagtable_stop != -1 and pos_tagtable_stop<pos_end:
            pos_end = pos_tagtable_stop + 1
        if pos_tagname != -1 and pos_tagname<pos_end:
            pos_end = pos_tagname + 1

        if self.verbosity >= 9:
            print'pos_tagtable_loop:', pos_tagtable_loop
            print'pos_tagtable_stop:', pos_tagtable_stop
            print'pos_tagname      :', pos_tagname
            print 'Will parse tagtable text to end at position: [%s]' % pos_end
            
        ## Just checking
        if not ( pos_tagtable_loop!=-1 or pos_tagtable_stop!=-1 or pos_tagname!=-1 ):
            if self.verbosity > 1:
                print 'WARNING: EOF in tagtable, must be a CIF file'
##                print 'Items looked for are a begin or end of a saveframe, or'
##                print 'a begin (loop_) or end (stop_ or _tagname) of a tagtable'
##                print '(free or looped).'
##                print 'Actually the begin/end of saveframe is not checked since'
##                print 'NMR-STAR and mmCIF both end a tagtable without it.'
        
        # Tag values
        if self._tagtable_loop_values_parse(
                text, pos, pos_end): ## will set title too
            print "ERROR: not parsed table"
            return None
        ## Set the position to the end of this tagtable at the beginning
        ## of a stop_ or a new tagtable
        pos = pos_end
        
        ## Skip the stop sign and empty space if it was stop_
        if pos_tagtable_stop != -1:
            ## Try a match from the previously found position including
            ## the white space char before it.
            match_tagtable_stop = pattern_tagtable_stop_2.search( text, pos-1 )
            if not match_tagtable_stop:
                print "ERROR: no stop_ on second try"
                return None
            pos = match_tagtable_stop.end()
        
        if self.check_integrity():
            print "ERROR: integrity of parsed table is not ok"
            return None
        return pos


    """
    Parse names and values of free tagtable loop from pos
    returns new position alias status (None for failure)
    """
    def _tagtable_free_parse( self, text, pos ):
        
        text_length = len(text)

        while pos < text_length - 1:
            if text[pos] != '_':
                break
            # Tag name
            match_tag_name = pattern_tag_name.search(text, pos)
            if match_tag_name:
                if ( match_tag_name.start() - pos ) != 0:
                    print "ERROR: looking for a free tag name (0)"
                    return None
            else:
                print "ERROR: looking for a free tag name(1)"
                return None
            self.tagnames.append( match_tag_name.group(1) )
            pos  = match_tag_name.end()
            # Tag value
            value, pos = tag_value_parse(text, pos)
            if pos == 0:
                print "ERROR: looking for a free tag name(1)"
                return None
            ## Structures of free and looped tagtable are the same
            self.tagvalues.append( [ value ] ) 
            if self.verbosity >= 9:
                print '**Parsed tag name : [%s] and value [%s]: ' % (
                    match_tag_name.group(1), value)
        self.set_title()
        return pos


    """
    Parse values of tagtable loop from pos to pos_end
    returns status (None for success, 1 for failure)
    """
    def _tagtable_loop_values_parse( self, text, pos, pos_end):
        
        if self.free:
            print "ERROR: This is a 'free' tagtable, only looped tagtable can be parsed"
            return 1

        names_length                = len(self.tagnames)

        ## Empty the table
        self.tagvalues   = []        
        for _tag_id in range( names_length ):
            self.tagvalues.append( [] )

        ## Get rid of initial white space if any, shouldn't be needed
        match_white_space = re.compile('\s+').search( text, pos, pos_end )
        if match_white_space:
            if match_white_space.start() == 0: # Match has to start at the beginning
                pos = match_white_space.end()
            
        tag_id          = 0
        count           = 0
        count_hash      = 100000
        text_length        = len(text)

        ## Only process characters to predetermined end
        while pos < pos_end:
            if self.verbosity > 1:
                if pos - count > count_hash:
                    print '##### %s chars processed ######' % count_hash
                    count = pos
            ## 1 char search; ', ", or (; at beginning of line)
            match_quoted = pattern_quoted.search( text, pos, pos_end )
            
            #
            # Wim 25/09/03: Changed following to allow correct parsing of H5'' type names
            # and "asdfasdf'" type stuff
            #

            if match_quoted:
                
                if match_quoted.start() == pos:
                    ## QUOTED:
                    value, pos = tag_value_quoted_parse( text, pos )

                    if pos ==  None:
                        print 'ERROR: got error in parse (1)'
                        return 1
                    if pos > pos_end:
                        print 'ERROR: found a quoted value that was not wholly within boundaries (1)'
                        return 1
                    self.tagvalues[ tag_id ].append( value ); tag_id = tag_id + 1

                    if tag_id == names_length:  tag_id = 0

                else:
                    
                    #
                    # New positions depend on whether correct quote or not
                    # If not correct quote, reset pos and do 'normal' parse
                    #
                    
                    if text[match_quoted.start()] in ["'",'"'] and text[match_quoted.start()-1] != " ":
                    
                        tempendpos = match_quoted.start() + string.find(text[match_quoted.start():],' ')
                      
                    else:
                    
                        tempendpos = match_quoted.start()

                    ## Parse all unquoted tag values beginning from position
                    ## UP TO specified end position
                    ## NOT QUOTED
                    
                    for t in text[pos:tempendpos].split():
                        self.tagvalues[tag_id].append( t ); tag_id = tag_id + 1
                        if tag_id == names_length: tag_id = 0
                                        
                    if tempendpos == match_quoted.start():

                        ## QUOTED:
                        pos = tempendpos
 
                        value, pos = tag_value_quoted_parse( text, pos )

                        if pos ==  None:
                            print 'ERROR: got error in parse (2)'
                            return 1
                        if pos > pos_end:
                            print 'ERROR: found a quoted value that was not wholly within boundaries (2)'
                            return 1
                        self.tagvalues[ tag_id ].append( value ); tag_id = tag_id + 1
                        if tag_id == names_length:  tag_id = 0

                    else:

                        pos = tempendpos

            else:

                ## NOT QUOTED until end (only executed once)
                for t in text[pos:pos_end].split():
                    self.tagvalues[tag_id].append( t ); tag_id = tag_id + 1
                    if tag_id == names_length: tag_id = 0

                pos = text_length # Needed to break while loop
                
            
        col_length = len( self.tagvalues[-1] )    

        if tag_id != 0:
            print "ERROR: not correct number of tag values read"
            print "Read [%s] tag(s) that is:" \
                  % ( col_length * names_length + tag_id )
            print "[%s] row(s) complete and [%s] tag value(s) in last row that is incomplete." \
                  % ( col_length, tag_id )
            print "Tag names of this table are:"
            print self.tagnames
            
            for xxx in range(0,len(self.tagvalues[0])):
             
              for yyy in range(0,len(self.tagvalues)):
                print self.tagvalues[yyy][xxx],
              
              print '\n-----------------------------------------------'
              
            pos = 0
            while pos < tag_id:
                 print self.tagvalues[pos][-1]
                 pos = pos + 1
            
            return 1

        if col_length == 0:
            print "ERROR: no tag values parsed"
            return 1

        # Set the title
        self.set_title()
        return None


###############################################################################
if __name__ == '__main__':
    STAR.verbosity = 9
##    text = """_A a _B "b'" """; free = 1
    text = """_A a b c"""; free = None
    tt = TagTable(  free      = free,
                    tagnames  = [],
                    tagvalues = [],
                    verbosity = STAR.verbosity)
    pos = tt.parse( text = text, pos = 0)
    print 'got pos: [%s] for length: [%s] (Should be the same)' % (pos, len(text))
    print tt
    print tt.star_text()
    
