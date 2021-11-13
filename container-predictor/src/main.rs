#[macro_use]
extern crate dotenv_codegen;

extern crate dotenv;
extern crate redis;

use dotenv::dotenv;
use std::env;

fn main() {
    let somestring = env::var("CARGO_HOME").unwrap();
    let someotherstring = env::var("brokerFees").unwrap();
    println!("Hello, {}", [somestring, someotherstring].join(""));

}


fn write_to_redis() -> redis::RedisResult<()> {
    let client = redis::Client::open("redis://127.0.0.1/")?;
    let mut con = client.get_connection()?;

    /* do something here */

    Ok(())
}