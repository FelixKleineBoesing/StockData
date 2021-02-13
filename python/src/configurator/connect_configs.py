
def get_postgres_sink(postgres_host, postgres_port, postgres_db, postgres_user, postgres_password,
                      schema_host, schema_port):
    postgres_sink = {"name": "postgres-sink",
                     "config": {"connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
                                "tasks.max": "1",
                                "topics": "stocks",
                                "key.converter": "org.apache.kafka.connect.storage.StringConverter",
                                "value.converter": "io.confluent.connect.avro.AvroConverter",
                                "value.converter.schema.registry.url": "http://{}:{}".
                                    format(schema_host, schema_port),
                                "connection.url": "jdbc:postgresql://{}:{}/{}?user={}&password={}".
                                    format(postgres_host, postgres_port, postgres_db, postgres_user, postgres_password),
                                "key.converter.schemas.enable": "false",
                                "value.converter.schemas.enable": "true",
                                "auto.create": "true",
                                "auto.evolve": "true",
                                "insert.mode": "upsert",
                                "pk.fields": "index",
                                "pk.mode": "record_key"
                                }
                     }
    return postgres_sink


def get_postgres_source(postgres_host, postgres_port, postgres_db, postgres_user, postgres_password,
                        schema_host, schema_port, kafka_host, kafka_port):
    postgres_source = {"name": "postgres-source",
                       "config": {"connector.class":"io.debezium.connector.postgresql.PostgresConnector",
                                  "tasks.max": "1",
                                  "database.hostname": postgres_host,
                                  "database.port": postgres_port,
                                  "database.user": postgres_user,
                                  "database.password": postgres_password,
                                  "database.dbname": postgres_db,
                                  "database.server.name": "dbserver1",
                                  "database.whitelist": "stocks",
                                  "database.history.kafka.bootstrap.servers": "{}:{}".format(kafka_host, kafka_port),
                                  "database.history.kafka.topic": "schema-changes.stocks",
                                  "key.converter": "org.apache.kafka.connect.storage.StringConverter",
                                  "value.converter": "io.confluent.connect.avro.AvroConverter",
                                  "key.converter.schemas.enable": "false",
                                  "value.converter.schemas.enable": "true",
                                  "value.converter.schema.registry.url": "http://{}:{}".
                                      format(schema_host, schema_port),
                                  "transforms": "unwrap",
                                  "transforms.unwrap.type": "io.debezium.transforms.UnwrapFromEnvelope"
                                  }
                       }
    return postgres_source