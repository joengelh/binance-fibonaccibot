#[macro_use]
extern crate dotenv_codegen;

extern crate dotenv;
//extern crate redis;
extern crate postgres;

use postgres::{Connection, TlsMode};
use postgres::tls::native_tls::NativeTls;
use dotenv::dotenv;
use std::env;

fn main() {
    dotenv().ok();

    let r_port: String = env::var("dbPort").unwrap();
    let r_host: String = env::var("brokerFees").unwrap();
    println!("Hello, {}", [r_host, r_port].join(" "));

    let RedisVars = RedisVars {
        db_port: env::var("rPort").unwrap(),
        db_host: env::var("dbHost").unwrap(),
        db_name: env::var("rName").unwrap(),
        db_pw: env::var("POSTGRES_PASSWORD").unwrap(),
    };

    println!("{}", RedisVars.db_port);

    let postgres_path: String = [
        "postgresql://",
        env::var("dbUser").unwrap(),
        ":",
        env::var("POSTGRES_PASSWORD").unwrap(),
        "@",
        env::var("dbHost").unwrap(),
        ":",
        env::var("dbPort").unwrap(),
        "/",
        env::var("dbName").unwrap(),
    ].join("");
    let mut conn = Client::connect(postgres_path).unwrap();
}

struct RedisVars {
    db_port: String,
    db_host: String,
    db_name: String,
    db_pw: String, 
}