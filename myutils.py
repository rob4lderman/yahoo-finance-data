#
#
#

import getopt       # for parsing cli args
import sys          # for parsing cli args

import requests     # for making http requests
import json

#
# API: https://www.dlitz.net/software/pycrypto/api/current/
#
from Crypto.Cipher import AES
from Crypto import Random
import base64


from pymongo import MongoClient


#        datestr = datestr + " {}".format( date.today().year )
#        tmpdate = datetime.strptime(datestr, "%b %d %Y")
#        return tmpdate.strftime("%m/%d/%y")
#        delta = timedelta( days=daysago )
#        begindate = datetime.today() - delta
# https://docs.python.org/3.3/library/datetime.html#strftime-strptime-behavior
from datetime import date, datetime, timedelta, timezone
import pytz


#
# Print to STDOUT
#
def logTrace( *objs ):
    print(*objs)

#
# Print to STDERR
#
def logError( *objs ):
    print( *objs, file=sys.stderr )

#
# Prints to STDERR
#
def logInfo( *objs ):
    logError( *objs )


#
# Parse command line args  
#
# @return a dictionary of opt=val
#
def parseArgs(long_options):
    opts, args = getopt.getopt( sys.argv[1:], "", long_options )
    retMe = {}
    for opt,val in opts:
       retMe[ opt ] = val
    return retMe

#
# Verify the args map contains the given required_args
#
# @return args
#
# @throws RuntimeError if required_arg is missing.
#
def verifyArgs( args, required_args ):
    for arg in required_args:
        if arg not in args:
            raise RuntimeError( 'Argument %r is required' % arg )
        elif len(args[arg]) == 0:
            raise RuntimeError( 'Argument %r is required' % arg )
    return args

#
# @return args
#
def setArgDefaultValue(args, arg, defaultValue):
    args[arg] = args[arg] if arg in args else defaultValue
    return args


#
# Write the given json object to the given file
#
def writeJson( jsonObj, filename ):
    logTrace( "writeJson: writing to file " + filename + "...");
    f = open(filename, "w")
    f.write( json.dumps( jsonObj, indent=2, sort_keys=True) )
    f.close()


#
# @return a jsonobj as read from the given json file
#
def readJson( filename ):
    logTrace( "readJson: reading from file " + filename + "...");
    f = open(filename, "r")
    jsonObj = json.load(f)
    f.close()
    return jsonObj


#
# @return a ref to the mongo db by the given name.
#
def getMongoDb( mongoUri ):
    dbname = mongoUri.split("/")[-1]
    hostname = mongoUri.split("@")[-1]
    mongoClient = MongoClient( mongoUri )
    logTrace("getMongoDb: connected to mongodb://{}, database {}".format( hostname, dbname ) )
    return mongoClient[dbname]


#
# @return JSON (dictionary) response object for the given REST GET request
#
def fetchJson(httpGetUrl):

    r = requests.get(httpGetUrl)

    logTrace("fetchJson: httpGetUrl:", httpGetUrl, "r.status_code", r.status_code)

    if r.status_code == 200:
        return r.json()
    else:
        r.raise_for_status()


#
# ---- encryption ----------------------------------------------
#

#
# @return the string s, padded on the right to the nearest multiple of bs.
#         the pad char is the ascii char for the pad length.
#
def pad(s, bs):
    retMe = s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    # logTrace("pad: retMe: #" + retMe + "#")
    return retMe


#
# @param s a string or byte[] previously returned by pad. 
#          assumes the pad char is equal to the length of the pad
#
# @return s with the pad on the right removed.
#
def unpad(s):
    retMe = s[:-ord(s[len(s)-1:])]
    # logTrace("unpad: retMe:", retMe)
    return retMe


#
# @param key - key size can be 16, 24, or 32 bytes (128, 192, 256 bits)
#              You must use the same key when encrypting and decrypting.
# @param msg - the msg to encrypt
#
# @return base64-encoded ciphertext
#
def encrypt(key, msg):
    msg = pad(msg, AES.block_size)

    #
    # iv is like a salt.  it's used for randomizing the encryption
    # such that the same input msg isn't encoded to the same cipher text
    # (so long as you use a different iv).  The iv is then prepended to
    # the ciphertext.  Before decrypting, you must remove the iv and only
    # decrypt the ciphertext.
    #
    # Note: AES.block_size is always 16 bytes (128 bits)
    #
    iv = Random.new().read(AES.block_size)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    #
    # Note: the iv is prepended to the encrypted message
    # encryptedMsg is a base64-encoded byte[] 
    # 
    return base64.b64encode(iv + cipher.encrypt(msg))


#
# @param key - key size can be 16, 24, or 32 bytes (128, 192, 256 bits)
#              You must use the same key when encrypting and decrypting.
# @param encryptedMsg - the msg to decrypt (base64-encoded), previously returned 
#                       by encrypt.  First 16 bytes is the iv (salt)
#
def decrypt(key, encryptedMsg):
    enc = base64.b64decode(encryptedMsg)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


#
# ---- dates ----------------------------------------------
#
#
def playWithDates(args):

    d = date.today()
    logTrace("playWithDates: date.today():", d, d.strftime("%a %m/%d/%Y %H:%M:%S %z %Z"))

    n = datetime.now()
    logTrace("playWithDates: datetime.now():", n, n.strftime("%a %m/%d/%Y %H:%M:%S z=%z Z=%Z"))

    n = datetime.utcnow()
    logTrace("playWithDates: datetime.utcnow():", n, n.strftime("%a %m/%d/%Y %H:%M:%S z=%z Z=%Z"))

    n = datetime.now().isoformat(' ')
    logTrace("playWithDates: datetime.now().isoformat():", n)

    n = datetime.now(tz=pytz.utc)
    logTrace("playWithDates: datetime.now(tz=pytz.utc):", n, n.strftime("%a %m/%d/%Y %H:%M:%S z=%z Z=%Z"))

    tz = pytz.timezone("America/Denver")
    n = datetime.now(tz=tz)
    logTrace("playWithDates: datetime.now(tz=pytz.timezone(America/Denver)):", n, n.strftime("%a %m/%d/%Y %H:%M:%S z=%z Z=%Z"))

    n = datetime.now(tz=pytz.timezone("America/New_York"))
    logTrace("playWithDates: datetime.now(tz=pytz.timezone([merica/New_York)):", n, n.strftime("%a %m/%d/%Y %H:%M:%S z=%z Z=%Z"))



