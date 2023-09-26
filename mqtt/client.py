import json
from paho.mqtt.client import Client, MQTTMessage


class MQTTClient:
    """
    MQTTClient - Class for managing MQTT clients.

    Args:
        client_id (str): Unique client identifier.
        sub_topics (list[tuple[str, int]], optional): List of topics that the client subscribes to by default. 
            Each element in the list is a tuple (topic, qos). Default is None.

    Attributes:
        client_id (str): Unique client identifier.
        mqtt_client (paho.mqtt.client.Client): Paho MQTT client.
        connected (bool): Flag indicating whether the client is connected to the MQTT broker.
        sub_topics (list[tuple[str, int]]): List of topics that the client subscribes to by default.

    Methods:
        connect(ip: str, port: int = 1883, keepalive: int = 60) -> None:
            Connects the client to an MQTT broker.

        on_connect(client: Client, user_data: str | None, flags: dict, rc: int) -> None:
            Callback function called upon successful connection to the MQTT broker.

        on_disconnect(client: Client, user_data: str | None, rc: int) -> None:
            Callback function called upon disconnection from the MQTT broker.

        publish(message: str | dict, topic: str = None) -> None:
            Publishes a message to the specified topic.

    Example:
        client = MQTTClient(client_id="my_client")
        client.connect(ip="mqtt.eclipse.org")
        client.publish("Hello, MQTT!", topic="my_topic")
    """
    def __init__(
            self,
            *,
            client_id: str,
            sub_topics: list[tuple[str, int]] = None # [('server/connect', 0)]
            ) -> None:
        self.client_id: str = client_id.strip()
        self.mqtt_client: Client = Client(client_id=self.client_id)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.connected: bool = False
        self.sub_topics = sub_topics

    def connect(
            self,
            ip: str,
            port: int = 1883,
            keepalive: int = 60
    ) -> None:
        """
        Connects the client to an MQTT broker.

        Args:
            ip (str): IP address of the MQTT broker.
            port (int, optional): Port for the connection. Default is 1883.
            keepalive (int, optional): Keepalive interval for sending keepalive packets. Default is 60.

        Returns:
            None
        """
        self.mqtt_client.connect(ip, port, keepalive)
        self.mqtt_client.subscribe(self.sub_topics) if self.sub_topics else None

    def on_connect(
        self,
        client: Client, 
        user_data: str | None, 
        flags: dict, 
        rc: int
    ) -> None:
        """
        Callback function called upon successful connection to the MQTT broker.

        Args:
            client (paho.mqtt.client.Client): Paho MQTT client.
            user_data (str | None): User data (not used).
            flags (dict): Flags related to the connection.
            rc (int): Connection result code.

        Returns:
            None
        """
        if rc == 0:
            self.connected: bool = True
            print(self.client_id, "connected")

    @staticmethod
    def on_message(
        client: Client, 
        user_data: str | None, 
        msg: MQTTMessage
    ) -> None:
        """
        Callback function called upon receiving a message from the MQTT broker.

        Args:
            client (paho.mqtt.client.Client): Paho MQTT client.
            user_data (str | None): User data (not used).
            msg (paho.mqtt.client.MQTTMessage): Received message.

        Returns:
            None
        """
        pass

    def on_disconnect(
        self,
        client: Client,
        user_data: str | None,
        rc: int
    ) -> None:
        """
        Callback function called upon disconnection from the MQTT broker.

        Args:
            client (paho.mqtt.client.Client): Paho MQTT client.
            user_data (str | None): User data (not used).
            rc (int): Disconnection result code.

        Returns:
            None
        """
        self.connected: bool = False

    def publish(
        self,
        message: str | dict,
        topic: str = None
    ) -> None:
        """
        Publishes a message to the specified topic.

        Args:
            message (str | dict): Message to publish. Can be a string or a dictionary.
            topic (str, optional): Topic to publish the message to. If not specified, the default topic will be used.

        Returns:
            None
        """
        if type(message) == dict:
            message = json.dumps(message)

        self.mqtt_client.publish(
            topic=topic or f"client/{self.client_id}",
            payload=message
        )
