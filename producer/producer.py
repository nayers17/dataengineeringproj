from kafka import KafkaProducer
import json, time

# connect to broker

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
)

# send 10 sample messages
for i in range(10):
    msg = {'count': i, 'ts': time.time()}
    producer.send('test-1', json.dumps(msg).encode('utf-8'))
    print('Sent:', msg)
    time.sleep(1)
    

producer.flush()
producer.close()