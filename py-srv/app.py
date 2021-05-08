import asyncio

from flask import Flask, jsonify

from events.listener.post_created import PostCreatedListener
from events.publisher.user_created import UserCreatedPublisher
from pub_sub import PubSubClient
from redis_client import NewRedisClient


def main():
    app = Flask(__name__)
    rdb = NewRedisClient()
    pubsub = PubSubClient(rdb)

    PostCreatedListener(pubsub).listen()

    @app.route('/')
    def hello_world():
        UserCreatedPublisher(pubsub).publish({"id": 1, "name": "Kiran PY"})
        return jsonify({"msg": "Hello, World!"})

    app.run(debug=False, host='0.0.0.0', port=9000)


if __name__ == '__main__':
    main()
