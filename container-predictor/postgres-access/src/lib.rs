use dotenv::dotenv;
use std::env;
use sqlx::postgres::{PgPoolOptions, PgRow};
use sqlx::{FromRow, Row};

#[derive(Debug, FromRow)]
struct Ticket {
	count: i64
}

#[tokio::main]
pub async fn get_count(sql: &str) -> Result<i64, sqlx::Error> {
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

	let select_query = sqlx::query_as::<_, Ticket>(&sql);
	let tickets: Vec<Ticket> = select_query.fetch_all(&pool).await?;

    Ok(tickets[0].count)
}
