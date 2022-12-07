""" Request to register account """
REGISTER_REQ = 0
""" Failed to register """
REGISTER_FAIL = 1
""" Successfully registered """
REGISTER_SUCCESS = 2


""" Request to login account """
LOGIN_REQ = 3
""" Failed to login """
LOGIN_FAIL = 4
""" Successfully logged in """
LOGIN_SUCCESS = 5

""" Updating personal info """
UPDATE_INFO = 6



""" Email or password is too long """
TOO_LONG = 7
""" Email or password is invalid """
INVALID_INPUT = 8
""" Proper input for email / password """
VALID_INPUT = 9

""" Used for sending parts of user data at a time """
APPOINMENTS = 10
VACCINES = 11
HEALTHCARD = 12
INFORMATION = 13

""" For indexing the right data """
DATA_INDEXES = {INFORMATION : 0, APPOINMENTS : 1, VACCINES : 2, HEALTHCARD : 3}