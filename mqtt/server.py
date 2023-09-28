from typing import Callable
from paho.mqtt.client import Client, MQTTMessage


class MQTTServer:
    """
    MQTTServer - Class for managing MQTT servers.

    Args:
        server_id (str, optional): Unique server identifier. Default is "server".
        sub_topics (list[tuple[str, int]], optional): List of topics that the server subscribes to by default. 
            Each element in the list is a tuple (topic, qos). Default is [('client/+', 0)].

    Attributes:
        server_id (str): Unique server identifier.
        mqtt_server (paho.mqtt.client.Client): Paho MQTT client used as the server.
        connected (bool): Flag indicating whether the server is connected to the MQTT broker.
        sub_topics (list[tuple[str, int]]): List of topics that the server subscribes to by default.
        connected_clients (dict): Dictionary to store connected clients.

    Methods:
        connect(ip: str, port: int = 1883, keepalive: int = 60) -> None:
            Connects the server to an MQTT broker as a client.

        on_connect(client: Client, user_data: str | None, flags: dict, rc: int) -> None:
            Callback function called upon successful connection to the MQTT broker.

        on_disconnect(client: Client, user_data: str | None, rc: int) -> None:
            Callback function called upon disconnection from the MQTT broker.

        on_message: Callable
            Getter and Setter for the callback function called upon receiving a message from the MQTT broker.

        publish(message: str | dict, topic: str = None) -> None:
            Publishes a message to the specified topic.

    Example:
        server = MQTTServer(server_id="my_server")
        server.connect(ip="mqtt.eclipse.org")
        server.publish("Hello, MQTT!", topic="my_topic")
    """
    def __init__(
            self,
            *,
            server_id: str = "server",
            username: str = None,
            password: str = None,
            sub_topics: list[tuple[str, int]] = [('client/+', 0)]
            ) -> None:
        self.server_id: str = server_id.strip()
        self.mqtt_server: Client = Client(client_id=self.server_id)
        if username or password:
            self.mqtt_server.username_pw_set(username=username, password=password)

        self.mqtt_server.on_connect = self.on_connect
        self.mqtt_server.on_message = self.on_message
        self.mqtt_server.on_disconnect = self.on_disconnect
        self.connected: bool = False
        self.sub_topics = sub_topics
        
        self.connected_clients: dict = dict()

    def connect(
            self,
            ip: str,
            port: int = 1883,
            keepalive: int = 60
    ) -> None:
        """
        Connects the server to an MQTT broker as a client.

        Args:
            ip (str): IP address of the MQTT broker.
            port (int, optional): Port for the connection. Default is 1883.
            keepalive (int, optional): Keepalive interval for sending keepalive packets. Default is 60.

        Returns:
            None
        """
        self.mqtt_server.connect(ip, port, keepalive)
        self.mqtt_server.subscribe(self.sub_topics) if self.sub_topics else None

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
            print(self.server_id, "connected")
    
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
    
    @property
    def on_message(
        self
    ) -> Callable:
        """
        Getter for the callback function called upon receiving a message from the MQTT broker.

        Returns:
            Callable: Callback function called upon receiving a message.
        """
        def default_on_message(
            client: Client, 
            user_data: str | None, 
            msg: MQTTMessage
        ) -> None:
            message: str = msg.payload.decode()
            topic: str = msg.topic
            print(topic, message)
        
        return default_on_message
    
    @on_message.setter
    def on_message(
        self,
        callback: Callable
    ) -> None:
        """
        Setter for the callback function called upon receiving a message from the MQTT broker.

        Args:
            callback (Callable): Callback function for handling messages.

        Returns:
            None
        """
        self.mqtt_server.on_message = callback

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
        pass
