#![allow(unused)] // silence unused warnings while exploring (to comment out)

use dotenv::dotenv;
use std::env;
use sqlx::postgres::{PgPoolOptions, PgRow};
use sqlx::{FromRow, Row};

#[derive(Debug, FromRow)]
struct Ticket {
	id: i32,
	symbol: String,
}

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
	
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

    
    // 1) Create a connection pool
	let pool = PgPoolOptions::new()
		.max_connections(5)
		.connect(&postgres_path)
		.await?;

	let select_query = sqlx::query_as::<_, Ticket>("SELECT id, symbol FROM table001");
	let tickets: Vec<Ticket> = select_query.fetch_all(&pool).await?;
	println!("\n{:?}", tickets);

	Ok(())
}
