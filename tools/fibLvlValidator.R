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
sqlQuery <- dbSendQuery(con, "SELECT * FROM table001 WHERE resultpercent IS NOT NULL and corvalue >= -0.25;")
validated <- dbFetch(sqlQuery)
dbClearResult(sqlQuery)

for (i in unique(validated$fiblevel)){
  interm <- validated[validated$fiblevel == i,]
  capital <- 10000
  for (move in interm$resultpercent){
    capital <- capital + move
  }
  plot(interm$resultpercent, interm$corvalue, main = i)
  print(paste("==================", i,"=================="))
  print(paste("trades: ", length(interm$symbol)))
  print(paste("mean percent: ", mean(interm$resultpercent)))
  print(paste("result: ", capital))
  print(paste("id time cor: ", mean(interm$corvalue)))
  print(paste("corvalue resultpercent cor: ", cor(interm$resultpercent, interm$corvalue)))
  successcount <- 0
  unsuccesscount <- 0
  print(unique(interm$symbol))
  for (row in interm$resultpercent){
    if (row > 0){
      successcount <- successcount +1
    }
    else{
      unsuccesscount <- unsuccesscount +1
    }
  }
  print(paste("success n: ", successcount))
  print(paste("unsuccess n: ", unsuccesscount))
}
print(paste("total corvalue resultpercent cor: ", cor(validated$resultpercent, validated$corvalue)))
dbDisconnect(con)
