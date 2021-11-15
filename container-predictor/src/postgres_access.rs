use postgres::{Client, Error, NoTls};
use std::collections::HashMap;
use dotenv::dotenv;
use std::env;

struct Student {
    id: i32
}

pub fn get_query_single() -> Result<(), Error> {

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

    let mut client = Client::connect(&postgres_path,
        NoTls,
    )?;

    Ok(for row in client.query("SELECT count(*) from table001", &[])? {
        let id: i32 = row.get(0);
        println!("found app user: {}", id);
    })

}