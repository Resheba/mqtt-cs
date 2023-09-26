# MQTT Module

The MQTT module (`mqtt.py`) provides convenient Python classes for MQTT (Message Queuing Telemetry Transport) communication. MQTT is a lightweight and efficient messaging protocol widely used in IoT (Internet of Things) and various other applications for message exchange between clients and servers.

## MQTT Client

The MQTT Client class (`MQTTClient`) simplifies the process of connecting to an MQTT broker, publishing messages, and handling MQTT events. It allows you to create and manage MQTT client instances for communication with an MQTT broker.

### Key Features:
- Establish connections with MQTT brokers.
- Publish messages to specified topics.
- Define custom callback functions for handling MQTT events (e.g., on_connect, on_message).

### Usage Example:

```python
from mqtt import MQTTClient

# Create an MQTT Client instance
client = MQTTClient(client_id="my_client")

# Connect to an MQTT broker
client.connect(ip="mqtt.eclipse.org")

# Publish a message
client.publish("Hello, MQTT!", topic="my_topic")

# Start the MQTT client's event loop
client.mqtt_client.loop_start()
```

For detailed information on class methods and attributes, please consult the module's documentation.

## MQTT Server

The MQTT Server class (`MQTTServer`) enables you to create and manage an MQTT server instance that acts as an MQTT broker. It allows you to connect to an MQTT broker as a server, handle incoming messages, and interact with connected clients.

### Key Features:
- Connect to MQTT brokers as a server.
- Define custom callback functions for handling MQTT events (e.g., on_connect, on_message).

### Usage Example:

```python
from mqtt import MQTTServer

# Create an MQTT Server instance
server = MQTTServer(server_id="my_server")

# Connect to an MQTT broker as a server
server.connect(ip="mqtt.eclipse.org")

# Define custom callback functions for handling MQTT events
def custom_message_handler(client, userdata, message):
    print("Received message:", message.payload.decode())

server.on_message = custom_message_handler

# Start the MQTT server's event loop
server.mqtt_server.loop_forever()
```

For detailed information on class methods and attributes, please consult the module's documentation.

## Requirements

- Python 3.x

## Installation

1. Clone this repository or download the `mqtt.py` module.
2. Ensure you have Python 3.x installed on your system.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

