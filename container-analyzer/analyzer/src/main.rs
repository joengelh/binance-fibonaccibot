use binance_access;
use postgres_access;
use redis_access;

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
    let sql = "SELECT count(*) FROM table001
    where takeprofit is not null and resultpercent is null;";
    let open_trades = postgres_access::get_count(&sql);
    redis_access::set_key_value("openTrades", 
        &open_trades.unwrap().to_string());
}

fn cache_sum_result() {
    let sql = "SELECT count(resultpercent) FROM table001;";
    let closed_trades = postgres_access::get_count(&sql);
    let cutoff: i64 = 1;
    if &closed_trades.as_ref().unwrap() <= &&cutoff {
        redis_access::set_key_value("sumResult", "0 %");
    } else {
        let sql = "select sum(resultpercent) from table001;";
        let sum_result = postgres_access::get_sum(&sql);
        redis_access::set_key_value("sumResult", 
        &format!("{}{}", &sum_result.unwrap().to_string(), " %"));
    }
}

fn cache_recent_sum_result() {
    let sql = "SELECT count(resultpercent) FROM table001
    where time > now() - interval \'24 hours\';";
    let closed_trades = postgres_access::get_count(&sql);
    let cutoff: i64 = 1;
    if &closed_trades.as_ref().unwrap() <= &&cutoff {
        redis_access::set_key_value("recentSumResult", "0 %");
    } else {
        let sql = "select sum(resultpercent) from table001
        where time > now() - interval \'24 hours\';";
        let sum_result = postgres_access::get_sum(&sql);
        redis_access::set_key_value("recentSumResult", 
        &format!("{}{}", &sum_result.unwrap().to_string(), " %"));
    }
}