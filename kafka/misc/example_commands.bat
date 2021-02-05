# create topic
D:\kafka\bin\windows\kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic word-count-input

# start a producer
D:\kafka\bin\windows\kafka-console-producer.bat --broker-list localhost:9092 --topic favourite-color-input

# start a consumer
D:\kafka\bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 ^
    --topic bank-balance-output ^
    --from-beginning ^
    --formatter kafka.tools.DefaultMessageFormatter ^
    --property print.key=true ^
    --property print.value=true ^
    --property key.deserializer=org.apache.kafka.common.serialization.StringDeserializer ^
    --property value.deserializer=org.apache.kafka.common.serialization.StringDeserializer

