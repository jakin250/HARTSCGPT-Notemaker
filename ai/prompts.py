from textwrap import dedent


PROMPT_LIBRARY = [
    {
        "id": "smart_ai",
        "number": "01",
        "name": "Smart AI",
        "category": "General",
        "description": "General notes with smart structure.",
        "deliverable": "A clear set of general-purpose notes organised into the most useful sections for the source material.",
        "instructions": dedent(
            """
            Create smart notes from the supplied material.
            Organise the output into logical sections such as overview, key points, supporting details, and notable takeaways when appropriate.
            Keep the structure easy to scan and adapt the layout to the material rather than forcing a rigid template.
            Preserve important names, dates, definitions, figures, and terminology from the source.
            """
        ).strip(),
        "ui_guidance": "Best for any document when you want clear, balanced notes without a field-specific format.",
    },
    {
        "id": "thesis_dissertation",
        "number": "02",
        "name": "Thesis & Dissertation",
        "category": "Academic",
        "description": "Capture research goals, methods, and findings.",
        "deliverable": "A structured academic note set covering the research problem, objectives, methodology, findings, and conclusion.",
        "instructions": dedent(
            """
            Summarise the material as thesis or dissertation notes.
            Focus on the research problem, objectives, questions, methodology, data or evidence base, findings, limitations, and conclusion.
            Preserve discipline-specific terminology and make the scholarly argument easy to follow.
            Highlight any recommendations, implications, or future research directions that appear in the source.
            """
        ).strip(),
        "ui_guidance": "Useful for graduate research review, proposal support, and dissertation reading notes.",
    },
    {
        "id": "research_paper",
        "number": "03",
        "name": "Research Paper",
        "category": "Academic",
        "description": "Summarize studies with methods and results.",
        "deliverable": "A concise research summary covering the study aim, methods, results, and core conclusion.",
        "instructions": dedent(
            """
            Create notes for a research paper.
            Include the study aim, research question or hypothesis, method, sample or dataset, main results, interpretation, and conclusion.
            Keep methodological details accurate and distinguish reported findings from inferred implications.
            If the source includes statistics, models, or measured outcomes, preserve them clearly.
            """
        ).strip(),
        "ui_guidance": "Best for reading journal articles, empirical studies, and evidence-focused summaries.",
    },
    {
        "id": "literature_review",
        "number": "04",
        "name": "Literature Review",
        "category": "Academic",
        "description": "Track themes, gaps, and key sources.",
        "deliverable": "A literature review note set organised by themes, trends, debates, gaps, and notable sources.",
        "instructions": dedent(
            """
            Turn the material into literature review notes.
            Group the content by themes, recurring arguments, competing perspectives, research gaps, and significant sources.
            Emphasise how the sources relate to each other rather than listing isolated summaries.
            Keep the notes grounded in the supplied material and make unresolved questions explicit.
            """
        ).strip(),
        "ui_guidance": "Helpful for mapping a field quickly before writing or refining a research review.",
    },
    {
        "id": "lecture_study_notes",
        "number": "05",
        "name": "Lecture / Study Notes",
        "category": "Academic",
        "description": "Clear lecture points for study and revision.",
        "deliverable": "A study-friendly note set highlighting main concepts, explanations, examples, and revision cues.",
        "instructions": dedent(
            """
            Produce lecture or study notes from the material.
            Focus on key concepts, explanations, examples, definitions, and memorable takeaways for revision.
            Use short sections and bullet points where that improves clarity.
            Keep the notes clear enough for later review without losing important academic substance.
            """
        ).strip(),
        "ui_guidance": "Ideal for class notes, study packs, and quick revision material.",
    },
    {
        "id": "textbook_chapter_notes",
        "number": "06",
        "name": "Textbook Chapter Notes",
        "category": "Education",
        "description": "Key concepts and definitions per chapter.",
        "deliverable": "Chapter notes organised by topic with definitions, explanations, and core examples.",
        "instructions": dedent(
            """
            Summarise the material as textbook chapter notes.
            Organise the notes by chapter sections or major topics.
            Highlight key concepts, definitions, formulas, examples, and chapter takeaways.
            Preserve the teaching flow of the material so the notes still reflect how the chapter builds ideas.
            """
        ).strip(),
        "ui_guidance": "Best for compressing textbook content into clean chapter-by-chapter notes.",
    },
    {
        "id": "exam_revision_notes",
        "number": "07",
        "name": "Exam Revision Notes",
        "category": "Education",
        "description": "High-yield points and formulas.",
        "deliverable": "A compact revision sheet focused on the highest-yield ideas, formulas, and facts to memorise.",
        "instructions": dedent(
            """
            Create exam revision notes from the source material.
            Prioritise high-yield ideas, formulas, definitions, rules, and likely testable points.
            Remove low-value detail unless it is necessary for understanding.
            Present the notes in a fast-review format that supports memorisation and final revision.
            """
        ).strip(),
        "ui_guidance": "Useful when you need condensed notes for fast review before an exam.",
    },
    {
        "id": "flashcards_generator",
        "number": "08",
        "name": "Flashcards Generator",
        "category": "Education",
        "description": "Turn concepts into Q&A cards.",
        "deliverable": "A set of flashcards in clear question-and-answer format based only on the supplied material.",
        "instructions": dedent(
            """
            Convert the material into flashcards.
            Write each flashcard as a clear question followed by a concise answer.
            Focus on definitions, distinctions, formulas, processes, and important facts that suit active recall.
            Keep each card short, specific, and directly supported by the source.
            """
        ).strip(),
        "ui_guidance": "Great for turning notes or chapters into active-recall study cards.",
    },
    {
        "id": "study_guide_generator",
        "number": "09",
        "name": "Study Guide Generator",
        "category": "Education",
        "description": "Structured study plan and summaries.",
        "deliverable": "A study guide with topic summaries, priority areas, and a practical learning sequence.",
        "instructions": dedent(
            """
            Build a study guide from the supplied material.
            Include topic summaries, the most important points to master, and a sensible order for studying the content.
            Add brief review prompts or checkpoints when useful, but do not invent content beyond the source.
            Keep the guide structured, practical, and easy to follow over multiple study sessions.
            """
        ).strip(),
        "ui_guidance": "Best for turning large source bundles into a usable study roadmap.",
    },
    {
        "id": "news_article_summary",
        "number": "10",
        "name": "News Article Summary",
        "category": "Media",
        "description": "Key facts, sources, and timeline.",
        "deliverable": "A factual summary highlighting the main event, timeline, sources, and essential developments.",
        "instructions": dedent(
            """
            Summarise the material as news article notes.
            Focus on the key facts, timeline, major actors, quoted or cited sources, and the main development.
            Keep the tone factual and avoid adding speculation beyond what the material supports.
            Make the summary easy to scan for newsroom or briefing use.
            """
        ).strip(),
        "ui_guidance": "Useful for fast summaries of articles, reports, and breaking-news material.",
    },
    {
        "id": "interview_notes",
        "number": "11",
        "name": "Interview Notes",
        "category": "Media",
        "description": "Quotes, themes, and highlights.",
        "deliverable": "Interview notes organised around main themes, notable quotes, and standout insights.",
        "instructions": dedent(
            """
            Create interview notes from the supplied material.
            Capture the main themes, memorable quotes, important viewpoints, and notable moments from the speaker.
            Attribute statements clearly when the source distinguishes speakers.
            Keep the notes faithful to the speaker's message and easy to reuse for writing or production.
            """
        ).strip(),
        "ui_guidance": "Best for interviews, transcripts, and media production highlights.",
    },
    {
        "id": "press_brief_summary",
        "number": "12",
        "name": "Press Brief Summary",
        "category": "Media",
        "description": "Announcements and key messages.",
        "deliverable": "A clean press brief summary capturing announcements, key messages, and supporting details.",
        "instructions": dedent(
            """
            Summarise the material as a press brief.
            Highlight the main announcement, supporting messages, important figures, timelines, and next steps.
            Keep the output concise, factual, and suitable for editorial or stakeholder review.
            Separate confirmed details from background context where helpful.
            """
        ).strip(),
        "ui_guidance": "Helpful for press releases, statements, and official briefings.",
    },
    {
        "id": "media_research_notes",
        "number": "13",
        "name": "Media Research Notes",
        "category": "Media",
        "description": "Insights, context, and analysis.",
        "deliverable": "Research notes that combine the key facts with context, patterns, and relevant analysis from the material.",
        "instructions": dedent(
            """
            Turn the source into media research notes.
            Capture the core facts, useful context, emerging patterns, and any analysis supported by the material.
            Keep the notes practical for editorial research, background preparation, or content development.
            Make clear which points are direct facts and which are interpretive summaries grounded in the source.
            """
        ).strip(),
        "ui_guidance": "Strong fit for backgrounders, explainer prep, and context-building research.",
    },
    {
        "id": "meeting_notes",
        "number": "14",
        "name": "Meeting Notes",
        "category": "Business",
        "description": "Decisions, owners, and action items.",
        "deliverable": "Meeting notes that capture agenda points, decisions, owners, action items, and next steps.",
        "instructions": dedent(
            """
            Convert the material into meeting notes.
            Highlight the purpose of the meeting, key discussion points, decisions made, action items, owners, and deadlines if provided.
            Keep the structure practical and suitable for team follow-up.
            When speakers are identifiable, preserve attribution for important decisions or commitments.
            """
        ).strip(),
        "ui_guidance": "Best for calls, internal meetings, and stakeholder sessions where follow-through matters.",
    },
    {
        "id": "market_research_notes",
        "number": "15",
        "name": "Market Research Notes",
        "category": "Business",
        "description": "Trends, competitors, and insights.",
        "deliverable": "Market research notes covering trends, competitors, opportunities, and actionable insights.",
        "instructions": dedent(
            """
            Produce market research notes from the supplied material.
            Focus on market trends, customer signals, competitor activity, risks, opportunities, and useful insights.
            Keep the notes structured for business use and preserve any relevant metrics or comparisons in the source.
            Distinguish clearly between observed evidence and higher-level takeaways.
            """
        ).strip(),
        "ui_guidance": "Helpful for competitor scans, market briefs, and commercial opportunity reviews.",
    },
    {
        "id": "strategy_notes",
        "number": "16",
        "name": "Strategy Notes",
        "category": "Business",
        "description": "Goals, initiatives, and risks.",
        "deliverable": "Strategy notes organised around goals, initiatives, dependencies, risks, and recommended focus areas.",
        "instructions": dedent(
            """
            Summarise the material as strategy notes.
            Highlight goals, priorities, initiatives, constraints, risks, and expected outcomes.
            Keep the output decision-oriented and structured for planning or leadership review.
            Preserve the logic connecting objectives, actions, and tradeoffs where the source provides it.
            """
        ).strip(),
        "ui_guidance": "Useful for strategic plans, roadmaps, and high-level initiative tracking.",
    },
    {
        "id": "financial_report_breakdown",
        "number": "17",
        "name": "Financial Report Breakdown",
        "category": "Business",
        "description": "KPIs, performance, and takeaways.",
        "deliverable": "A business-focused breakdown of the financial report with KPIs, performance changes, and practical takeaways.",
        "instructions": dedent(
            """
            Break down the financial report into business-ready notes.
            Focus on key metrics, performance trends, major changes, management commentary, and practical takeaways.
            Make the output easy for non-specialist stakeholders to follow while keeping the numbers accurate.
            Call out strengths, pressure points, and notable business implications supported by the material.
            """
        ).strip(),
        "ui_guidance": "Best for stakeholder-friendly summaries of company financial performance.",
    },
    {
        "id": "financial_report_notes",
        "number": "18",
        "name": "Financial Report Notes",
        "category": "Finance",
        "description": "Metrics, trends, and highlights.",
        "deliverable": "Finance notes capturing the report's most important metrics, trend lines, and highlights.",
        "instructions": dedent(
            """
            Summarise the material as financial report notes.
            Highlight revenue, costs, margins, profitability, cash flow, balance sheet signals, and notable trends where available.
            Preserve important figures accurately and make comparisons clear when the source provides them.
            Keep the tone analytical and focused on what matters most in the report.
            """
        ).strip(),
        "ui_guidance": "Useful for earnings reports, annual reports, and finance-focused review.",
    },
    {
        "id": "investment_research_summary",
        "number": "19",
        "name": "Investment Research Summary",
        "category": "Finance",
        "description": "Thesis, risks, and upside drivers.",
        "deliverable": "An investment summary covering the core thesis, risks, catalysts, and upside or downside drivers.",
        "instructions": dedent(
            """
            Create an investment research summary from the supplied material.
            Focus on the investment thesis, business or asset quality, valuation signals if present, risks, catalysts, and upside or downside drivers.
            Keep the analysis disciplined and grounded in the source rather than adding outside assumptions.
            Present both supporting and cautionary points clearly.
            """
        ).strip(),
        "ui_guidance": "Best for research notes, screening summaries, and investment memo prep.",
    },
    {
        "id": "economic_paper_summary",
        "number": "20",
        "name": "Economic Paper Summary",
        "category": "Finance",
        "description": "Models, assumptions, and conclusions.",
        "deliverable": "A summary of the economic paper covering the research question, model, assumptions, results, and conclusion.",
        "instructions": dedent(
            """
            Summarise the material as an economic paper review.
            Highlight the research question, model or framework, assumptions, data, findings, and conclusion.
            Preserve technical language where needed, but explain the analytical flow clearly.
            Call out policy or market implications only when the source supports them.
            """
        ).strip(),
        "ui_guidance": "Helpful for economics reading, policy analysis, and model-focused summaries.",
    },
    {
        "id": "portfolio_analysis_notes",
        "number": "21",
        "name": "Portfolio Analysis Notes",
        "category": "Finance",
        "description": "Allocation, risk, and performance.",
        "deliverable": "Portfolio notes covering allocation, performance, risk exposures, and notable observations.",
        "instructions": dedent(
            """
            Turn the material into portfolio analysis notes.
            Focus on asset allocation, diversification, performance, risk exposures, benchmarks, and notable shifts or drivers.
            Keep the summary precise and preserve percentages, rankings, and comparisons from the source.
            Present the notes in a format that helps a reviewer understand portfolio positioning quickly.
            """
        ).strip(),
        "ui_guidance": "Useful for portfolio reviews, client updates, and investment monitoring notes.",
    },
]

