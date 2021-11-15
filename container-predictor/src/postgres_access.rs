use dotenv::dotenv;
use std::env;
use postgres::{Client, NoTls, Error};

struct Author {
    id: i32
}

pub fn get_query_single() {

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

    let mut client = Client::connect(&postgres_path, NoTls);

    for row in client.query("SELECT id FROM table001;", &[])? {
        let author = Author {
            id: row.get(0),
        };
        println!("Author {} is from {}", author.name, author.country);
    }

    Ok(())
}