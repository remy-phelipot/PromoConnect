import re
import urllib
import urllib2

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
    data = urllib.urlencode(parameters)

    # Create and send http request
    request = urllib2.Request(captivePortailUrl,data)
    httpResponse = urllib2.urlopen(request)

    htmlResponse = httpResponse.read()

    # Search for the disconnection token and return it
    tokenExtractor = re.compile(r"NAME=\"logout_id\" TYPE=\"hidden\" "\
                                "VALUE=\"([0-9|a-z]+)\"")
    matchResult = tokenExtractor.search(htmlResponse)

    if(matchResult != None and len(matchResult.groups()) > 0):
        return matchResult
    else:
        raise RuntimeError("Cannot match HTML response. "\
                           "Maybe username/password are wrong,"\
                           " or login page/response have changed")

def disconnect(username, password):

    pass

if __name__ == '__main__':
    connect('username','password')
