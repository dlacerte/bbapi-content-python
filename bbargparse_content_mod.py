##
# COMMAND LINE ARGUMENT PARSE MODULE for: bbapi-course-membership.py & bbapi-content.py 

# Process command-line arguments using argparse module: https://docs.python.org/2/howto/argparse.html
# ArgParse supports grouping of arguments - subparsers for each type of operation
# This script can perform the following operations on CONTENT records:
# 1) "update" the record: 
# 2) "get" a single record that matches a given CONTENTID
# 3) "list" all records matching a given CONTENTID
# 4) "delete" a single CONTENTID from the COURSE
# 5) "create" a new CONTENT item in the course
# Each operation has its own sub-parser and help example
# Added an optional -t TARGET option to specify TARGET BB INSTANCE for the commands:
# possible TARGETS are: 
#                        STAGE = wccnet-stage.blackboard.com
#                        TEST = wccnet-test.blackboard.com
#                        LIVE = wccnet-live.blackboard.com (default)
import argparse
from bbconstants import *

# The User can provide either the PK1 (numeric) value of the course or the courseID (text/numeric) string on command line
# The API path differs for each case, this function decodes the command line COURSEID to determine if it is a PK1 or courseId
def decode_CID(CID):
	global crs_primary_Path
        # If the CID from the command-line is purely numeric assume it is a PK1 and add 'underscore' and "_1" to it
	if CID.isdigit() :
		CID = '_' + CID + '_1'
        # if we find both a lone underscore and a trailing 'underscore one' we assume a valid pk1 from course_main table
	elif CID.find("_") == 0 and CID.find("_1") > 1 :
		CID = CID
	# at this point we assume User entered an alphnumeric courseId from the course_main table 
        else:
                crs_primary_Path = crs_primary_Path + "courseId:" 
	return CID
               
# FUNC: child_crs() List all CHILD content items for the given COURSEID  and CONTENTID 
# USE: bbapi-content child COURSEID CONTENTID
# GET /learn/api/public/v1/courses/{courseId}/contents/{contentId}/children
def child_crs(args):
	global APIPATH
	global FIELDS
	global QTYPE
        cid = decode_CID(args.courseid)
        FIELDS = ''
        APIPATH = crs_Path + crs_primary_Path + cid + "/contents/" + args.contentid
        #FIELDS = "&fields=name,courseId,externalId,description"
        QTYPE = 'CHILDGET'
# FUNC: top_crs() list only the TOP content items in a particular course
# USE: bbapi-content top COURSEID 
# GET /learn/api/public/v1/courses/{courseId}/contents
def top_crs(args):
	global APIPATH
	global FIELDS
	global QTYPE
        cid = decode_CID(args.courseid)
        FIELDS = ''
        APIPATH = crs_Path + crs_primary_Path + cid + "/contents"
        #FIELDS = "&fields=name,courseId,externalId,description"
        QTYPE = 'TOPGET'
# FUNC: list_crs list all CHILD content items for each TOP content item
# USE: bbapi-content list COURSEID  ( lots of output )  
# GET /learn/api/public/v1/courses/{courseId}/contents/{contentId}
def list_crs(args):
	global APIPATH
	global FIELDS
	global QTYPE
        FIELDS = ''
        APIPATH = crs_Path + crs_pattern_Path + args.courseid
        #print "API PATH = ", APIPATH 
        #FIELDS = "&fields=name,courseId,externalId,description"
        QTYPE = 'LISTGET'
# FUNC: get_crs get a single CONTENT item for a given COURSEID
# USE: bbapi-content get COURSEID CONTENTID
# GET /learn/api/public/v1/courses/{courseId}/contents/{contentId}
def get_crs(args):
	global APIPATH
	global FIELDS
	global QTYPE
        cid = decode_CID(args.courseid)
        FIELDS = ''
        APIPATH = crs_Path + crs_primary_Path + cid + "/contents/" + args.contentid 
        #FIELDS = "&fields=name,courseId,externalId,description"
        QTYPE = 'GET'
# FUNC: update_crs() update a single USER enrollment record for the specified courseId/userId 
def update_crs(args):
        global APIPATH
        global FIELDS
        global QTYPE
        cid = decode_CID(args.courseid)
        FIELDS = ''
        APIPATH  = crs_Path + crs_pattern_Path + args.courseid
        print "APIPATH = ", APIPATH 
        #FIELDS = "&fields=courseId"
        QTYPE = 'MULTIGET'
# FUNC: dir_crs() List all CONTENT records matching the USERID (string pattern) that was provided
def dir_crs(args):
        global APIPATH
        global FIELDS
        global QTYPE
        FIELDS = ''
        APIPATH  = crs_Path
        #APIPATH = APIPATH + crs_zero_offset_query
        APIPATH = APIPATH + crs_single_Path + args.courseid + crs_users_Path
        #FIELDS = "&fields=courseId"
        QTYPE = 'GET'
# FUNC: del_crs()  delete a single contentid item from a given course
def del_crs(args):
        global APIPATH
        global FIELDS
        global QTYPE
        FIELDS = ''
        APIPATH  = crs_Path
        #APIPATH = APIPATH + crs_zero_offset_query
        APIPATH = APIPATH + crs_single_Path + args.courseid + con_Path + args.contentid 
        #FIELDS = "&fields=courseId"
        QTYPE = 'DELETE'

# Define COMMAND-LINE MENU and Arguments
def bbargs():
	parser = argparse.ArgumentParser(description='Process command line Arguments')
	parser.add_argument('-t', '--target', help='-t TARGET_BB_INSTANCE: LIVE, TEST, STAGE' )
	subparsers = parser.add_subparsers(help='operational commands: top, list, update, create, delete, child ')

# list TOP contents for a given courseid
	top_parser = subparsers.add_parser('top', help="list all TOP content items for courseId")
	top_parser.set_defaults(func=top_crs)
	top_parser.add_argument('courseid', action="store", help="courseId" )

# list all TOP and CHILD content
	list_parser = subparsers.add_parser('list', help="list all CHILD items for each TOP content item")
	list_parser.set_defaults(func=list_crs)
	list_parser.add_argument('courseid', action="store", help="courseId" )

# get item for given COURSEID and CONTENTID
	get_parser = subparsers.add_parser('get', help="get one particular contentId item from courseId ")
	get_parser.set_defaults(func=get_crs)
	get_parser.add_argument('courseid', action="store", help="courseId" )
	get_parser.add_argument('contentid', action="store", help="contentId" )

# delete item for given COURSEID and CONTENTID
	del_parser = subparsers.add_parser('delete', help="delete one contentId item from courseId ")
	del_parser.set_defaults(func=del_crs)
	del_parser.add_argument('courseid', action="store", help="courseId" )
	del_parser.add_argument('contentid', action="store", help="contentId" )

# get all CHILD contnet items for a given TOP contentID in the COURSEID
	child_parser = subparsers.add_parser('child', help="get all CHILD content for a given TOP CONTNETID in COURSEID")
	child_parser.set_defaults(func=child_crs)
	child_parser.add_argument('courseid', action="store", help="courseId" )
	child_parser.add_argument('contentid', action="store", help="contentId" )

# update an existing Content record 
# the -a and -r options are optional aka required=False
	update_parser = subparsers.add_parser('update', help='update existing content item property for courseId/userId' ) 
        update_parser.set_defaults(func=update_crs)
        update_parser.add_argument('courseid', action="store", help="courseId")
#	update_parser.add_argument('-b', '--body', action="store", help="get BODY of content item", required=False )

        args = parser.parse_args()
        args.func(args)
        return args, APIPATH, FIELDS, QTYPE
