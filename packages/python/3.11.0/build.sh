#!/bin/bash

PREFIX=$(realpath $(dirname $0))

mkdir -p build

cd build
curl -L -o python.tar.gz "https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz" 
tar xzf python.tar.gz --strip-components=1
rm python.tar.gz
./configure --prefix "$PREFIX" --with-ensurepip=install
make -j$(nproc)
make install -j$(nproc)
cd ..
rm -rf build

echo "Installing Java (Zulu OpenJDK)"
curl -L -o java.tar.gz "https://cdn.azul.com/zulu/bin/zulu17.30.15-ca-jdk17.0.1-linux_x64.tar.gz"
tar xzf java.tar.gz
rm java.tar.gz
mv zulu17.30.15-ca-jdk17.0.1-linux_x64 "$PREFIX/java"

echo "Installing Apache Spark"
curl -L -o spark.tgz "https://dlcdn.apache.org/spark/spark-4.0.0/spark-4.0.0-bin-hadoop3.tgz"
tar xzf spark.tgz
rm spark.tgz
mv spark-4.0.0-bin-hadoop3 "$PREFIX/spark"
echo "Setting up Ivy directory"
mkdir -p /tmp/home/.ivy2

echo "Installing Hadoop native binaries"
curl -L -o hadoop-native.tar.gz "https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz"
tar xzf hadoop-native.tar.gz
rm hadoop-native.tar.gz
mv hadoop-3.3.6 "$PREFIX/hadoop"




bin/pip3 install numpy scipy pandas pycryptodome whoosh bcrypt passlib sympy xxhash base58 cryptography PyNaCl pyspark
