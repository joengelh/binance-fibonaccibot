use sqlx::postgres::{PgPoolOptions, PgRow};
use sqlx::{FromRow, Row};
use dotenv::dotenv;
use std::env;

#[derive(Debug, FromRow)]
struct Ticket {
	id: i64,
	name: String,
}

pub async fn get_query_single() -> Result<(), sqlx::Error> {

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

    let pool = PgPoolOptions::new()
		.max_connections(5)
		.connect(&postgres_path)
		.await?;

        let rows = sqlx::query("SELECT * FROM table001").fetch_all(&pool).await?;
        let str_result = rows
            .iter()
            .map(|r| format!("{} - {}", r.get::<i64, _>("id"), r.get::<String, _>("name")))
            .collect::<Vec<String>>()
            .join(", ");
        println!("\n== select tickets with PgRows:\n{}", str_result);
}