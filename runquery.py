#!/usr/bin/python3
#
# It has begun..
#
#

import csv
import json
import myutils
import os
import functools    # reduce

import requests     # for making http requests

import statistics   # TODO

import pandas       # TODO

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
# @return the command-line args map
#
def parseArgs():
    long_options = [ "action=", 
                     "sql=", 
                     "mongouri=",
                     "outputfile=",
                     "inputfile=",
                     "startdate=", 
                     "enddate=",
                     "symbol="
                   ]
    args = myutils.verifyArgs( myutils.parseArgs(long_options), 
                               required_args = [ '--action' ] )
    myutils.logTrace("parseArgs: verified args=", args)
    return args


# -rx- #
# -rx- # @return AES-encrypted creds
# -rx- #
# -rx- def encryptCreds( creds ):
# -rx-     key = os.environ['ARI_AES_KEY'].encode('utf-8')
# -rx-     return myutils.encrypt(key, creds).decode('utf-8')
# -rx- 
# -rx- 
# -rx- #
# -rx- # @return AES-derypted creds
# -rx- #
# -rx- def decryptCreds( encCreds ):
# -rx-     key = os.environ['ARI_AES_KEY'].encode('utf-8')
# -rx-     return myutils.decrypt(key, encCreds )
# -rx- 



#
# @return csvdata from the given URL, one record per line
#
def fetchCsv(httpGetUrl):

    r = requests.get(httpGetUrl)

    myutils.logTrace("fetchCsv: httpGetUrl:", httpGetUrl, "r.status_code", r.status_code)

    if r.status_code == 200:
        return r.text.split("\n")
    else:
        r.raise_for_status()


#
# @param csvfile - an iterable over csv data, one record per iteration)
#
# @return the given csvfile converted into JSON (dictionary) records
#
def convertCsvToJson( csvfile ):
    reader = csv.DictReader(csvfile)
    return list(reader)


#
# {
#     "Date": "1992-07-20", 
#     "Symbol": "IBM", 
#     "_id": "IBM-1992-07-20", 
#     "Volume": "11625200", 
#     "Adj Close": "15.985412", 
#     "Open": "93.25", 
#     "Low": "92.75", 
#     "High": "93.375", 
#     "Close": "92.875"
# }
#
# @return quote
#
def buildQuoteRecord(quote, symbol):
    quote["Symbol"] = symbol 
    quote["_id"] = quote["Symbol"] + "-" + quote["Date"]
    quote["Volume"] = int(quote["Volume"])

    for floatField in [ "Adj Close", "Open", "Low", "High", "Close" ]:
        quote[floatField] = float(quote[floatField])

    return quote

#
#
# Parse the CSV result into JSON dictionaries
#
# [http://ichart.finance.yahoo.com/table.csv?s=WU&a=01&b=19&c=2010&d=01&e=19&f=2010&g=d&ignore=.csv](http://ichart.finance.yahoo.com/table.csv?s=WU&a=01&b=19&c=2010&d=01&e=19&f=2010&g=d&ignore=.csv)
#    * startdate=a+1/b/c
#    * enddate=d+1/e/f
#
# Date,Open,High,Low,Close,Volume,Adj Close
# 2016-05-13,148.789993,149.860001,147.419998,147.720001,2371800,147.720001
# 2016-05-12,149.210007,149.389999,147.110001,148.839996,3247000,148.839996
# 2016-05-11,149.710007,151.089996,148.740005,148.949997,3050000,148.949997
# 2016-05-10,148.240005,150.039993,147.740005,149.970001,3982400,149.970001
# 2016-05-09,147.699997,148.199997,147.009995,147.339996,4274500,147.339996
# 2016-05-06,144.860001,147.970001,144.470001,147.289993,4880300,147.289993
# 2016-05-05,145.949997,147.300003,145.449997,146.470001,6501200,145.070003
# 2016-05-04,143.360001,145.00,143.309998,144.25,2577100,142.871221
# 2016-05-03,144.649994,144.899994,142.899994,144.130005,3584300,142.752373
# 2016-05-02,146.559998,147.00,144.429993,145.270004,3502400,143.881476
#
# @return list of quotes, in dictionary form
# 
def fetchYahooHistoricalDataCsv( symbol, startdate, enddate ):

    url = "http://ichart.finance.yahoo.com/table.csv?s={0}&a={1}&b={2}&c={3}&d={4}&e={5}&f={6}&g=d&ignore=.csv".format( symbol,
                                                                                                                         startdate.month-1,
                                                                                                                         startdate.day,
                                                                                                                         startdate.year,
                                                                                                                         enddate.month-1,
                                                                                                                         enddate.day,
                                                                                                                         enddate.year)
                                                                                                

    retMe = list( map( lambda quote: buildQuoteRecord(quote, symbol), convertCsvToJson( fetchCsv(url) ) ) )
    myutils.logTrace("fetchYahooHistoricalDataCsv: len(retMe):", len(retMe), "retMe[0]:", ( json.dumps(retMe[0]) if len(retMe) > 0 else "") )
    return retMe


