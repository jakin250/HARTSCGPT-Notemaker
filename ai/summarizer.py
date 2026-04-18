from ai.local_engine import LocalNoteEngine


class DraftGenerator:

    def __init__(self, config):
        self.engine = LocalNoteEngine(
            reduction_ratio=config.get("note_reduction_ratio", 0.5)
        )

    def generate(
        self,
        text,
        prompt_id,
        audience_id,
        custom_instructions="",
        draft_title="",
    ):
        return self.engine.generate(
            text=text,
            prompt_id=prompt_id,
            audience_id=audience_id,
            custom_instructions=custom_instructions,
            draft_title=draft_title,
        )


class LegalDraftGenerator(DraftGenerator):
    pass


class Summarizer(DraftGenerator):
    pass
