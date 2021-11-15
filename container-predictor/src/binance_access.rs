use binance::api::*;
use binance::account::*;
use dotenv::dotenv;
use std::env;

pub fn get_base_currency_balance() -> f32 {
    dotenv().ok();

    let api_key = Some(env::var("apiKey").unwrap());
    let secret_key = Some(env::var("apiSecret").unwrap());
    let base_currency = &env::var("baseCurrency").unwrap();

    let account: Account = Binance::new(api_key, secret_key);
    
    let balance_str = match account.get_balance(base_currency) {
        Ok(balance) => balance,
        Err(e) => panic!("{:?}", e),
    };

    let balance_f: f32 = balance_str.free.parse().unwrap();
    let balance_r: f32 = (balance_f * 100.0).round() / 100.0;
    return balance_r;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_biance_connection() {
        let balance = get_base_currency_balance();
        assert!(balance >= 0.0);
    }
}