#
# @return JSON data from query.yahooapis.com
#
def fetchYahooData(sql):
    return myutils.fetchJson('http://query.yahooapis.com/v1/public/yql?env=http://datatables.org/alltables.env&format=json&q={0}'.format(sql))


#
# @return true if r["query"]["count"] > 0
#
def haveQuoteData(r):
    return r["query"]["count"] > 0
    # return r["query"] is not None and r["query"]["results"] is not None and r["query"]["results"]["quote"] is not None


#
# --symbol IBM --startdate 2016-04-25 --enddate 2016-05-01
#
#    fetchYahooData: {
#      "query": {
#        "count": 5,
#        "created": "2016-05-10T06:30:06Z",
#        "lang": "en-US",
#        "results": {
#          "quote": [
#            {
#              "Adj_Close": "144.54507",
#              "Close": "145.940002",
#              "Date": "2016-04-29",
#              "High": "147.339996",
#              "Low": "144.190002",
#              "Open": "146.490005",
#              "Symbol": "IBM",
#              "Volume": "4225800"
#            },
#            ...
#          ]
#        }
#      }
#    }
#
#
# @return list of quotes.
#
def fetchYahooHistoricalData(symbol, startdate, enddate):

    myutils.logTrace("fetchYahooHistoricalData:", symbol, startdate, enddate)

    sql = 'select * from yahoo.finance.historicaldata where startDate="{0}" and endDate="{1}" and symbol="{2}"'.format( startdate,
                                                                                                                        enddate,
                                                                                                                        symbol)

    r = fetchYahooData(sql)

    if not haveQuoteData(r):
        myutils.logTrace("fetchYahooHistoricalData: response:", json.dumps(r))
        return []
    else:
        return r["query"]["results"]["quote"]


#
# Upsert quote to db
#
def upsertQuote( db, quote ):
    myutils.logTrace("upsertQuote: ", json.dumps(quote))
    db.quotes.update_one( { "_id": quote["_id"] }, 
                          { "$set": quote }, 
                          upsert=True )
    return quote



#
# --symbol IBM --startdate 2016-04-25 --enddate 2016-05-01
# 
#
def downloadYahooHistoricalData(args):

    db = myutils.getMongoDb( os.environ["R4_MONGO_URI"] )

    args = myutils.setArgDefaultValue(args, '--startdate', '1950-01-01')
    args = myutils.setArgDefaultValue(args, '--enddate', date.today().strftime("%Y-%m-%d"))
    args = myutils.verifyArgs( args, required_args = [ '--symbol', '--startdate', '--enddate' ] )

    historicalQuotes = fetchYahooHistoricalDataCsv(args['--symbol'], 
                                                   datetime.strptime( args['--startdate'], "%Y-%m-%d"), 
                                                   datetime.strptime( args['--enddate'], "%Y-%m-%d") )


    # historicalQuotes = searchAndFetchYahooHistoricalData( args['--symbol'], 
    #                                                       args['--startdate'], 
    #                                                       args['--enddate'] )

    [ upsertQuote( db, historicalQuote ) for historicalQuote in historicalQuotes]



