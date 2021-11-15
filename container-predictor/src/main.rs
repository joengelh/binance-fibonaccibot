mod binance_access;



fn main() {
    binance_access::get_base_currency_balance()
}

// keys to be cached
// simulatedAvg
//  value=str(round(sum(resultPercent)/len(resultPercent), 2)) + " %"
// simulatedSum
//  value=str(round(sum(resultPercent), 2)) + " %"
// simulatedWinner
//  value=round(sum(i > 0 for i in resultPercent), 2)
// simulatedLoser
//  value=round(sum(i < 0 for i in resultPercent), 2)
//  for index, row in openTrades.iterrows():
//  resultPercent.append(((float(stopId[0][0]) - float(row[1])) / float(row[1])) * 100 - self.brokerFees * 2)
//  str(round(sum(resultPercent)/len(resultPercent), 2)) + " %"
// assets
// openTrades
// sumResult
//  select sum((resultpercent/100) * positioncost) from ' + 
// recentSumResult
//  select sum((resultpercent/100) * positioncost) from ' + 