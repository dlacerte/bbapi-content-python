# bbconstants file for unchanging constants values
#

# The target App Servers also requires a registered RESTful API Integration definition
# These global variables should likely be in a centralized config file
saas_test_appkey = 'your-app-key'
saas_test_appsecret = 'your-secret'
saas_test_server = "your.blackboard.com"
#
saas_prod_appkey = 'your-appkey'
saas_prod_appsecret = 'your-secret'
saas_prod_server = "your.blackboard.com"
#
saas_stage_appkey = ''
saas_stage_appsecret = ''
saas_stage_server = "your-stage.blackboard.com"
#
saas_live_appkey = 'XXX'
saas_live_appsecret = 'xx'
saas_live_server = "your-live.blackboard.com"
# All communication is via Secure HTTP https://
https = "https://"
# Use REQUESTS module to request access and optin the OAUTH2 authorization token
grant_request = { 'grant_type':'client_credentials' }
oauth_url = '/learn/api/public/v1/oauth2/token'
prox = { 'https': 'https://your-proxy.net:3128', 'http':'http://your-proxy.net:3128' }

# Path variables for building the API URL endpoint
crs_Path = '/learn/api/public/v1/courses'
crs_v2_Path = '/learn/api/public/v2/courses'
crs_single_Path = '/externalId:'
crs_courseid_Path = '/courseId:'

# Users Membership Enrollments API URL endpoint
crs_users_Path = '/users'
crs_single_user_Path = '/users/externalId:'
crs_courseid_Path = '/courseId:'
crs_pattern_Path = '?courseId='
crs_username_Path = '/users/userName:'
crs_task_Path = '/tasks'
crs_primary_Path = "/"

# Contents variables for building API URL endpoints
con_Path = '/contents/'
con_asgn_Path = '/contents/createAssignment'

# Gradebook related API paths: 
grade_columns_Path = '/gradebook/columns'
grade_column_Path = '/gradebook/columns/'
grade_users_Path = '/users'
grade_user_Path = '/users/'
grade_schemas_Path = '/schemas'
grade_schema_Path = '/schemas/'
grade_attempts_Path = '/attempts'
grade_attempt_Path = '/attempts/'
grade_notations_Path = '/gradeNotations'
grade_notation_Path = '/gradeNotations/'
grade_periods_Path = '/gradebook/periods'
grade_period_Path = '/gradebook/periods/'
grade_lastchanged_Path = '/users/lastChanged'