#
# Compute the simple moving average for the given number of days (periods)
#
# @return quotes, with new field: {days}-SimpleMovingAverage
#
def computeSimpleMovingAvg( days, quotes ):

    min_days = 200

    for i in range(min_days,len(quotes)):
        ma = sum( map( lambda quote: quote["Adj Close"], quotes[i-days+1:i+1] ) ) / days
        quotes[i][str(days) + "-SimpleMovingAverage"] = ma
        # Note: yahoo finance uses "Close" to calc 200-day and 50-day moving avg.
        #       but "Close" doesn't take dividends into consideration!
        # ma = sum( map( lambda quote: quote["Close"], quotes[i-days+1:i+1] ) ) / days
        # quotes[i]["movingAverage" + str(days) + "Close"] = ma

    return quotes


#
# Compute periodic FORWARD returns for a given field in the quote data.
#
# FORWARD Return = (quote[five-days-from-today] - quote[today]) / quote[today]
#
# @param fieldName - the quote field to calc the forward return on
# @param numPeriods - the number of periods
# @param quotes - quote data
#
# @return quotes, with new field: {fieldName}-{numPeriods}-PeriodForwardReturn
#
def computePeriodicForwardReturn( fieldName, numPeriods, quotes ):

    for i in range(len(quotes) - numPeriods):
        if fieldName in quotes[i] and fieldName in quotes[i+numPeriods]:
            r = (quotes[i+numPeriods][fieldName] - quotes[i][fieldName]) / quotes[i][fieldName]
            quotes[i][fieldName + "-" + str(numPeriods) + "-PeriodForwardReturn"] = r

    return quotes

#
# Compute periodic returns for a given field in the quote data.
#
# Return = (quote[today] - quote[five-days-ago]) / quote[five-days-ago]
#
# @param fieldName - the quote field to calc the return on
# @param numPeriods - the number of periods
# @param quotes - quote data
#
# @return quotes, with new field: {fieldName}-{numPeriods}-PeriodReturn
#
def computePeriodicReturn( fieldName, numPeriods, quotes ):

    for i in range(numPeriods, len(quotes) ):
        if fieldName in quotes[i] and fieldName in quotes[i-numPeriods]:
            r = (quotes[i][fieldName] - quotes[i-numPeriods][fieldName]) / quotes[i-numPeriods][fieldName]
            quotes[i][fieldName + "-" + str(numPeriods) + "-PeriodReturn"] = r

    return quotes


#
# Tag historical quotes when a golden cross occurred;
#
# i.e the 50-day SMA moved above the 200-day SMA
#
def tagGoldenCrossEvents( quotes ):

    # only have ma data from min_days on
    min_days = 200

    for i in range(min_days+1, len(quotes)):
        if (quotes[i-1]["50-SimpleMovingAverage"] < quotes[i-1]["200-SimpleMovingAverage"]
                and quotes[i]["50-SimpleMovingAverage"] > quotes[i]["200-SimpleMovingAverage"] ):
            quotes[i]["GoldenCross"] = True

    return quotes


#
# TODO
#
def sumField(quotes, fieldName):
    retMe = functools.reduce( lambda memo, quote: memo + quote.get(fieldName, 0.0),
                              quotes,
                              0 )
    return retMe


#
# TODO
# 
def meanField_x(quotes, fieldName):
    filteredQuotes = list( filter(lambda quote: fieldName in quote, quotes) )
    return sumField( filteredQuotes, fieldName ) / float(len(filteredQuotes))


