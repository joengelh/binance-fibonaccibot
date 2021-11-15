use dotenv::dotenv;
use std::env;
use postgres::{Client, NoTls, Error};

struct ReturnedData {
    data: ,
}

pub fn get_count() -> Result<Vec, Error> {

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

    for row in &client.query("select count(*) from table001 where takeprofit is not null and resultpercent is null", &[]).unwrap() {
        let person = ReturnedData {
            id: row.get(0),
            name: row.get(1),
            data: row.get(2)
        };
        println!("Found person {}", person.name);
    }
}