AUDIENCE_OPTIONS = [
    {
        "id": "general_reader",
        "label": "General Reader",
        "description": "Explain clearly in plain language while keeping the structure clean and useful.",
    },
    {
        "id": "student",
        "label": "Student",
        "description": "Keep the output study-friendly, well-organised, and easy to revise later.",
    },
    {
        "id": "researcher",
        "label": "Researcher",
        "description": "Preserve method, evidence, and nuance with a clear analytical structure.",
    },
    {
        "id": "educator",
        "label": "Educator",
        "description": "Present the material in a teaching-ready format with strong clarity and sequence.",
    },
    {
        "id": "media_professional",
        "label": "Media Professional",
        "description": "Write concisely, preserve attribution, and keep the output factual and easy to scan.",
    },
    {
        "id": "business_professional",
        "label": "Business Professional",
        "description": "Keep the output practical, action-oriented, and focused on decisions and follow-up.",
    },
    {
        "id": "financial_analyst",
        "label": "Financial Analyst",
        "description": "Use an analytical tone that preserves metrics, trends, and risk signals accurately.",
    },
    {
        "id": "executive",
        "label": "Executive",
        "description": "Focus on the highest-signal insights, implications, and decisions with minimal clutter.",
    },
]

PROMPT_LOOKUP = {prompt["id"]: prompt for prompt in PROMPT_LIBRARY}
AUDIENCE_LOOKUP = {audience["id"]: audience for audience in AUDIENCE_OPTIONS}

