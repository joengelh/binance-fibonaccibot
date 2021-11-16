FROM rust:latest as builder

RUN USER=root cargo new --bin rust-docker-web
WORKDIR /analyzer
COPY . ./
RUN cargo run