use binance_access;
use postgres_access;
use redis_access;

use std::env;
use std::str::FromStr;
use std::{thread, time};

fn main() {
    loop {
        cache_balance();
        cache_open_trades();
        cache_sum_result();
        cache_recent_sum_result();
        thread::sleep(time::Duration::from_secs(60));
    }    
}

fn cache_balance() {
    let balance = binance_access::get_base_currency_balance();
    redis_access::set_key_value("assets", &balance);
}

fn cache_open_trades() {
    let sql = ["SELECT count(*) FROM", 
        &env::var("dbTable").unwrap_or_default(), 
        "where takeprofit is not null and resultpercent is null;"].join(" ");
    let open_trades = postgres_access::get_count(&sql);
    redis_access::set_key_value("openTrades", 
        &open_trades.unwrap().to_string());
}

fn cache_sum_result() {
    let sql = ["SELECT count(resultpercent) FROM",
        &env::var("dbTable").unwrap_or_default()].join(" ");
    let closed_trades = postgres_access::get_count(&sql);
    let cutoff: i64 = 1;
    if &closed_trades.as_ref().unwrap() < &&cutoff  {
        if FromStr::from_str(&env::var("liveTrading").unwrap_or_default()) == Ok(true) {
            redis_access::set_key_value("sumResult",
                &format!("{}{}", "NaN ", &env::var("baseCurrency").unwrap_or_default()));
        } else {
            redis_access::set_key_value("sumResult", "NaN %");
        }
    } else {
        if FromStr::from_str(&env::var("liveTrading").unwrap_or_default()) == Ok(true) {
            let sql = ["select sum(resultpercent / 100) * positioncost from",
                &env::var("dbTable").unwrap_or_default(),
                "where positioncost is not null"].join(" ");
            let result = postgres_access::get_sum(&sql_positioncost);
            let rounded_result = (result.unwrap() * 100.0).round() / 100.0;
            redis_access::set_key_value("sumResult",
                &format!("{}{}{}", &rounded_result,
                " ", &env::var("baseCurrency").unwrap_or_default()));
        } else {
            let sql = ["select sum(resultpercent) from",
                &env::var("dbTable").unwrap_or_default()].join(" ");
            let sum_result = postgres_access::get_sum(&sql);
            let rounded_result = (sum_result.unwrap() * 100.0).round() / 100.0;
            redis_access::set_key_value("sumResult", 
                &format!("{}{}", &rounded_result.to_string(), " %"));
        }
    }
}

fn cache_recent_sum_result() {
    let sql = ["SELECT count(resultpercent) FROM",
        &env::var("dbTable").unwrap_or_default(),
        "where time > now() - interval \'24 hours\';"].join(" ");
    let closed_trades = postgres_access::get_count(&sql);
    let cutoff: i64 = 1;
    if &closed_trades.as_ref().unwrap() < &&cutoff  {
        if FromStr::from_str(&env::var("liveTrading").unwrap_or_default()) == Ok(true) {
            redis_access::set_key_value("recentSumResult",
                &format!("{}{}", "NaN ", &env::var("baseCurrency").unwrap_or_default()));
        } else {
            redis_access::set_key_value("recentSumResult", "NaN %");
        }
    } else { 
        if FromStr::from_str(&env::var("liveTrading").unwrap_or_default()) == Ok(true) {
            let result = ["select sum(resultpercent / 100) * positioncost from",
                &env::var("dbTable").unwrap_or_default(),
                "where positioncost is not null and time > now() - interval \'24 hours\';"].join(" ");
            let result = postgres_access::get_sum(&sql_positioncost);
            let rounded_result = (result.unwrap() * 100.0).round() / 100.0;
            redis_access::set_key_value("recentSumResult", 
                &format!("{}{}", &rounded_result.to_string(), " %"));
        } else {
            let sql = ["select sum(resultpercent) from",
                &env::var("dbTable").unwrap_or_default(),
                "where positioncost is not null and time > now() - interval \'24 hours\';"].join(" ");
            let sum_result = postgres_access::get_sum(&sql);
            let rounded_result = (sum_result.unwrap() * 100.0).round() / 100.0;
            redis_access::set_key_value("recentSumResult", 
                &format!("{}{}", &rounded_result.to_string(), " %"));
        }
    }
}
