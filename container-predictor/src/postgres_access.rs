use postgres::{Client, NoTls, Error};
use std::collections::HashMap;
use dotenv::dotenv;
use std::env;

struct QueryResult {
    data: String
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

    let mut client = Client::connect(&postgres_path, NoTls)?;
    
    let mut authors = HashMap::new();
    authors.insert(String::from("Chinua Achebe"), "Nigeria");
    authors.insert(String::from("Rabindranath Tagore"), "India");
    authors.insert(String::from("Anita Nair"), "India");

    for row in client.query("SELECT count(*) from table001;", &[])? {
        let result = QueryResult {
            data: row.get(0),
        };
        println!("{}", result.data.as_str());
    }

    Ok(())

}