use binance::api::*;
use binance::account::*;
use dotenv::dotenv;
use std::env;

pub fn get_base_currency_balance() -> f64 {
    dotenv().ok();

    let api_key = Some(env::var("apiKey").unwrap());
    let secret_key = Some(env::var("apiSecret").unwrap());
    let base_currency = &env::var("baseCurrency").unwrap();

    let account: Account = Binance::new(api_key, secret_key);
    
    // get balance
    let balance = account.get_balance(base_currency).unwrap();
    balance.free
}