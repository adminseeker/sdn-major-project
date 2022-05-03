
#connect h1-h4

curl -X POST http://localhost:8080/stats/flowentry/add -d '@s1_flow1.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s1_flow2.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s2_flow1.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s2_flow2.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s3_flow1.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s3_flow2.json'

#connect h2-h5

curl -X POST http://localhost:8080/stats/flowentry/add -d '@s1_flow3.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s1_flow4.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s4_flow1.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s4_flow2.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s3_flow3.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s3_flow4.json'

#connect h3-h6

curl -X POST http://localhost:8080/stats/flowentry/add -d '@s1_flow5.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s1_flow6.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s5_flow1.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s5_flow2.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s3_flow5.json'
curl -X POST http://localhost:8080/stats/flowentry/add -d '@s3_flow6.json'

