extern crate redis;

use dotenv::dotenv;
use std::env;
use redis::Commands;

pub fn push_data() {

    dotenv().ok();

    let redis_path: String = [
        "redis://",
        &env::var("POSTGRES_PASSWORD").unwrap(),
        "@",
        &env::var("dbHost").unwrap(),
        ":",
        &env::var("dbPort").unwrap(),
    ].join("");

    //let client = redis::Client::open(redis_path).unwrap();
    //let mut con = client.get_connection();
    //con.set("my_key", 42);
}
