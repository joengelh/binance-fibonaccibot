use dotenv::dotenv;
use std::env;
use postgres::{Client, NoTls, Error};

fn main() -> Result<(), Error> {

    dotenv().ok();

    let postgres_path: String = [
        "postgresql://",
        &env::var("dbUser").unwrap(),
        ":",
        &env::var("POSTGRES_PASSWORD").unwrap(),
        "@",
        &env::var("dbHost").unwrap(),
        ":",
        &env::var("dbPort").unwrap(),
        "/",
        &env::var("dbName").unwrap(),
    ].join("");

    let mut client = Client::connect(&postgres_path, NoTls)?;
    
    client.query("SELECT id, name, country FROM author", &[])? {
        let author = Author {
            _id: row.get(0),
            name: row.get(1),
            country: row.get(2),
        };
        println!("Author {} is from {}", author.name, author.country);

    Ok(())
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
