from ai.local_engine import LocalNoteEngine


class AIClient:
    """
    Compatibility shim for older imports.
    The app now uses a local note engine and does not call the OpenAI API.
    """

    def __init__(self, *_args, **_kwargs):
        self.engine = LocalNoteEngine(reduction_ratio=0.5)

    def chat(self, *_args, **_kwargs):
        raise RuntimeError(
            "AIClient.chat is no longer used. The web app now generates notes locally without API credits."
        )