#
# TODO
#
def meanField(quotes, fieldName):
    filteredQuotes = list( filter(lambda quote: fieldName in quote, quotes) )
    return statistics.mean( [quote[fieldName] for quote in filteredQuotes] )


#
# TODO
#
def stdevField(quotes, fieldName):
    filteredQuotes = list( filter(lambda quote: fieldName in quote, quotes) )
    # return statistics.pstdev( [quote[fieldName] for quote in filteredQuotes] )
    return statistics.pstdev( pluck(filteredQuotes, fieldName) )


#
# TODO
#
def pluck(dicts, fieldName):
    return [dic[fieldName] for dic in dicts]


#
# TODO
#
def analyzeGoldenCrosses( quotes ):

    goldenCrossQuotes = list( filter(lambda quote: "GoldenCross" in quote and quote["GoldenCross"] == True, quotes) )

    goldenCrossMovingUpQuotes = list( filter(lambda quote: quote["200-SimpleMovingAverage-1-PeriodReturn"] > 0 
                                                           and quote["50-SimpleMovingAverage-1-PeriodReturn"] > 0, goldenCrossQuotes) )

    myutils.logTrace( "analyzeGoldenCrosses: goldenCrossQuotes:", len(goldenCrossQuotes), json.dumps(goldenCrossQuotes))
    myutils.logTrace( "analyzeGoldenCrosses: goldenCrossMovingUpQuotes:", len(goldenCrossMovingUpQuotes), json.dumps(goldenCrossMovingUpQuotes))

    myutils.logTrace("analyzeGoldenCrosses: goldenCrossQuotes:", "\n",
                     "mean(Adj Close-5-PeriodForwardReturn):", meanField( goldenCrossQuotes, "Adj Close-5-PeriodForwardReturn" ), "\n",
                     "mean(Adj Close-20-PeriodForwardReturn):", meanField( goldenCrossQuotes, "Adj Close-20-PeriodForwardReturn" ), "\n",
                     "mean(Adj Close-65-PeriodForwardReturn):", meanField( goldenCrossQuotes, "Adj Close-65-PeriodForwardReturn" ), "\n",
                     "mean(Adj Close-130-PeriodForwardReturn):", meanField( goldenCrossQuotes, "Adj Close-130-PeriodForwardReturn" ), "\n",
                     "stdev(Adj Close-130-PeriodForwardReturn):", stdevField( goldenCrossQuotes, "Adj Close-130-PeriodForwardReturn" ), "\n",
                     "mean(Adj Close-260-PeriodForwardReturn):", meanField( goldenCrossQuotes, "Adj Close-260-PeriodForwardReturn" ), "\n",
                     "stdev(Adj Close-260-PeriodForwardReturn):", stdevField( goldenCrossQuotes, "Adj Close-260-PeriodForwardReturn" ) )

    myutils.logTrace("analyzeGoldenCrosses: goldenCrossMovingUpQuotes:", "\n",
                     "mean(Adj Close-5-PeriodForwardReturn):", meanField( goldenCrossMovingUpQuotes, "Adj Close-5-PeriodForwardReturn" ), "\n",
                     "mean(Adj Close-20-PeriodForwardReturn):", meanField( goldenCrossMovingUpQuotes, "Adj Close-20-PeriodForwardReturn" ), "\n",
                     "mean(Adj Close-65-PeriodForwardReturn):", meanField( goldenCrossMovingUpQuotes, "Adj Close-65-PeriodForwardReturn" ), "\n",
                     "mean(Adj Close-130-PeriodForwardReturn):", meanField( goldenCrossMovingUpQuotes, "Adj Close-130-PeriodForwardReturn" ), "\n",
                     "stdev(Adj Close-130-PeriodForwardReturn):", stdevField( goldenCrossMovingUpQuotes, "Adj Close-130-PeriodForwardReturn" ), "\n",
                     "mean(Adj Close-260-PeriodForwardReturn):", meanField( goldenCrossMovingUpQuotes, "Adj Close-260-PeriodForwardReturn" ), "\n",
                     "stdev(Adj Close-260-PeriodForwardReturn):", stdevField( goldenCrossMovingUpQuotes, "Adj Close-260-PeriodForwardReturn" ) )


