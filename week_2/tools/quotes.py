from tools.tool_base import Tool  

from typing import Generator

class MotivationTool(Tool):
    description = "Provides a motivational quote"

    def run(self, input: str) -> Generator[str, None, None]:
        quotes = [
            "Push yourself, because no one else is going to do it for you.",
            "Success doesn’t just find you. You have to go out and get it.",
            "Dream bigger. Do bigger.",
            "Don’t stop when you’re tired. Stop when you’re done.",
        ]
        import random
        yield random.choice(quotes)