DEFAULT_PROMPT_ID = PROMPT_LIBRARY[0]["id"]
DEFAULT_AUDIENCE_ID = AUDIENCE_OPTIONS[0]["id"]

SYSTEM_PROMPT = dedent(
    """
    You are XAI Notemaker, an AI assistant for turning source materials into clear, structured notes.
    Ground every statement in the supplied source materials.
    Never invent facts, quotations, dates, figures, citations, or references.
    If the source material does not support a point, say so directly.
    Adapt tone and depth to the selected audience.
    Use clear headings, lists, tables, and structure where that improves readability.
    Preserve important terminology, names, timelines, and metrics from the source.
    """
).strip()


def get_prompt(prompt_id):
    return PROMPT_LOOKUP.get(prompt_id, PROMPT_LOOKUP[DEFAULT_PROMPT_ID])


def get_audience(audience_id):
    return AUDIENCE_LOOKUP.get(audience_id, AUDIENCE_LOOKUP[DEFAULT_AUDIENCE_ID])


def build_messages(prompt_id, text, audience_id, custom_instructions="", draft_title=""):
    prompt = get_prompt(prompt_id)
    audience = get_audience(audience_id)

    prompt_sections = [
        f"Selected Notemaker style: {prompt['number']}. {prompt['name']}",
        f"Department: {prompt['category']}",
        f"Required deliverable: {prompt['deliverable']}",
        f"Audience: {audience['label']}",
        f"Audience guidance: {audience['description']}",
        "Mandatory drafting instructions:",
        prompt["instructions"],
    ]

    if draft_title.strip():
        prompt_sections.append(f"Document title or note label: {draft_title.strip()}")

    if custom_instructions.strip():
        prompt_sections.append(
            "Additional user instructions:\n"
            f"{custom_instructions.strip()}"
        )

    prompt_sections.extend(
        [
            "Use only the source materials below.",
            text.strip(),
        ]
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "\n\n".join(prompt_sections)},
    ]
