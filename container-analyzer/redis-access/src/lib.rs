use std::env;

fn connect() -> redis::Connection {

    let redis_host_name =
        env::var("dbHost").expect("missing environment variable REDIS_HOSTNAME");

    let redis_password = env::var("POSTGRES_PASSWORD").unwrap_or_default();

    //if Redis server needs secure connection
    let uri_scheme = match env::var("IS_TLS") {
        Ok(_) => "rediss",
        Err(_) => "redis",
    };

    let redis_conn_url = format!("{}://:{}@{}", uri_scheme, redis_password, redis_host_name);

    redis::Client::open(redis_conn_url)
        .expect("Invalid connection URL")
        .get_connection()
        .expect("failed to connect to Redis")
}

pub fn set_key_value(key: &str, value: &str) {
    let mut conn = connect();
    let _: () = redis::cmd("SET")
        .arg(key)
        .arg(value)
        .query(&mut conn)
        .expect("failed to execute SET for 'foo'");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_set_key_value() {
        set_key_value("openTrades", "200000");
    }
}