#
# 
# starts with yahoo historical quote data:
#   {
#       "Date": "1992-07-20", 
#       "Symbol": "IBM", 
#       "_id": "IBM-1992-07-20", 
#       "Volume": "11625200", 
#       "Adj Close": "15.985412", 
#       "Open": "93.25", 
#       "Low": "92.75", 
#       "High": "93.375", 
#       "Close": "92.875"
#   }
# 
# ...and adds several fields:
#
#   {
#     "200-SimpleMovingAverage": 7.684316140000001,
#     "200-SimpleMovingAverage-1-PeriodForwardReturn": 0.0017045954072367185,
#     "200-SimpleMovingAverage-1-PeriodReturn": 0.0017397576985340132,
#     "50-SimpleMovingAverage": 9.013451719999999,
#     "50-SimpleMovingAverage-1-PeriodForwardReturn": 0.003490170134288966,
#     "50-SimpleMovingAverage-1-PeriodReturn": 0.003668210657789041,
#     "Adj Close": 9.482065,
#     "Adj Close-1-PeriodForwardReturn": 0.020344197176458887,
#     "Adj Close-1-PeriodReturn": 0.0031397360264661758,
#     "Adj Close-130-PeriodForwardReturn": 0.4892841380015851,
#     "Adj Close-130-PeriodReturn": 0.25940479518874016,
#     "Adj Close-20-PeriodForwardReturn": 0.04338949374424241,
#     "Adj Close-20-PeriodReturn": 0.07757167331005557,
#     "Adj Close-260-PeriodForwardReturn": 0.5973087085988126,
#     "Adj Close-260-PeriodReturn": 0.6373860576548657,
#     "Adj Close-5-PeriodForwardReturn": 0.06552201445571183,
#     "Adj Close-5-PeriodReturn": -0.03474310569327656,
#     "Adj Close-65-PeriodForwardReturn": 0.22677307105572458,
#     "Adj Close-65-PeriodReturn": 0.23565863268181308,
#     "Close": 79.875,
#     "Date": "1982-10-29",
#     "High": 80.5,
#     "Low": 79.125,
#     "Open": 79.875,
#     "Symbol": "IBM",
#     "Volume": 2825600,
#     "_id": "IBM-1982-10-29"
#   }
#   
# @return quotes
#
def computeMetaMetrics(quotes):

    # compute moving avgs and stuff...
    quotes = computeSimpleMovingAvg( 200, quotes )
    quotes = computeSimpleMovingAvg( 50, quotes )

    quotes = computePeriodicReturn( "200-SimpleMovingAverage", 1, quotes )
    quotes = computePeriodicReturn( "50-SimpleMovingAverage", 1, quotes )

    quotes = computePeriodicForwardReturn( "200-SimpleMovingAverage", 1, quotes )
    quotes = computePeriodicForwardReturn( "50-SimpleMovingAverage", 1, quotes )

    quotes = computePeriodicReturn( "Adj Close", 1, quotes )
    quotes = computePeriodicReturn( "Adj Close", 5, quotes )       # a week
    quotes = computePeriodicReturn( "Adj Close", 20, quotes )      # a month
    quotes = computePeriodicReturn( "Adj Close", 13*5, quotes )    # a quarter
    quotes = computePeriodicReturn( "Adj Close", 26*5, quotes )    # six months
    quotes = computePeriodicReturn( "Adj Close", 52*5, quotes )    # a year

    quotes = computePeriodicForwardReturn( "Adj Close", 1, quotes )
    quotes = computePeriodicForwardReturn( "Adj Close", 5, quotes )       # a week
    quotes = computePeriodicForwardReturn( "Adj Close", 20, quotes )      # a month
    quotes = computePeriodicForwardReturn( "Adj Close", 13*5, quotes )    # a quarter
    quotes = computePeriodicForwardReturn( "Adj Close", 26*5, quotes )    # six months
    quotes = computePeriodicForwardReturn( "Adj Close", 52*5, quotes )    # a year

    quotes = tagGoldenCrossEvents( quotes )

    return quotes


