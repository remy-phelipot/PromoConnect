import re
import urllib.parse, urllib.request

# Address of the login web page
captivePortailUrl = "https://portail-promologis-lan.insa-toulouse.fr"\
                    ":8001"

# Perform the connection process
# return the disconnection token if the connection is succesful
def connect(username, password):
    parameters = {'accept':'Connexion',
                  'auth_user':username,
                  'auth_pass':password,
                  'redirurl':'https://www.kernel.org',
                  'checkbox_charte':'on'}
    data = urllib.parse.urlencode(parameters).encode('ascii')

    # Create and send http request
    request = urllib.request.Request(captivePortailUrl,data)
    httpResponse = urllib.request.urlopen(request)

    htmlResponse = httpResponse.read().decode('ascii')

    # Search for the disconnection token and return it
    tokenExtractor = re.compile(r"NAME=\"logout_id\" TYPE=\"hidden\" "\
                                "VALUE=\"([0-9|a-z]+)\"")
    matchResult = tokenExtractor.search(htmlResponse)

    if(matchResult != None and len(matchResult.groups()) > 0):
        return matchResult.groups()[0]
    else:
        raise RuntimeError("Cannot match HTML response. "\
                           "Maybe username/password are wrong,"\
                           " or login page/response have changed")

# Perform the disconnection process
def disconnect(disconnectionToken):
    parameters = {'logout_id':disconnectionToken,
                  'logout':'Deconnection'}
    data = urllib.parse.urlencode(parameters).encode('ascii')

    # Create and send http request
    request = urllib.request.Request(captivePortailUrl,data)
    httpResponse = urllib.request.urlopen(request)
    htmlResponse = httpResponse.read().decode('ascii')

    responseChecker = re.compile("You have been disconnected.")

    if(responseChecker.search(htmlResponse) == None):
        raise RuntimeError("Cannot match HTML response. "\
                           "Maybe disconnection web page has changed"\
                           " or the token id was not correct")

if __name__ == '__main__':
    token = connect('username','password')
    disconnect(token)
