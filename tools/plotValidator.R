library(RPostgres)

#connect to timescaledb
con <- dbConnect(RPostgres::Postgres(), dbname = "postgres",
                 host = "192.168.2.8",
                 user = "postgres",
                 password = "password")

#declare fibonacci levels
fR <- data.frame(
  retracement = c(1.618,1.382,1.236,1,0.786,
                  0.618,0.5,0.382,0.236,0),
  lineColor = c('red', 'blue', 'green',
                'yellow', 'brown', 'turquoise3',
                'orange', 'purple', 
                'violet', 'goldenrod1')
)
fR$fibLevel <- NA
fR$southLevel <- NA
fR$northLevel <- NA

#get list of buy advice instances
sqlQuery <- dbSendQuery(con, "SELECT * FROM table001 
                     WHERE resultpercent IS NOT NULL
                        and fiblevel >= 1;")
validated <- dbFetch(sqlQuery)
dbClearResult(sqlQuery)

for (i in 1:nrow(validated)){
  # get plot data
  sqlString <-  paste("select * from table001 
  where symbol like '", validated$symbol[i],"' 
  and id >= '", validated$startid[i], "' 
  and id <= '", validated$stopid[i] + 30000, "';", sep = "")
  sqlQuery <- dbSendQuery(con, sqlString)
  plotData <- dbFetch(sqlQuery)
  dbClearResult(sqlQuery)
  
  # get stopid time
  sqlString <-  paste("select time from table001 
  where id = '", validated$stopid[i], "';", sep = "")
  sqlQuery <- dbSendQuery(con, sqlString)
  stopIdTime <- dbFetch(sqlQuery)
  dbClearResult(sqlQuery)
  
  # re-engineer data present at point of making decision
  sqlString <-  paste("select * from table001 
  where symbol like '", validated$symbol[i],"'
  and id >= '", validated$startid[i], "'
  and id <= '", validated$stopid[i], "';", sep = "")
  sqlQuery <- dbSendQuery(con, sqlString)
  largeData <- dbFetch(sqlQuery)
  dbClearResult(sqlQuery)
  
  #get change
  change <- as.numeric(max(largeData$askprice)) - 
    as.numeric(min(largeData$askprice))
  
  for (fiblvl in 0:nrow(fR)){
    fR$fibLevel[fiblvl] <- as.numeric(max(largeData$askprice)) - 
      change * fR$retracement[fiblvl]
    fR$southLevel[fiblvl] <- fR$fibLevel[fiblvl] * 0.9995
    fR$northLevel[fiblvl] <- fR$fibLevel[fiblvl] * 1.0005
  }
  
  #get extreme vlues for ylim
  ylimlow <- min(c(min(fR$southLevel), min(plotData$askprice)))
  ylimhigh <- max(c(max(fR$northLevel), max(plotData$askprice)))
  
  #get S/F
  if (validated$resultpercent[i] > 0){
    resChar <- "S"
  } else{
    resChar <- "F"
  }
  #create plot
  plot(plotData$time, plotData$askprice,
       xlab = "time",
       ylab = "askprice",
       ylim = c(as.numeric(ylimlow), as.numeric(ylimhigh)),
       main = paste(resChar,
                    validated$symbol[i], 
                    validated$id[i], 
                    format(round(validated$resultpercent[i], 2), nsmall = 2),
                    format(round(validated$corvalue[i], 2), nsmall = 2)))
  
  #add lines for buy and sell, aswell as fibonacci retracement levels
  abline(v = validated$time[i], col = "red")
  abline(v = stopIdTime, col = "blue")
  for (fiblvl in 1:nrow(fR)){
    abline(h=c(fR$northLevel[fiblvl], fR$southLevel[fiblvl]), 
           col=fR$lineColor[fiblvl])
    text(min(largeData$time), fR$northLevel[fiblvl], 
         fR$retracement[fiblvl], cex = 1, pos = 3)
  }
}  

#disconnect from db
dbDisconnect(con) 

