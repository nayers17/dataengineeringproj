from kafka import KafkaConsumer
import json

# connect and subscribe
consumer = KafkaConsumer(
    'test-1',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    value_deserializer=lambda v: json.loads(v.decode())
)

# read 10 messages

for idx, msg in enumerate(consumer):
    print('Received:', msg.value)
    if idx >= 9:
        break
    
consumer.close()