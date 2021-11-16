use binance_access;
use postgres_access;
use redis_access;

fn main() {
    // cache balance
    let balance = binance_access::get_base_currency_balance();
    println!("{}", balance);
    redis_access::set_key_value("assets", &balance);
    postgres_access::get_query_single();
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