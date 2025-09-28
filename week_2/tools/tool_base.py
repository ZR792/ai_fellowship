from typing import Generator

class Tool:
    description: str = "No description provided"

    def run(self, input: str) -> Generator[str, None, None]:
        raise NotImplementedError("You must implement the `run` method in your tool subclass.")