#
#   --symbol IBM 
#
def processHistoricalData(args):

    args = myutils.verifyArgs( args, required_args = [ '--symbol' ] )

    db = myutils.getMongoDb( os.environ["R4_MONGO_URI"] )

    quotes = db.quotes.find( { "Symbol": args["--symbol"] },
                             sort=[ ("_id", 1) ] )      # note: _id's are sorted by date


    quotes = computeMetaMetrics( list(quotes) )

    for quote in quotes:
        myutils.logTrace("processHistoricalData: ", json.dumps(quote, indent=2, sort_keys=True))


    analyzeGoldenCrosses( quotes )


#
#   --symbol IBM 
#
def playWithPandas(args):

    args = myutils.verifyArgs( args, required_args = [ '--symbol' ] )

    db = myutils.getMongoDb( os.environ["R4_MONGO_URI"] )

    quotes = db.quotes.find( { "Symbol": args["--symbol"] },
                             sort=[ ("_id", 1) ] )      # note: _id's are sorted by date

    quotes = computeMetaMetrics( list(quotes) )

    df = pandas.DataFrame(quotes)

    myutils.logTrace("playWithPandas: df:")
    myutils.logTrace(df)

    # df.describe(): basic column stats like mean and stdev
    myutils.logTrace("playWithPandas: df.describe():")
    myutils.logTrace(df.describe())

    # get a single column, returned as a "Series"
    myutils.logTrace("playWithPandas: df['Adj Close']:")
    myutils.logTrace(df['Adj Close'])

    # slice a few rows
    myutils.logTrace("playWithPandas: df[0:10]:")
    myutils.logTrace(df[0:10])

    myutils.logTrace("playWithPandas: df.loc[:,['Date','Close']]")
    myutils.logTrace( df.loc[:,['Date','Close']] )

    # df.at: fast access to scalar
    # df.iat: same as df.at, but only allows index notation (df.at allows row/column labels)
    myutils.logTrace("playWithPandas: df.at[8,'Adj Close']")
    myutils.logTrace(df.at[8,'Adj Close'])


    # iloc: select rows/cols by index
    #       df.iloc[3]
    #       df.iloc[3:7]
    #       df.iloc[[1,3,5],[0:2]]
    #       df.iloc[[True,True,False],[0:2]]
    myutils.logTrace("playWithPandas: df.iloc[[1,2,4],[0,2]]")
    myutils.logTrace(df.iloc[[1,2,4],[0,2]])

    # returns a Series of booleans
    # can be used for selection
    myutils.logTrace("playWithPandas: df['Date'] > '2016-01-01'")
    myutils.logTrace(df['Date'] > '2016-01-01')

    # select by boolean
    myutils.logTrace("playWithPandas: df[ df['Date'] > '2016-01-01' ] ")
    myutils.logTrace(df[ df['Date'] > '2016-01-01' ])

    # isin()
    myutils.logTrace("playWithPandas: df[ df['Date'].isin(['2016-01-04','2016-04-06']) ] ")
    myutils.logTrace(df[ df['Date'].isin(['2016-01-04','2016-04-06']) ])

    # isnull(), notnull(): return boolean series
    # df.mean(0): means of columns (default)
    # df.mean(1): means of rows
    # df.mean(0, skipna=True (default)): means of columns
    # df.sum(0)
    # z-scaling:  df_z = (df - df.mean()) / df.std()
    # http://pandas.pydata.org/pandas-docs/stable/basics.html#basics-stats

    myutils.logTrace("playWithPandas: df[ df['GoldenCross'] == True ]")
    goldenCrosses = df[ df['GoldenCross'] == True ]
    myutils.logTrace(goldenCrosses)

    myutils.logTrace( "playWithPandas: means, stdevs: ")
    myutils.logTrace( goldenCrosses.loc[:, ['Adj Close-130-PeriodForwardReturn', 'Adj Close-260-PeriodForwardReturn']].mean() )
    myutils.logTrace( goldenCrosses.loc[:, ['Adj Close-130-PeriodForwardReturn', 'Adj Close-260-PeriodForwardReturn']].std() )
    myutils.logTrace( goldenCrosses.loc[:, ['Adj Close-130-PeriodForwardReturn', 'Adj Close-260-PeriodForwardReturn']].std(ddof=0) )    # unbiased

    myutils.logTrace("playWithPandas: df[ (df['GoldenCross'] == True) & (df['200-SimpleMovingAverage-1-PeriodReturn'] > 0) & (df['50-SimpleMovingAverage-1-PeriodReturn'] > 0)]")
    goldenCrosses = df[ (df['GoldenCross'] == True) & (df['200-SimpleMovingAverage-1-PeriodReturn'] > 0) & (df['50-SimpleMovingAverage-1-PeriodReturn'] > 0)]

    myutils.logTrace( goldenCrosses )

    myutils.logTrace( "playWithPandas: means, stdevs: ")
    myutils.logTrace( goldenCrosses.loc[:, ['Adj Close-130-PeriodForwardReturn', 'Adj Close-260-PeriodForwardReturn']].mean() )
    myutils.logTrace( goldenCrosses.loc[:, ['Adj Close-130-PeriodForwardReturn', 'Adj Close-260-PeriodForwardReturn']].std() )
    myutils.logTrace( goldenCrosses.loc[:, ['Adj Close-130-PeriodForwardReturn', 'Adj Close-260-PeriodForwardReturn']].std(ddof=0) )    # unbiased

    myutils.logTrace("playWithPandas: statistics.pstdev: ", statistics.pstdev( goldenCrosses['Adj Close-260-PeriodForwardReturn'].tolist() ) )

    myutils.logTrace("playWithPandas: goldenCrosses.to_dict('records')")
    myutils.logTrace(json.dumps(goldenCrosses.to_dict('records'),indent=2))




