FROM rust:latest as builder

RUN USER=root cargo new --bin rust-docker-web
WORKDIR /analyzer
COPY ./Cargo.toml ./
RUN cargo build --release
RUN rm src/*.rs

ADD . ./

RUN rm ./target/release/deps/analyzer*
RUN cargo build --release


FROM debian:buster-slim
ARG APP=/usr/src/app