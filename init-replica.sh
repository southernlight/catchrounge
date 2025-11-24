#!/bin/bash

echo "Initializing MongoDB Replica Set..."

# MongoDB가 완전히 시작될 때까지 잠시 기다리기 (10초)
sleep 10

# MongoDB Replica Set 초기화 (인증 없음)
mongosh --host mongo1:27017 <<EOF
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})
EOF

echo "MongoDB Replica Set initialization complete."