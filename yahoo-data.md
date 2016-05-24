
## Python Pandas

* Basic stats: [http://pandas.pydata.org/pandas-docs/stable/basics.html#basics-stats](http://pandas.pydata.org/pandas-docs/stable/basics.html#basics-stats)
* Indexing: [http://pandas.pydata.org/pandas-docs/stable/indexing.html](http://pandas.pydata.org/pandas-docs/stable/indexing.html)

.

    quotes = db.quotes.find( { "Symbol": args["--symbol"] },
                             sort=[ ("_id", 1) ] )      # note: _id's are sorted by date

    df = pandas.DataFrame(list(quotes))

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


## TODO

* NOTE: past market returns are biased!!
    * they don't incorporate FAILED businesses
    * only businesses that are still around are measured

* TODO: $ pip3 install TA-Lib 
    * NotImplementedError: cygwin
    * [http://mrjbq7.github.io/ta-lib/](http://mrjbq7.github.io/ta-lib/)
    * [http://mrjbq7.github.io/ta-lib/install.html](http://mrjbq7.github.io/ta-lib/install.html)
* TODO: python plotting
    * python vs r: [http://www.eickonomics.com/posts/2014-03-25-python-vs-R-adding-TA-indicators/](http://www.eickonomics.com/posts/2014-03-25-python-vs-R-adding-TA-indicators/)
* TODO: time-series correlations: [https://en.wikipedia.org/wiki/Autocorrelation](https://en.wikipedia.org/wiki/Autocorrelation)


--------------------------------------------------------------------------------------------------------------
## Stock Lists / Indexes

* amex.companylist.csv
* nasdaq.companylist.csv
* nyse.companylist.csv
* Market sector indices: http://www.nasdaq.com/markets/indices/sector-indices.aspx
* Major stock indices: http://www.nasdaq.com/markets/indices/major-indices.aspx
* ~4000 publicly traded companies on major exchanges; ~15000 trade on pink sheets
    * [http://www.businessinsider.com/us-has-too-few-publicly-listed-companies-2015-6](http://www.businessinsider.com/us-has-too-few-publicly-listed-companies-2015-6)
* Russell 3000: (^RUA) 3000 largest, cap-weighted. 98% of the american market
* Russell 2000: (^RUT) 2000 lowest in the Russell 3000.  "Small-cap"
* Russell 1000: (^RUI) Top 1000 of Russell 3000.  90% of equity market.
* Russell has like 1800+ indices, covering stocks across the globe
* S&P 500: (^GSPC) 500 largest by market cap.  "Large-cap".


--------------------------------------------------------------------------------------------------------------
## Downloading data

* idempotency!
* download quotes/quotelist data daily
    * quotes contains a lot more than the historical end-of-day data
    * can only get this info on the day of.  No historical data
    * DOES NOT include ADJ CLOSE! so the data becomes stale after a corp action (dividend, e.g.)
        * so may not want to bother with the daily data at all
* historical data
    * download any time - won't overwrite any other field
* computing add'l data (e.g. moving avgs, future/past prices)
    * idempotent operations
* Adj_close will change for ALL historical data when..
    * stock splits
    * pays a dividend
    * mergers and other corp actions
    * so need to update all my historical data
    * including computed data (moving avgs, etc)
* yahoo limits: 1000-2000 requests/hr



--------------------------------------------------------------------------------------------------------------
## Technical data to collect / process

* Eod data
* moving avgs
    * 20, 50, 100, 200
* moving avg derivatives
    * capture this with +/- 1 past/future value
* price derivatives
    * from prev day
    * to next day
    * could capture this instead by including +/- 1 past/future price
* past and future prices
    * +/- 5, 20 (1mo), 65 (3mo), 130 (6mo), 260 (1yr)
* short interest
* macd 
    * and other indicators
* golden cross markets
    * in a "tags" field?
    * other one-off events?
    * earnings reporting dates
    * macro news day events 
        * unemployment report
        * quarterly GDP
        * FED open market operations committee
        * NOTE: macro news dates are the same for ALL companies
            * whereas golden cross, earnings dates are company specific.
            * so 



--------------------------------------------------------------------------------------------------------------
## API: query.yahooapis.com:


    http://query.yahooapis.com/v1/public/yql?
                env=http://datatables.org/alltables.env
                format=json
                q=<query>


NOTE: data delayed 15 mins

### yahoo.finance.quotes

* Instant quote info. 
* Data delayed 15 mins.  
* includes PE ratio, PriceBook, etc.

Example: 

    $ ./runquery.py  --action fetchYahooData --sql 'select * from yahoo.finance.quotes where symbol in ("IBM")'
    main: verified args= {'--action': 'fetchYahooData', '--sql': 'select * from yahoo.finance.quotes where symbol in ("IBM")'}
    fetchYahooData: {
      "query": {
        "count": 1,
        "created": "2016-05-10T06:22:52Z",
        "lang": "en-US",
        "results": {
          "quote": {
            "AfterHoursChangeRealtime": null,
            "AnnualizedGain": null,
            "Ask": "147.31",
            "AskRealtime": null,
            "AverageDailyVolume": "4732730",
            "Bid": "147.10",
            "BidRealtime": null,
            "BookValue": "14.77",
            "Change": "+0.05",
            "ChangeFromFiftydayMovingAverage": "-1.21",
            "ChangeFromTwoHundreddayMovingAverage": "9.19",
            "ChangeFromYearHigh": "-27.10",
            "ChangeFromYearLow": "30.44",
            "ChangePercentRealtime": null,
            "ChangeRealtime": null,
            "Change_PercentChange": "+0.05 - +0.03%",
            "ChangeinPercent": "+0.03%",
            "Commission": null,
            "Currency": "USD",
            "DaysHigh": "148.20",
            "DaysLow": "147.01",
            "DaysRange": "147.01 - 148.20",
            "DaysRangeRealtime": null,
            "DaysValueChange": null,
            "DaysValueChangeRealtime": null,
            "DividendPayDate": "3/10/2016",
            "DividendShare": "5.60",
            "DividendYield": "3.80",
            "EBITDA": "20.08B",
            "EPSEstimateCurrentYear": "13.53",
            "EPSEstimateNextQuarter": "3.32",
            "EPSEstimateNextYear": "14.14",
            "EarningsShare": "13.42",
            "ErrorIndicationreturnedforsymbolchangedinvalid": null,
            "ExDividendDate": "5/6/2016",
            "FiftydayMovingAverage": "148.55",
            "HighLimit": null,
            "HoldingsGain": null,
            "HoldingsGainPercent": null,
            "HoldingsGainPercentRealtime": null,
            "HoldingsGainRealtime": null,
            "HoldingsValue": null,
            "HoldingsValueRealtime": null,
            "LastTradeDate": "5/9/2016",
            "LastTradePriceOnly": "147.34",
            "LastTradeRealtimeWithTime": null,
            "LastTradeTime": "4:02pm",
            "LastTradeWithTime": "4:02pm - <b>147.34</b>",
            "LowLimit": null,
            "MarketCapRealtime": null,
            "MarketCapitalization": "141.58B",
            "MoreInfo": null,
            "Name": "International Business Machines",
            "Notes": null,
            "OneyrTargetPrice": "144.05",
            "Open": "147.70",
            "OrderBookRealtime": null,
            "PEGRatio": "4.09",
            "PERatio": "10.98",
            "PERatioRealtime": null,
            "PercebtChangeFromYearHigh": "-15.54%",
            "PercentChange": "+0.03%",
            "PercentChangeFromFiftydayMovingAverage": "-0.82%",
            "PercentChangeFromTwoHundreddayMovingAverage": "+6.65%",
            "PercentChangeFromYearLow": "+26.04%",
            "PreviousClose": "147.29",
            "PriceBook": "9.97",
            "PriceEPSEstimateCurrentYear": "10.89",
            "PriceEPSEstimateNextYear": "10.42",
            "PricePaid": null,
            "PriceSales": "1.73",
            "SharesOwned": null,
            "ShortRatio": "4.66",
            "StockExchange": "NYQ",
            "Symbol": "IBM",
            "TickerTrend": null,
            "TradeDate": null,
            "TwoHundreddayMovingAverage": "138.15",
            "Volume": "4302433",
            "YearHigh": "174.44",
            "YearLow": "116.90",
            "YearRange": "116.90 - 174.44",
            "symbol": "IBM"
          }
        }
      }
    }


### yahoo.finance.quoteslist

* Instant quote info. 
* pretty much same as yahoo.finance.quotes, just less info.
* Data delayed 15 mins.  
* includes open, high, low, lastTradeTime

Example: 

    $ ./runquery.py  --action fetchYahooData --sql 'select * from yahoo.finance.quoteslist where symbol in ("IBM")'
    main: verified args= {'--action': 'fetchYahooData', '--sql': 'select * from yahoo.finance.quoteslist where symbol in ("IBM")'}
    fetchYahooData: {
      "query": {
        "count": 1,
        "created": "2016-05-10T06:23:50Z",
        "lang": "en-US",
        "results": {
          "quote": {
            "Change": "+0.05",
            "DaysHigh": "148.20",
            "DaysLow": "147.01",
            "LastTradeDate": "5/9/2016",
            "LastTradePriceOnly": "147.34",
            "LastTradeTime": "4:02pm",
            "Open": "147.70",
            "Symbol": "IBM",
            "Volume": "4302433",
            "symbol": "IBM"
          }
        }
      }
    }
    

### yahoo.finance.historicaldata

* Historical quotes
* open, high, low, close, volume

Example: 

    $ ./runquery.py  --action fetchYahooData --sql 'select * from yahoo.finance.historicaldata where startDate="2016-04-25" and endDate="2016-05-01" and symbol="IBM"'
    main: verified args= {'--action': 'fetchYahooData', '--sql': 'select * from yahoo.finance.historicaldata where startDate="2016-04-25" and endDate="2016-05-01" and symbol="IBM"'}
    fetchYahooData: {
      "query": {
        "count": 5,
        "created": "2016-05-10T06:30:06Z",
        "lang": "en-US",
        "results": {
          "quote": [
            {
              "Adj_Close": "144.54507",
              "Close": "145.940002",
              "Date": "2016-04-29",
              "High": "147.339996",
              "Low": "144.190002",
              "Open": "146.490005",
              "Symbol": "IBM",
              "Volume": "4225800"
            },
            {
              "Adj_Close": "145.664274",
              "Close": "147.070007",
              "Date": "2016-04-28",
              "High": "150.179993",
              "Low": "146.729996",
              "Open": "149.75",
              "Symbol": "IBM",
              "Volume": "3791500"
            },
            {
              "Adj_Close": "149.03177",
              "Close": "150.470001",
              "Date": "2016-04-27",
              "High": "150.779999",
              "Low": "148.970001",
              "Open": "149.350006",
              "Symbol": "IBM",
              "Volume": "3111200"
            },
            {
              "Adj_Close": "147.655056",
              "Close": "149.080002",
              "Date": "2016-04-26",
              "High": "149.789993",
              "Low": "147.899994",
              "Open": "148.649994",
              "Symbol": "IBM",
              "Volume": "2979800"
            },
            {
              "Adj_Close": "147.387633",
              "Close": "148.809998",
              "Date": "2016-04-25",
              "High": "148.899994",
              "Low": "147.110001",
              "Open": "148.160004",
              "Symbol": "IBM",
              "Volume": "2848900"
            }
          ]
        }
      }
    }




### yahoo.finance.balancesheet

* nothing there

Example: 

    $ ./runquery.py  --action fetchYahooData --sql 'select * from yahoo.finance.balancesheet where symbol="IBM"'



### yahoo.finance.dividendhistory

* dividends

Example: 

    $ ./runquery.py  --action fetchYahooData --sql 'select * from yahoo.finance.dividendhistory where symbol = "IBM" and startDate = "1952-01-01" and endDate = "2013-12-31"'
    main: verified args= {'--sql': 'select * from yahoo.finance.dividendhistory where symbol = "IBM" and startDate = "1952-01-01" and endDate = "2013-12-31"', '--action': 'fetchYahooData'}
    fetchYahooData: {
        "query": {
            "count":215,
            "created":"2016-05-10T05:34:58Z",
            "lang":"en-US",
            "results": {
                "quote":[ {
                    "Symbol":"IBM",
                    "Date":"2016-05-06",
                    "Dividends":"1.400000"
                }, {
                    "Symbol":"IBM",
                    "Date":"2016-02-08",
                    "Dividends":"1.300000"
                },{
                    "Symbol":"IBM",
                    "Date":"2015-11-06",
                    "Dividends":"1.300000"
                }, {
                    "Symbol":"IBM",
                    "Date":"2015-08-06",
                    "Dividends":"1.300000"
                },{
                    ...
                }]
            }
        }
    }

### yahoo.finance.industry

* list of companies in each industry
* need to use industry IDs: [https://biz.yahoo.com/ic/ind_index.html](https://biz.yahoo.com/ic/ind_index.html)

Example: 

    $ ./runquery.py  --action fetchYahooData --sql 'select * from yahoo.finance.industry where id="112"'
    main: verified args= {'--action': 'fetchYahooData', '--sql': 'select * from yahoo.finance.industry where id="112"'}
    fetchYahooData: {
        "query":{
            "count":1,
            "created":"2016-05-10T05:48:44Z",
            "lang":"en-US",
            "results":{
                "industry":{
                    "id":"112",
                    "name":"",
                    "company":[{
                        "name":"Abundant\nProduce Ltd",
                        "symbol":"ABT.AX"
                    },{
                        "name":"Adarsh\nPlant Protect Ltd",
                        "symbol":"ADARSHPL.BO"
                    },{
                        "name":"African\nPotash Ltd",
                        "symbol":"AFPO.L"
                    },{
                        "name":"Agri-Tech\n(India) Ltd",
                        "symbol":"AGRITECH.NS"
                    },{
                        "name":"Agrium\nInc",
                        "symbol":"AGU.DE"
                    },{
                        "name":"Agrium\nInc",
                        "symbol":"AGU.TO"
                    },


### yahoo.finance.isin

?

    $ ./runquery.py  --action fetchYahooData --sql 'select * from yahoo.finance.isin where symbol in ("US9843321061")'
    main: verified args= {'--action': 'fetchYahooData', '--sql': 'select * from yahoo.finance.isin where symbol in ("US9843321061")'}
    fetchYahooData: {
      "query": {
        "count": 1,
        "created": "2016-05-10T06:41:35Z",
        "lang": "en-US",
        "results": {
          "stock": {
            "Isin": "YHO.DE",
            "symbol": "US9843321061"
          }
        }
      }
    }


### others

The following don't seem to return anything:

    $ ./runquery.py  --action fetchYahooData --sql 'SELECT * FROM yahoo.finance.keystats WHERE symbol="IBM"'
    fetchYahooData: {
      "query": {
        "count": 1,
        "created": "2016-05-10T06:10:16Z",
        "lang": "en-US",
        "results": {
          "stats": {
            "symbol": "IBM"
          }
        }
      }
    }
    
    
    
    $ ./runquery.py  --action fetchYahooData --sql 'select * from yahoo.finance.onvista where symbol in ("DE0005200000")'
    main: verified args= {'--action': 'fetchYahooData', '--sql': 'select * from yahoo.finance.onvista where symbol in ("DE0005200000")'}
    fetchYahooData: {
      "query": {
        "count": 1,
        "created": "2016-05-10T06:12:50Z",
        "lang": "en-US",
        "results": {
          "stock": {
            "Analysts": null,
            "Confirmation": null,
            "Downgrade": null,
            "EbitMarge": null,
            "EquityRatio": null,
            "PER1": null,
            "PER2": null,
            "PER3": null,
            "PER4": null,
            "PER5": null,
            "Upgrade": null,
            "symbol": "DE0005200000"
          }
        }
      }
    }
    
    $ ./runquery.py  --action fetchYahooData --sql 'SELECT * FROM yahoo.finance.option_contracts WHERE ticker="YHOO"'
    $ ./runquery.py  --action fetchYahooData --sql 'SELECT * FROM yahoo.finance.option_contracts WHERE symbol="DNKN160916P00040000"'
    $ ./runquery.py  --action fetchYahooData --sql 'SELECT * FROM yahoo.finance.option_contracts WHERE symbol="YHOO"'
    main: verified args= {'--action': 'fetchYahooData', '--sql': 'SELECT * FROM yahoo.finance.option_contracts WHERE symbol="YHOO"'}
    fetchYahooData: {
      "query": {
        "count": 1,
        "created": "2016-05-10T06:15:25Z",
        "lang": "en-US",
        "results": {
          "option": {
            "symbol": "YHOO"
          }
        }
      }
    }
    
    
    $ ./runquery.py  --action fetchYahooData --sql 'SELECT * FROM yahoo.finance.options WHERE symbol="DNKN160916P00040000"'
    $ ./runquery.py  --action fetchYahooData --sql 'SELECT * FROM yahoo.finance.options WHERE symbol="GOOG" AND expiration="2016-05"'
    main: verified args= {'--action': 'fetchYahooData', '--sql': 'SELECT * FROM yahoo.finance.options WHERE symbol="GOOG" AND expiration="2016-05"'}
    fetchYahooData: {
      "query": {
        "count": 1,
        "created": "2016-05-10T06:16:47Z",
        "lang": "en-US",
        "results": {
          "optionsChain": {
            "expiration": "2016-05",
            "symbol": "GOOG"
          }
        }
      }
    }
    
    
    $ ./runquery.py  --action fetchYahooData --sql 'SELECT * FROM yahoo.finance.quant WHERE symbol="GOOG"'
    main: verified args= {'--action': 'fetchYahooData', '--sql': 'SELECT * FROM yahoo.finance.quant WHERE symbol="GOOG"'}
    fetchYahooData: {
      "query": {
        "count": 1,
        "created": "2016-05-10T06:17:52Z",
        "lang": "en-US",
        "results": {
          "stock": {
            "Analysts": null,
            "CompanyName": null,
            "EarningsGrowth": null,
            "EbitMarge": null,
            "FourMonthsAgo": null,
            "LastMonth": null,
            "LastYear": null,
            "ReturnOnEquity": null,
            "SixMonths": null,
            "Stockholders": null,
            "ThreeMonthsAgo": null,
            "Today": null,
            "TotalAssets": null,
            "TrailingPE": null,
            "TwoMonthsAgo": null,
            "symbol": "GOOG"
          }
        }
      }
    }
    
    
    $ ./runquery.py  --action fetchYahooData --sql 'SELECT * FROM yahoo.finance.quant2 WHERE symbol="GOOG"'
    main: verified args= {'--action': 'fetchYahooData', '--sql': 'SELECT * FROM yahoo.finance.quant2 WHERE symbol="GOOG"'}
    fetchYahooData: {
      "query": {
        "count": 1,
        "created": "2016-05-10T06:18:40Z",
        "lang": "en-US",
        "results": {
          "stock": {
            "FourMonthsAgo": null,
            "LastMonth": null,
            "ThreeMonthsAgo": null,
            "TwoMonthsAgo": null,
            "symbol": "GOOG"
          }
        }
      }
    }


    $ ./runquery.py  --action fetchYahooData --sql 'SELECT * FROM yahoo.finance.sectors'


    $ ./runquery.py  --action fetchYahooData --sql 'SELECT * FROM yahoo.finance.stocks WHERE symbol="GOOG"'
    main: verified args= {'--sql': 'SELECT * FROM yahoo.finance.stocks WHERE symbol="GOOG"', '--action': 'fetchYahooData'}
    fetchYahooData: {
      "query": {
        "count": 1,
        "created": "2016-05-10T06:20:34Z",
        "lang": "en-US",
        "results": {
          "stock": {
            "CompanyName": null,
            "end": "2016-05-10",
            "start": "2004-08-19",
            "symbol": "GOOG"
          }
        }
      }
    }




                   
-----------------------------------------------------------------------------------------------------
## API: finance.yahoo.com

Note: this is pretty much the same data as the above JSON yahooapi.

http://wern-ancheta.com/blog/2015/04/05/getting-started-with-the-yahoo-finance-api/
http://www.jarloo.com/yahoo_finance/

http://finance.yahoo.com/d/quotes.csv?s=GE+PTR+MSFT&f=snd1l1yr
    f= data prescription

http://finance.yahoo.com/webservice/v1/symbols/YHOO,AAPL/quote?format=json&view=detail
{
    "list" : { 
        "meta" : { 
            "type" : "resource-list",
            "start" : 0,
            "count" : 2
        },
        "resources" : [ 
        {
            "resource" : { 
                "classname" : "Quote",
                "fields" : { 
                    "change" : "-0.520000",
                    "chg_percent" : "-1.423489",
                    "day_high" : "36.410000",
                    "day_low" : "35.910000",
                    "issuer_name" : "Yahoo! Inc.",
                    "issuer_name_lang" : "Yahoo! Inc.",
                    "name" : "Yahoo! Inc.",
                    "price" : "36.009998",
                    "symbol" : "YHOO",
                    "ts" : "1462305600",
                    "type" : "equity",
                    "utctime" : "2016-05-03T20:00:00+0000",
                    "volume" : "9087248",
                    "year_high" : "45.070000",
                    "year_low" : "26.150000"
                }
            }
        }
        ,
            {
                "resource" : { 
                    "classname" : "Quote",
                    "fields" : { 
                        "change" : "1.540001",
                        "chg_percent" : "1.644597",
                        "day_high" : "95.739998",
                        "day_low" : "93.680000",
                        "issuer_name" : "Apple Inc.",
                        "issuer_name_lang" : "Apple Inc.",
                        "name" : "Apple Inc.",
                        "price" : "95.180000",
                        "symbol" : "AAPL",
                        "ts" : "1462305600",
                        "type" : "equity",
                        "utctime" : "2016-05-03T20:00:00+0000",
                        "volume" : "56779285",
                        "year_high" : "132.970000",
                        "year_low" : "92.000000"
                    }
                }
            }

        ]
    }
}




-----------------------------------------------------------------------------------------------------
## API: ichart.finance.yahoo.com

* Historical data in csv
* [http://ichart.finance.yahoo.com/table.csv?s=WU&a=01&b=19&c=2010&d=01&e=19&f=2010&g=d&ignore=.csv](http://ichart.finance.yahoo.com/table.csv?s=WU&a=01&b=19&c=2010&d=01&e=19&f=2010&g=d&ignore=.csv)
    * startdate=a+1/b/c
    * enddate=d+1/e/f
* [http://real-chart.finance.yahoo.com/table.csv?s=IBM&d=4&e=3&f=2016&g=d&a=0&b=2&c=1962&ignore=.csv](http://real-chart.finance.yahoo.com/table.csv?s=IBM&d=4&e=3&f=2016&g=d&a=0&b=2&c=1962&ignore=.csv)
    * startdate=a+1/b/c
    * enddate=d+1/e/f

.

    $ ./runquery.pl --action downloadYahooHistoricalData --symbol IBM 
    $ ./runquery.pl --action downloadYahooHistoricalData --symbol IBM --startdate 1950-01-01
    $ ./runquery.pl --action downloadYahooHistoricalData --symbol IBM --startdate 2016-04-25 --enddate 2016-05-01

    $ ./runquery.pl --action processHistoricalData --symbol IBM 




-----------------------------------------------------------------------------------------------------
## TA-Lib Technical Analysis Indicators


### Retracement vs Reversal Indicators

* Volume
    * Retracement: small lots (retail traders)
    * Reversal: large lots (institutional traders)
* Money Flow
    * Retracement: buying interest during decline
    * Reversal: little buying interest
* Chart Patterns
    * Retracement: few reversal patterns.  maybe some candles
    * Reversal: several reversal patterns, usually chart patterns, e.g. double top
* Short interest
    * Retracement: no change
    * Reversal: increasing short interest
* Time Frame
    * Retracement: short-term reversal, no longer than 1 - 2 weeks
    * Reversal: long-term reversal, lasts longer than 2 weeks
* Fundamentals
    * Retracement: no change
    * Reversal: change or speculation of change in fundamentals
* Recent Activity:
    * Retracement: usually occurs right after large gains
    * Reversal: can happen any time
* Candlesticks:
    * Retracement: "indecision candles": typically have long tops and bottoms (e.g. spinning tops)
    * Reversal: reversal candles, e.g engulfings, soldiers, etc



### Overlap Studies

* BBANDS: Bollinger Bands
    * volatility indicator
    * N-period moving average (MA) 
        * default: N=20
        * default: simple moving average
        * "middleBB"
    * upper band, "upperBB": MA + K * stdev(MA)    
        * default K=2
    * lower band, "lowerBB": MA - K * stdev(MA)
    * %b = (last-lowerBB) / (upperBB/lowerBB)
        * relative position within the band
    * bandwidth = (upperBB-lowerBB)/middleBB
        * normalized width of band
        * for direct comparison with other assets
        * bandwidth = (2*stdev(middleBB) - (-2*stdev(moddleBB)))/middleBB = 4*stdev(middleBB)/middleBB = 2*K*stdev(middleBB)/middleBB
    * strategy:
        * bands close together: low volatility
        * bands far apart: high volatility
        * buy when price touches/crosses lower band
        * sell when price touches/crosses higher band
        * sell options when bands are historically far apart
        * buy options when bands are historically close together
            * expecting volatility to regress to normal
        * confirm price action when combined with other indicators
    * studies:
        * no benefit over buy and hold
        * "contrarian bollinger bands": produced some positive results
* DEMA: Double Exponential Moving Average
    * attempts to minimize the lag associated with moving averages
    * DEMA = 2*EMA - EMA(EMA)
        * EMA(EMA) removes the lag and accounts for the doubling of the EMA
* EMA: Exponential Moving Average
    * "weighted" moving average
    * S1 = Y1
    * St = alpha * Yt + (1-alpha) * St-1
        * alpha: weighting factor
    * EMAtoday = EMAyesterday + alpha * (Ytoday - EMAyesterday)
* SMMA: Smoothed Moving Average (not in TA_Lib)
    * aka Modified Moving Average
    * aka Running Moving Average
    * SMMA = EMA with alpha = 1/N
* HT_TRENDLINE         Hilbert Transform - Instantaneous Trendline
    * like a moving average, but with minimal lag
* KAMA                 Kaufman Adaptive Moving Average
* MA                   Moving average
* MAMA                 MESA Adaptive Moving Average
* MAVP                 Moving average with variable period
* MIDPOINT             MidPoint over period
* MIDPRICE             Midpoint Price over period
* SAR                  Parabolic SAR
* SAREXT               Parabolic SAR - Extended
* SMA                  Simple Moving Average
* T3                   Triple Exponential Moving Average (T3)
* TEMA                 Triple Exponential Moving Average
* TRIMA                Triangular Moving Average
* WMA                  Weighted Moving Average


### Momentum Indicators

* ADX: Average Directional Movement Index
    * "Trend strength indicator"
    * used to determine when price is trending strongly
    * THE ULTIMATE TREND INDICATOR
    * ADX is bi-directional
        * measures abs value of trend strength, up or down
        * values: 0 to 100
            * 0-25: weak trend
                * if ADX below 25 for more than 30 bars...
                * price enters trading range conditions
                * combine with candlestick patterns to anticipate breakouts
                * confirm with rising ADX
            * 25-50: strong trend
            * 50-75: very strong trend
            * 75-100: extremely strong trend
    * Plotted with two DMI (Directional Movement Indicators)
        * "upmove": High_today - High_yesterday
        * "downmove": Low_yesterday - Low_today
        * if (upmove > 0 AND upmove > downmove)
            * then: +DM = upmove
            * else: +DM = 0
        * if (downmove > 0 AND downmove > upmove)
            * then: -DM = downmove
            * else: -DM = 0
        * \+DMI = 100 * SMMA(+DM) / average-true-range
        * \-DMI = 100 * SMMA(-DM) / average-true-range
        * SMMA = smoothed moving average
    * ADX=  100 * SMMA( +DI - -DI / +DI + -DI )
    * default N=14 (for SMMA)
    * Strategy: Elder:
        * buy: ADX peaks and starts to decline
        * sell: ADX stops falling and goes flat
* ADXR: Average Directional Movement Index Rating
    * average of two ADX periods
    * ADXR = (ADX_i - ADX_i-n) / 2
    * n = period of ADX SMMA (default=14)
    * smoothes the ADX
* APO                  Absolute Price Oscillator
* AROON                Aroon
* AROONOSC             Aroon Oscillator
* BOP                  Balance Of Power
* CCI                  Commodity Channel Index
* CMO                  Chande Momentum Oscillator
* DX                   Directional Movement Index
* MACD                 Moving Average Convergence/Divergence
* MACDEXT              MACD with controllable MA type
* MACDFIX              Moving Average Convergence/Divergence Fix 12/26
* MFI                  Money Flow Index
    * volume-weighted RSI
    * typical price = (High + Low + Close) / 3
    * raw money flow = typical price * volume
        * positive when typical price_today > typical price_yesterday
        * negative when typical price_today < typical price_yesterday
    * money flow ratio = (14-period positive money flow) / (14-period negative money flow)
    * money flow index = 100 - 100 / (1 + money flow ratio)
    * alternatively: money flow index = 100 * positive money flow / (positive + negative money flow)
        * i.e. the proporition of money flow thats positive
    * strategy: indicates overbought and oversold conditions
        * MFI > 80 = overbought
            * 80+% of money flow has been positive
        * MFI < 20 = oversold
            * 80+% of money flow has been negative
    * strategy: divergence: 
        * asset makes higher high
        * but MFI makes lower high
        * could signal reversal
        * and vice-versa
* MINUS_DI             Minus Directional Indicator
* MINUS_DM             Minus Directional Movement
* MOM                  Momentum
* PLUS_DI              Plus Directional Indicator
* PLUS_DM              Plus Directional Movement
* PPO                  Percentage Price Oscillator
* ROC                  Rate of change : ((price/prevPrice)-1)*100
* ROCP                 Rate of change Percentage: (price-prevPrice)/prevPrice
* ROCR                 Rate of change ratio: (price/prevPrice)
* ROCR100              Rate of change ratio 100 scale: (price/prevPrice)*100
* RSI                  Relative Strength Index
    * upday = Close_today - Close_yesterday, if Close_today > Close_yesterday, else 0
    * downday = Close_today - Close_yesterday, if Close_today < Close_yesterday, else 0
    * RS = SMMMA( updays, n ) / SMMA( downdays, n )
        * RS > 1 if SMMA(updays) > SMMA(downdays)
            * positive momentum
        * RS = 1 if SMMA(updays) == SMMA(downdays)
            * sideways
        * RS < 1 if SMMA(updays) < SMMA(downdays)
            * negative momentum
    * RSI = 100 - 100 / (1 + RS)
    * alternatively: RSI = 100 * SMMA(updays) / SMMA(updays) + SMMA(downdays)
        * proportion of updays relative to downdays
    * strategy: overbought/oversold
        * RSI > 80 = overbought
        * RSI < 20 = oversold
    * strategy: divergence
        * bearish: price makes new high but RSI makes lower high
        * bullish: price makes new low but RSI makes higher low
* STOCH: Stochastic (Oscillator?)
    * %K = 100 * (Close_today - Low_n) / (High_n - Low_n)
    * n = number of trading periods (default = 14)
    * measures where today's close is,
        * relative to the trading range over the last n periods
    * %D = 3-day moving average of %K
    * transaction signals when %K crosses %D
    * %K > 80 
        * if Close_today is near the high for the trading range
    * %K < 20
        * if Close_today is near the low of the trading range
* STOCHF               Stochastic Fast
* STOCHRSI             Stochastic Relative Strength Index
* TRIX                 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
* ULTOSC               Ultimate Oscillator
* WILLR                Williams' %R


### Volume Indicators

* AD                   Chaikin A/D Line
* ADOSC                Chaikin A/D Oscillator
* OBV                  On Balance Volume

### Cycle Indicators

* HT_DCPERIOD          Hilbert Transform - Dominant Cycle Period
* HT_DCPHASE           Hilbert Transform - Dominant Cycle Phase
* HT_PHASOR            Hilbert Transform - Phasor Components
* HT_SINE              Hilbert Transform - SineWave
* HT_TRENDMODE         Hilbert Transform - Trend vs Cycle Mode

### Price Transform

* AVGPRICE             Average Price
* MEDPRICE             Median Price
* TYPPRICE             Typical Price
* WCLPRICE             Weighted Close Price

### Volatility Indicators

* ATR: Average True Range 
    * N-day SMMA of "true range" values
    * "true range"
        * High - Low
        * takes into account yesterday's close
            * if it's outside today's High-Low range
* NATR                 Normalized Average True Range
* TRANGE               True Range


### Pattern Recognition

* CDL2CROWS            Two Crows
* CDL3BLACKCROWS       Three Black Crows
* CDL3INSIDE           Three Inside Up/Down
* CDL3LINESTRIKE       Three-Line Strike
* CDL3OUTSIDE          Three Outside Up/Down
* CDL3STARSINSOUTH     Three Stars In The South
* CDL3WHITESOLDIERS    Three Advancing White Soldiers
* CDLABANDONEDBABY     Abandoned Baby
* CDLADVANCEBLOCK      Advance Block
* CDLBELTHOLD          Belt-hold
* CDLBREAKAWAY         Breakaway
* CDLCLOSINGMARUBOZU   Closing Marubozu
* CDLCONCEALBABYSWALL  Concealing Baby Swallow
* CDLCOUNTERATTACK     Counterattack
* CDLDARKCLOUDCOVER    Dark Cloud Cover
* CDLDOJI              Doji
* CDLDOJISTAR          Doji Star
* CDLDRAGONFLYDOJI     Dragonfly Doji
* CDLENGULFING         Engulfing Pattern
* CDLEVENINGDOJISTAR   Evening Doji Star
* CDLEVENINGSTAR       Evening Star
* CDLGAPSIDESIDEWHITE  Up/Down-gap side-by-side white lines
* CDLGRAVESTONEDOJI    Gravestone Doji
* CDLHAMMER            Hammer
* CDLHANGINGMAN        Hanging Man
* CDLHARAMI            Harami Pattern
* CDLHARAMICROSS       Harami Cross Pattern
* CDLHIGHWAVE          High-Wave Candle
* CDLHIKKAKE           Hikkake Pattern
* CDLHIKKAKEMOD        Modified Hikkake Pattern
* CDLHOMINGPIGEON      Homing Pigeon
* CDLIDENTICAL3CROWS   Identical Three Crows
* CDLINNECK            In-Neck Pattern
* CDLINVERTEDHAMMER    Inverted Hammer
* CDLKICKING           Kicking
* CDLKICKINGBYLENGTH   Kicking - bull/bear determined by the longer marubozu
* CDLLADDERBOTTOM      Ladder Bottom
* CDLLONGLEGGEDDOJI    Long Legged Doji
* CDLLONGLINE          Long Line Candle
* CDLMARUBOZU          Marubozu
* CDLMATCHINGLOW       Matching Low
* CDLMATHOLD           Mat Hold
* CDLMORNINGDOJISTAR   Morning Doji Star
* CDLMORNINGSTAR       Morning Star
* CDLONNECK            On-Neck Pattern
* CDLPIERCING          Piercing Pattern
* CDLRICKSHAWMAN       Rickshaw Man
* CDLRISEFALL3METHODS  Rising/Falling Three Methods
* CDLSEPARATINGLINES   Separating Lines
* CDLSHOOTINGSTAR      Shooting Star
* CDLSHORTLINE         Short Line Candle
* CDLSPINNINGTOP       Spinning Top
* CDLSTALLEDPATTERN    Stalled Pattern
* CDLSTICKSANDWICH     Stick Sandwich
* CDLTAKURI            Takuri (Dragonfly Doji with very long lower shadow)
* CDLTASUKIGAP         Tasuki Gap
* CDLTHRUSTING         Thrusting Pattern
* CDLTRISTAR           Tristar Pattern
* CDLUNIQUE3RIVER      Unique 3 River
* CDLUPSIDEGAP2CROWS   Upside Gap Two Crows
* CDLXSIDEGAP3METHODS  Upside/Downside Gap Three Methods

