import codecs
import json
import logging
import uuid
from argparse import ArgumentParser
from typing import Text

from sanic import Blueprint, Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse

# -----------------------------------------------------------------------
# Global Definitions and Constants
# -----------------------------------------------------------------------
from core.personas import Personas

logger = logging.getLogger()


class ErrorResponse(Exception):
    def __init__(self, status, reason, message, details=None, help_url=None):
        self.error_info = {
            "version": "0.1.0",
            "status": "failure",
            "message": message,
            "reason": reason,
            "details": details or {},
            "help": help_url,
            "code": status,
        }
        self.status = status


# -----------------------------------------------------------------------
# Chatbot Server Class Definition
# -----------------------------------------------------------------------
class ChatbotServer:

    def __init__(self, config=None):
        if not config:
            logger.error("config not found!")

        logging.info("Loading Config from: {}".format(config))
        with codecs.open(config, 'r', encoding='utf-8') as f:
            cfgs = json.loads(f.read())
        self.persons_model = {}
        for person in cfgs:
            id = person.get("id", 1)
            name = person.get("name", "default")
            persona = person.get("persona", "你是一个上知天文下知地理的博学之士")
            model = Personas(persona)
            self.persons_model[id] = {
                "name": name,
                "model": model
            }

    def blueprint(
            self
    ) -> Blueprint:

        chatbot_webhook = Blueprint('name', url_prefix='/chatbot')

        @chatbot_webhook.route("/health", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @chatbot_webhook.route("/persona", methods=["POST"])
        async def persona(request: Request) -> HTTPResponse:
            id = str(uuid.uuid1())
            try:
                name = request.json.get("name", "default")
                persona = request.json.get("persona", "你是一个上知天文下知地理的博学之士")
                model = Personas(persona)
                self.persons_model[id] = {
                    "name": name,
                    "model": model
                }
            except Exception as e:
                raise ErrorResponse(
                    400, "InitPersonaError", f"An unexpected error occurred. Error: {e}"
                )
            resp = {"id": id,
                    "name": name,
                    "persona": persona}
            return response.json(resp)

        @chatbot_webhook.route("/reply", methods=["POST"])
        async def parse(request: Request) -> HTTPResponse:
            try:
                id = request.json.get("id", None)
                message = request.json.get("message", None)
                if len(message.strip()) == 0:
                    return response.json({"response": "你没有输入任何文字"})

                model = self.persons_model.get(id, None)
                if model is None or id is None:
                    return response.json({"response": "请指定正确的角色id"})

                reply = model["model"].predict(message)
                logger.info("message: {} \nreply result:{}".format(message, reply))

            except Exception as e:
                raise ErrorResponse(
                    400, "ParsingError", f"An unexpected error occurred. Error: {e}"
                )

            return response.json({"response": reply})

        return chatbot_webhook


# -----------------------------------------------------------------------
# Create Server App.
# -----------------------------------------------------------------------
def create_app(agent):
    app = Sanic(name="chatbot")
    app.config.RESPONSE_TIMEOUT = 60 * 60
    app.config.KEEP_ALIVE = False
    app.blueprint(agent.blueprint())

    return app


# -----------------------------------------------------------------------
# Main Function
# -----------------------------------------------------------------------
if __name__ == '__main__':
    # -------------------------------------------------------------------
    # Parse all cmd line args.
    # -------------------------------------------------------------------
    p = ArgumentParser()
    p.add_argument('-p', '--port', help='Port to host on', default=5007, type=int)
    p.add_argument('-c', '--config', help='Config path', default="./config/persona.json", type=Text)
    args = p.parse_args()

    # -------------------------------------------------------------------
    # Create a Chatbot Server and corresponding app, and run it.
    # -------------------------------------------------------------------
    chatbot = ChatbotServer(args.config)
    app = create_app(chatbot)
    app.run(host="0.0.0.0", port=args.port, debug=False)