#
# main entry point ---------------------------------------------------------------------------
# 
args = parseArgs()

#
#
#
if args["--action"] == "fetchYahooData":
    args = myutils.verifyArgs( args, required_args = [ '--sql' ] )
    r = fetchYahooData(args['--sql'])
    myutils.logTrace( "fetchYahooData:", json.dumps(r, indent=2, sort_keys=True) )

#
#
#
elif args["--action"] == "fetchYahooHistoricalDataCsv":
    args = myutils.setArgDefaultValue(args, '--startdate', '1950-01-01')
    args = myutils.setArgDefaultValue(args, '--enddate', date.today().strftime("%Y-%m-%d"))
    args = myutils.verifyArgs( args, required_args = [ '--symbol', '--startdate', '--enddate' ] )

    fetchYahooHistoricalDataCsv(args['--symbol'], 
                                datetime.strptime( args['--startdate'], "%Y-%m-%d"), 
                                datetime.strptime( args['--enddate'], "%Y-%m-%d") )

#
#
#
elif args["--action"] == "downloadYahooHistoricalData":
    downloadYahooHistoricalData(args)

#
#
#
elif args["--action"] == "processHistoricalData":
    processHistoricalData(args)

#
#
#
elif args["--action"] == "playWithPandas":
    playWithPandas(args)


#
# unrecognized
#
else:
    myutils.logError( "main: unrecognized --action:", args["--action"] )


