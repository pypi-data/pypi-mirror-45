![build status](https://travis-ci.org/BrewBlox/brewblox-devcon-spark.svg?branch=develop)

# Spark Service

The Spark service handles connectivity for the BrewPi Spark controller.

This includes USB/TCP communication with the controller, but also encoding, decoding, and broadcasting data.

![Command Transformation](http://www.plantuml.com/plantuml/png/dLPDZ-Cs3BtdLn2vJ59aaalHmw0eTfC9q2tQpc2JOe-58jDZxSYIAyepOnJzxwKasx7piOjTdsnza7oFZwJVaHVErwM6ZIrBOJBOEs4ejwuKNbapcLIyhy8hJ4MbbbKpXNydmC_iXpdStlu2quyeKRqW_BhVFuB3VseaFur7ulQZS8GWt5DTel44kRFbw2pCQgU1VQ-iWuFDclbqShp-XwZ07ZwZz2jgo6EvgfpDbKROVFph7lBQo1YTjx3ZM9z19Y2KGZ3M8pZrLFZu6PxjcoWhZNVm-B3Rmuh2hLLoGJ4cvP10iFtj-_tsxuVrRzlDlZExwCq4iWHamWiWRns2T2WyndtalU1vae0CECpmHKaSqDW3tLZpWiu3eGj7uCDzm2IjySvgZOuNflsD2x32i-llCW0EYRnJveaMCLWf31mup4AO9ypWq80l46hsjnmPsGnT9ZkA4vUCXAyCFRfIcQEHOvHdfXWJ1UIA8BC6mutCSb1ihStha4DjxNDTBISZA-yDu9l4ohTsd534lbNED8m9ugzQPm5bRckJ7OCv9gHR6UH4sWmbfmHcQCBxV9YRFZ_Rk0S7RULp37awEdCb8qSMV52BOhWs7rG3f_ZHMMyFTNwRl0TIFTBopCpEbfYuyas5lLJPRENmbgj28b5WbglabCAUnYZzGEA3mKzyUrtJtTd9BYBET8Y8G76aDoBBk33e1dA5JF8iXZa7GN0GX3_zsAdjFFArmzUrjc_mAYBc0akcWYej6eRB57H23COA3fBzgbBewnRtXOeduMTEJUjUdejDcSJE2JbXFP4zcuzjzphf5lwxefZO35ZkuqBknRAk5LFKzjHl4GeZhbaZGUL85N-hWmvgTYqy7p2aaalzUYIbLZbdXlzadtSWfBGkYmPYtIHVYu6aGMXkObaJ_Dz4OpTN-3c7l0jxBU85yFYG1RmgNp2GIZVJ2pVIPFXMalOCdfgoHDQ6P8tOghAa-3ZNrGdloskbs4wXY32GSQ4oBx2uFl94NcaTM18TJrqpAz3XTsggwqAfwYvteNlytYwqkyRPLnhRby8V3QxHt8Zpk9z6NnrSltFV9wWhvdCu_mhXavAGJkOCRvzaw5E1NFW-54PAAW-lnUajpbWGlkBI3PqdICdMJaOYk1fyCKxTXpXY1X6rCpHEbmN45aFjuC_IW2JnadhQSQfT64C37jj_A5yxS_8BDU4Jx_WA_vxz3m00 "Command Transformation")

## Features

### SparkConduit ([communication.py](./brewblox_devcon_spark/communication.py))

Direct communication with the Spark is handled here, for both USB and TCP connections. Data is not decoded or interpreted, but passed on to the `SparkCommander`.

### Controlbox Protocol ([commands.py](./brewblox_devcon_spark/commands.py))

The Spark communicates using the [Controlbox protocol](https://brewblox.netlify.com/dev/reference/spark_commands.html). A set of commands is defined to manage blocks on the controller.

In the commands module, this protocol of bits and bytes is encapsulated by `Command` classes. They are capable of converting a Python dict to a hexadecimal byte string, and vice versa.

### SparkCommander ([commander.py](./brewblox_devcon_spark/commander.py))

Serial communication is asynchronous: requests and responses are not linked at the transport layer.

`SparkCommander` is responsible for building and sending a command, and then matching it with a subsequently received response.

### SimulationCommander ([commander_sim.py](./brewblox_devcon_spark/commander_sim.py))

For when using an actual Spark is inconvenient, there is a simulation version. It serves as a drop-in replacement for the real commander: it handles commands, and returns sensible values.
Commands are encoded/decoded, to closely match the real situation.

### Datastore ([datastore.py](./brewblox_devcon_spark/datastore.py))

The service must keep track of object metadata not directly persisted by the controller. This includes user-defined object names and descriptions.

Services are capable of interacting with a BrewPi Spark that has pre-existing blocks, but will be unable to display objects with a human-meaningful name.

Object metadata is persisted to files. This does not include object settings - these are the responsibility of the Spark itself.

### Codec ([codec.py](./brewblox_devcon_spark/codec/codec.py))

While the controller <-> service communication uses the Controlbox protocol, individual objects are encoded separately, using Google's [Protocol Buffers](https://developers.google.com/protocol-buffers/).

The codec is responsible for converting JSON-serializable dicts to byte arrays, and vice versa. A specific transcoder is defined for each object.

For this reason, the object payload in Controlbox consists of two parts: a numerical `object_type` ID, and the `object_data` bytes.

### SparkController ([device.py](./brewblox_devcon_spark/device.py))

`SparkController` combines the functionality of `commands`, `commander`, `datastore`, and `codec` to allow interaction with the Spark using Pythonic functions.

Any command is modified both incoming and outgoing: ID's are converted using the datastore, data is sent to codec, and everything is wrapped in the correct command before it is sent to `SparkCommander`.

### Broadcaster ([broadcaster.py](./brewblox_devcon_spark/broadcaster.py))

The Spark service is not responsible for retaining any object data. Any requests are encoded and forwarded to the Spark.

To reduce the impact of this bottleneck, and to persist historic data, `Broadcaster` reads all objects every few seconds, and broadcasts their values to the eventbus.

Here, the data will likely be picked up by the [History Service](https://github.com/BrewBlox/brewblox-history).


### Seeder ([seeder.py](./brewblox_devcon_spark/seeder.py))

Some actions are required when connecting to a (new) Spark controller.
The Seeder feature waits for a connection to be made, and then performs these one-time tasks.

Examples are:
* Setting Spark system clock
* Reading controller-specific data from the remote datastore

## REST API

### ObjectApi ([object_api.py](./brewblox_devcon_spark/api/object_api.py))

Offers full CRUD (Create, Read, Update, Delete) functionality for Spark objects.

### SystemApi ([system_api.py](./brewblox_devcon_spark/api/system_api.py))

System objects are distinct from normal objects in that they can't be created or deleted by the user.

### RemoteApi ([remote_api.py](./brewblox_devcon_spark/api/remote_api.py))

Occasionally, it is desirable for multiple Sparks to work in concert. One might be connected to a temperature sensor, while the other controls a heater.

Remote blocks allow synchronization between master and slave blocks.

In the sensor/heater example, the Spark with the heater would be configured to have a dummy sensor object linked to the heater.

Instead of directly reading a sensor, this dummy object is updated by the service whenever it receives an update from the master object (the real sensor).

### AliasApi ([alias_api.py](./brewblox_devcon_spark/api/alias_api.py))

All objects can have user-defined names. The AliasAPI allows users to set or change those names.
