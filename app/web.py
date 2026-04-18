from flask import Flask, render_template, request

from ai.prompts import (
    AUDIENCE_OPTIONS,
    DEFAULT_AUDIENCE_ID,
    DEFAULT_PROMPT_ID,
    PROMPT_LIBRARY,
    get_audience,
    get_prompt,
)
from app.pipeline import (
    build_material_bundle,
    generate_draft,
    get_allowed_extensions,
    get_max_document_uploads,
)
from storage.config_loader import get_config


def _build_form_state(form_data=None):
    form_data = form_data or {}

    prompt_id = form_data.get("prompt_id", DEFAULT_PROMPT_ID)
    audience_id = form_data.get("audience_id", DEFAULT_AUDIENCE_ID)

    return {
        "prompt_id": get_prompt(prompt_id)["id"],
        "audience_id": get_audience(audience_id)["id"],
        "draft_title": form_data.get("draft_title", "").strip(),
        "custom_instructions": form_data.get("custom_instructions", "").strip(),
        "pasted_text": form_data.get("pasted_text", "").strip(),
    }


def create_app():
    config = get_config()
    web_app = Flask(__name__, template_folder="templates", static_folder="static")
    web_app.config["SECRET_KEY"] = config["secret_key"]
    web_app.config["MAX_CONTENT_LENGTH"] = config["max_upload_mb"] * 1024 * 1024
    web_app.config["LRW_CONFIG"] = config

    def render_home(form_state, result=None, errors=None, status_code=200):
        return (
            render_template(
                "index.html",
                prompt_options=PROMPT_LIBRARY,
                audience_options=AUDIENCE_OPTIONS,
                active_prompt=get_prompt(form_state["prompt_id"]),
                form=form_state,
                result=result,
                errors=errors or [],
                max_upload_mb=config["max_upload_mb"],
                max_input_chars=config["max_input_chars"],
                accepted_types=", ".join(get_allowed_extensions()),
                max_document_uploads=get_max_document_uploads(),
            ),
            status_code,
        )

    @web_app.errorhandler(413)
    def payload_too_large(_error):
        form_state = _build_form_state(request.form)
        return render_home(
            form_state=form_state,
            errors=[
                f"Your upload is larger than {config['max_upload_mb']}MB. "
                "Split the materials into smaller files and try again."
            ],
            status_code=413,
        )

    @web_app.route("/", methods=["GET", "POST"])
    def index():
        form_state = _build_form_state(request.form if request.method == "POST" else None)
        result = None
        errors = []

        if request.method == "POST":
            try:
                material_bundle = build_material_bundle(
                    uploaded_files=request.files.getlist("documents"),
                    pasted_text=form_state["pasted_text"],
                    max_input_chars=config["max_input_chars"],
                )

                draft_content = generate_draft(
                    config=config,
                    material_bundle=material_bundle,
                    prompt_id=form_state["prompt_id"],
                    audience_id=form_state["audience_id"],
                    custom_instructions=form_state["custom_instructions"],
                    draft_title=form_state["draft_title"],
                )

                result = {
                    "content": draft_content,
                    "source_names": material_bundle.source_names,
                    "source_count": len(material_bundle.source_names),
                    "word_count": material_bundle.word_count,
                    "output_word_count": len(draft_content.split()),
                    "char_count": material_bundle.char_count,
                    "prompt_name": get_prompt(form_state["prompt_id"])["name"],
                    "audience_name": get_audience(form_state["audience_id"])["label"],
                    "draft_title": form_state["draft_title"] or "Untitled notes",
                }
            except ValueError as error:
                errors.append(str(error))
            except Exception:
                web_app.logger.exception("HARTSC Notemaker local generation failed")
                errors.append(
                    "Note generation failed. Check your source materials and local app configuration, then try again."
                )

        return render_home(
            form_state=form_state,
            result=result,
            errors=errors,
            status_code=400 if errors else 200,
        )

    return web_app
