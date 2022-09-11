# pyvera

Python code generator for silvera language

## Libraries/Frameworks used in generated code

- [Fastapi](https://github.com/tiangolo/fastapi)
- [Beanie](https://github.com/roman-right/beanie/)
- [AIOKafka](https://github.com/aio-libs/aiokafka)
- [circuitbreaker](https://github.com/fabfuel/circuitbreaker)

## Project status

- [x] Setup py
- [x] Models generation
- [x] CRUD API generation
- [x] Custom API endpoints generation
- [x] Messages models
- [x] Kafka producers
- [x] Kafka consumers
- [x] Dependency services
- [x] Circuit breaker pattern
- [x] Start scripts
- [ ] \*Switch consul with eureka
- [ ] Containerization

\* Only realized later during the development that API Gateway, Service Registry generation was only supported for JAVA platform. Consul (Template) and Nginx were considered for the purposes of implementation of these patterns.
