from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1

FIELD_MESSAGE_ID = 0
FIELD_DEVICE_ID = 1
FIELD_TIMESTAMP = 2
FIELD_CATEGORY = 3
FIELD_MEASURE1 = 4
FIELD_MEASURE2 = 5

def parseEvent(message):
    return message.split('|')

def main():
    conf = SparkConf() \
        .setAppName("boontadata-streams-spark") \
        .setMaster("spark://sparkm1:7077") \
        .set("spark.cassandra.connection.host", "cassandra1")

    # set up our contexts
    sc = SparkContext(conf=conf) 
    sql = SQLContext(sc)
    streamingContext = StreamingContext(sc, batchDuration=5)

    kafka_stream = KafkaUtils.createDirectStream(streamingContext,
        ["sampletopic"], 
        {"metadata.broker.list": "ks1:9092,ks2:9092,ks3:9092"})

    parsed = kafka_stream.map(lambda event: parseEvent(event[1]))

    parsed.pprint()
    # sc.parallelize(aggregated) \
    #    .saveToCassandra("boontadata", "agg_events")

    streamingContext.start()
    streamingContext.awaitTermination()

if __name__ == '__main__':
    main()
