use dotenv::dotenv;
use std::env;
use sqlx::postgres::{PgPoolOptions};
use sqlx::{FromRow};

#[derive(Debug, FromRow)]
struct CountResult {
	count: i64
}

#[derive(Debug, FromRow)]
struct SumResult {
	sum: f64
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

	let select_query = sqlx::query_as::<_, CountResult>(&sql);
	let result: Vec<CountResult> = select_query.fetch_all(&pool).await?;

    Ok(result[0].count)
}


#[tokio::main]
pub async fn get_sum(sql: &str) -> Result<f64, sqlx::Error> {
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

	let select_query = sqlx::query_as::<_, SumResult>(&sql);
	let result: Vec<SumResult> = select_query.fetch_all(&pool).await?;

    Ok(result[0].sum)
}
