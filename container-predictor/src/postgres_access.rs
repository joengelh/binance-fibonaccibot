use postgres::{Client, TlsMode};
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

    let mut conn = Client::connect(&postgres_path, NoTls).unwrap();
    for row in &conn.query("SELECT count(*) from table001", &[]).unwrap() {
        let student = Student {
            id: row.get(0)
        };
        println!("Found student {}", student.id);
    }
}