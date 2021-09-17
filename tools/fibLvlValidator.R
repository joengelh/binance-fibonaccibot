library(RPostgres)

#connect to postgres
con <- dbConnect(RPostgres::Postgres(), dbname = "postgres",
                 host = "192.168.2.8",
                 user = "postgres",
                 password = "password")

#declare fibonacci levels
fR <- data.frame(
  retracement = c(2,1.786,1.618,1.382,1.236,
                  1,0.786,1.5,
                  0.618,0.5,0.382,0.236,0),
  lineColor = c('red', 'blue', 'green','blanchedalmond',
                'yellow', 'brown', 'turquoise3',
                'orange', 'purple', 'chartreuse1', 
                'violet', 'goldenrod1','forestgreen')
)
fR$fibLevel <- NA
fR$southLevel <- NA
fR$northLevel <- NA

#get list of buy advice instances

sqlQuery <- dbSendQuery(con, "SELECT * FROM table001 WHERE
                        resultpercent is not null;")
vA <- dbFetch(sqlQuery)
dbClearResult(sqlQuery)

for (i in unique(vA$fiblevel)){
  interm <- vA[vA$fiblevel == i,]
  plot(interm$resultpercent, interm$corvalue, main = i)
  abline(v=0, col="blue")
  successcount <- 0
  unsuccesscount <- 0
  for (row in interm$resultpercent){
    if (row > 0){
      successcount <- successcount +1
    }
    else{
      unsuccesscount <- unsuccesscount +1
    }
  }
}
print(paste("total corvalue resultpercent cor: ", cor(vA$resultpercent, vA$corvalue)))
dbDisconnect(con)

plot(vA$id, vA$resultpercent, 
     main = paste("cor id:", 
     cor(interm$resultpercent, interm$id)))
abline(h=0, col="blue")
boxplot(interm$resultpercent ~ interm$symbol)
abline(h=0, col="blue")
plot(vA$corvalue, vA$resultpercent, 
     main = paste("cor corvalue:", 
     cor(interm$resultpercent, interm$corvalue)))
abline(h=0, col="blue")
plot(vA$quotevolume, vA$resultpercent,
     main = paste("cor quotevolume:", 
     cor(interm$resultpercent, interm$quotevolume)))
abline(h=0, col="blue")
plot(vA$pricechangepercent, vA$resultpercent,
     main = paste("cor pricechangepercent:", 
     cor(interm$resultpercent, interm$pricechangepercent)))
abline(h=0, col="blue")
plot(vA$stdev, vA$resultpercent,
     main = paste("cor standard deviation:", 
                  cor(interm$stdev, interm$resultpercent)),
     xlim = c(0,0.000001))
abline(h=0, col="blue")

print(paste("success n: ", successcount))
print(paste("unsuccess n: ", unsuccesscount))
print(paste("trades: ", length(interm$symbol)))
