import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass

from ai.prompts import get_prompt


WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'/%.-]*")
SOURCE_SEPARATOR_RE = re.compile(r"\n\s*---\s*\n")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")
DEFINITION_RE = re.compile(
    r"^(?P<term>.+?)\s+(?:is|are|refers to|means|describes|defines)\s+(?P<meaning>.+)$",
    re.IGNORECASE,
)

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "also", "am",
    "an", "and", "any", "are", "as", "at", "be", "because", "been", "before",
    "being", "below", "between", "both", "but", "by", "can", "could", "did",
    "do", "does", "doing", "down", "during", "each", "few", "for", "from",
    "further", "had", "has", "have", "having", "he", "her", "here", "hers",
    "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is",
    "it", "its", "itself", "just", "me", "more", "most", "my", "myself", "no",
    "nor", "not", "now", "of", "off", "on", "once", "only", "or", "other",
    "our", "ours", "ourselves", "out", "over", "own", "same", "she", "should",
    "so", "some", "such", "than", "that", "the", "their", "theirs", "them",
    "themselves", "then", "there", "these", "they", "this", "those", "through",
    "to", "too", "under", "until", "up", "very", "was", "we", "were", "what",
    "when", "where", "which", "while", "who", "whom", "why", "with", "would",
    "you", "your", "yours", "yourself", "yourselves",
}

PROMPT_PROFILES = {
    "smart_ai": {
        "mode": "sectioned_notes",
        "sections": [
            ("Overview", {"overview", "summary", "scope", "context", "purpose", "background"}),
            ("Key Points", {"key", "main", "important", "primary", "core", "focus"}),
            ("Supporting Details", {"detail", "evidence", "example", "data", "result", "finding"}),
            ("Takeaways", {"conclusion", "takeaway", "recommendation", "implication", "next"}),
        ],
    },
    "thesis_dissertation": {
        "mode": "sectioned_notes",
        "sections": [
            ("Research Focus", {"research", "question", "objective", "aim", "problem", "thesis"}),
            ("Method and Evidence", {"method", "methodology", "sample", "dataset", "evidence", "data"}),
            ("Findings", {"result", "finding", "analysis", "observation", "outcome"}),
            ("Conclusion and Implications", {"conclusion", "recommendation", "implication", "future", "limitation"}),
        ],
    },
    "research_paper": {
        "mode": "sectioned_notes",
        "sections": [
            ("Study Aim", {"aim", "objective", "question", "hypothesis", "purpose"}),
            ("Method", {"method", "design", "sample", "dataset", "procedure", "measure"}),
            ("Results", {"result", "finding", "effect", "trend", "evidence"}),
            ("Conclusion", {"conclusion", "interpretation", "implication", "recommendation"}),
        ],
    },
    "literature_review": {
        "mode": "sectioned_notes",
        "sections": [
            ("Key Themes", {"theme", "pattern", "trend", "topic", "recurring"}),
            ("Debates and Perspectives", {"debate", "contrast", "perspective", "argument", "view"}),
            ("Research Gaps", {"gap", "missing", "future", "limitation", "understudied"}),
            ("Notable Sources", {"source", "study", "author", "paper", "research"}),
        ],
    },
    "lecture_study_notes": {
        "mode": "sectioned_notes",
        "sections": [
            ("Main Concepts", {"concept", "idea", "topic", "principle", "theme"}),
            ("Definitions and Explanations", {"define", "definition", "means", "refers", "explains"}),
            ("Examples and Applications", {"example", "application", "case", "illustration"}),
            ("Revision Points", {"remember", "important", "key", "summary", "takeaway"}),
        ],
    },
    "textbook_chapter_notes": {
        "mode": "sectioned_notes",
        "sections": [
            ("Chapter Overview", {"chapter", "overview", "introduction", "purpose"}),
            ("Key Concepts", {"concept", "principle", "topic", "idea"}),
            ("Definitions and Examples", {"definition", "example", "illustration", "means"}),
            ("Chapter Takeaways", {"conclusion", "summary", "takeaway", "review"}),
        ],
    },
    "exam_revision_notes": {
        "mode": "sectioned_notes",
        "sections": [
            ("High-Yield Points", {"important", "key", "main", "core", "essential"}),
            ("Definitions and Rules", {"definition", "rule", "law", "formula", "term"}),
            ("Formulas and Figures", {"formula", "equation", "rate", "value", "percent"}),
            ("Quick Review", {"summary", "takeaway", "remember", "revision"}),
        ],
    },
    "flashcards_generator": {
        "mode": "flashcards",
        "sections": [],
    },
    "study_guide_generator": {
        "mode": "study_guide",
        "sections": [
            ("Core Topics", {"topic", "concept", "theme", "idea"}),
            ("Priority Review", {"important", "key", "essential", "focus"}),
            ("Suggested Study Order", {"first", "next", "then", "finally", "sequence"}),
            ("Quick Checks", {"question", "review", "check", "remember"}),
        ],
    },
    "news_article_summary": {
        "mode": "sectioned_notes",
        "sections": [
            ("Main Event", {"event", "announcement", "reported", "said", "happened"}),
            ("Timeline", {"today", "yesterday", "date", "timeline", "after", "before"}),
            ("Key Sources and Actors", {"source", "official", "said", "according", "spokesperson"}),
            ("Important Details", {"detail", "impact", "response", "context", "development"}),
        ],
    },
    "interview_notes": {
        "mode": "sectioned_notes",
        "sections": [
            ("Main Themes", {"theme", "topic", "focus", "discussion"}),
            ("Notable Quotes and Views", {"quote", "said", "believes", "argues", "explains"}),
            ("Highlights", {"important", "key", "main", "insight"}),
            ("Follow-Up Angles", {"next", "future", "plan", "question", "outlook"}),
        ],
    },
    "press_brief_summary": {
        "mode": "sectioned_notes",
        "sections": [
            ("Announcement", {"announce", "announcement", "launch", "release"}),
            ("Key Messages", {"message", "highlight", "focus", "statement"}),
            ("Supporting Facts", {"detail", "figure", "date", "timeline", "fact"}),
            ("Next Steps", {"next", "plan", "schedule", "follow-up", "implementation"}),
        ],
    },
    "media_research_notes": {
        "mode": "sectioned_notes",
        "sections": [
            ("Core Facts", {"fact", "reported", "evidence", "data"}),
            ("Context", {"background", "context", "history", "prior"}),
            ("Patterns and Insights", {"pattern", "trend", "insight", "analysis"}),
            ("Useful Angles", {"angle", "question", "implication", "follow-up"}),
        ],
    },
    "meeting_notes": {
        "mode": "sectioned_notes",
        "sections": [
            ("Purpose and Context", {"agenda", "purpose", "objective", "meeting", "context"}),
            ("Key Discussion Points", {"discussion", "topic", "issue", "point"}),
            ("Decisions", {"decided", "agreed", "approved", "resolved", "decision"}),
            ("Action Items", {"action", "owner", "deadline", "follow-up", "next"}),
        ],
    },
    "market_research_notes": {
        "mode": "sectioned_notes",
        "sections": [
            ("Market Trends", {"market", "trend", "growth", "demand", "shift"}),
            ("Competitor Signals", {"competitor", "rival", "company", "benchmark"}),
            ("Opportunities", {"opportunity", "potential", "upside", "gap"}),
            ("Risks and Constraints", {"risk", "challenge", "threat", "constraint"}),
        ],
    },
    "strategy_notes": {
        "mode": "sectioned_notes",
        "sections": [
            ("Goals", {"goal", "objective", "target", "priority"}),
            ("Initiatives", {"initiative", "plan", "project", "execution"}),
            ("Risks and Dependencies", {"risk", "dependency", "constraint", "challenge"}),
            ("Strategic Takeaways", {"takeaway", "implication", "recommendation", "outcome"}),
        ],
    },
    "financial_report_breakdown": {
        "mode": "sectioned_notes",
        "sections": [
            ("Performance Snapshot", {"revenue", "profit", "margin", "performance", "growth"}),
            ("Key KPIs", {"kpi", "metric", "ratio", "cash", "expense"}),
            ("Management Signals", {"management", "outlook", "commentary", "guidance"}),
            ("Business Takeaways", {"takeaway", "impact", "risk", "opportunity"}),
        ],
    },
    "financial_report_notes": {
        "mode": "sectioned_notes",
        "sections": [
            ("Headline Metrics", {"revenue", "profit", "margin", "cash", "expense"}),
            ("Trends", {"trend", "increase", "decrease", "change", "growth"}),
            ("Highlights", {"highlight", "important", "key", "notable"}),
            ("Risk Signals", {"risk", "pressure", "decline", "volatility", "concern"}),
        ],
    },
    "investment_research_summary": {
        "mode": "sectioned_notes",
        "sections": [
            ("Investment Thesis", {"thesis", "case", "quality", "business", "asset"}),
            ("Catalysts and Upside", {"catalyst", "upside", "growth", "driver", "opportunity"}),
            ("Risks", {"risk", "downside", "pressure", "uncertainty", "threat"}),
            ("Bottom Line", {"conclusion", "view", "takeaway", "outlook"}),
        ],
    },
    "economic_paper_summary": {
        "mode": "sectioned_notes",
        "sections": [
            ("Research Question", {"question", "aim", "objective", "paper", "study"}),
            ("Model and Assumptions", {"model", "assumption", "framework", "method", "variable"}),
            ("Results", {"result", "finding", "effect", "trend"}),
            ("Conclusions", {"conclusion", "implication", "policy", "recommendation"}),
        ],
    },
    "portfolio_analysis_notes": {
        "mode": "sectioned_notes",
        "sections": [
            ("Allocation", {"allocation", "weight", "holding", "sector", "asset"}),
            ("Performance", {"performance", "return", "gain", "loss", "benchmark"}),
            ("Risk Exposure", {"risk", "volatility", "drawdown", "exposure", "concentration"}),
            ("Notable Observations", {"note", "shift", "change", "insight", "takeaway"}),
        ],
    },
}


@dataclass
class SentenceCandidate:
    text: str
    tokens: list[str]
    source_name: str
    section_title: str
    section_key: str
    word_count: int
    score: float
    global_index: int
    position_in_section: int


class LocalNoteEngine:

    def __init__(self, reduction_ratio=0.5):
        self.reduction_ratio = max(0.1, min(float(reduction_ratio), 0.5))

    def generate(
        self,
        text,
        prompt_id,
        audience_id="general_reader",
        custom_instructions="",
        draft_title="",
    ):
        del audience_id

        prompt = get_prompt(prompt_id)
        profile = PROMPT_PROFILES.get(prompt_id, PROMPT_PROFILES["smart_ai"])
        source_word_count = self._count_source_words(text)
        if source_word_count == 0:
            return ""

        target_word_count = max(1, math.floor(source_word_count * self.reduction_ratio))
        focus_terms = self._extract_focus_terms(custom_instructions, prompt)
        candidates = self._build_candidates(text, focus_terms)
        if not candidates:
            return self._truncate_to_word_limit(text.strip(), target_word_count)

        title = (draft_title or prompt["name"]).strip()
        header_budget = self._estimate_header_words(title, profile)
        content_budget = max(1, target_word_count - header_budget)
        selected, reserve = self._select_candidates(candidates, content_budget)
        rendered = self._render_output(
            title=title,
            profile=profile,
            selected=selected,
            reserve=reserve,
            word_budget=target_word_count,
        )
        return self._truncate_to_word_limit(rendered, target_word_count)

    def _count_source_words(self, compiled_text):
        total = 0
        for _source_name, body in self._parse_sources(compiled_text):
            total += self._word_count(body)
        return total

    def _build_candidates(self, compiled_text, focus_terms):
        raw_candidates = []
        term_counter = Counter()
        global_index = 0

        for source_name, body in self._parse_sources(compiled_text):
            for section_title, section_text in self._parse_sections(body):
                section_sentences = self._split_into_sentences(section_text)
                for position, sentence in enumerate(section_sentences):
                    word_count = self._word_count(sentence)
                    if word_count < 5:
                        continue

                    tokens = self._tokens(sentence)
                    informative = [token for token in tokens if token not in STOPWORDS and len(token) > 2]
                    if not informative and word_count < 8:
                        continue

                    term_counter.update(informative)
                    raw_candidates.append(
                        {
                            "text": sentence,
                            "tokens": tokens,
                            "source_name": source_name,
                            "section_title": section_title,
                            "section_key": f"{source_name}::{section_title}",
                            "word_count": word_count,
                            "position_in_section": position,
                            "global_index": global_index,
                        }
                    )
                    global_index += 1

        if not raw_candidates:
            return []

        max_frequency = max(term_counter.values(), default=1)
        frequency_lookup = {
            term: count / max_frequency
            for term, count in term_counter.items()
        }

        candidates = []
        for candidate in raw_candidates:
            informative = [
                token
                for token in candidate["tokens"]
                if token not in STOPWORDS and len(token) > 2
            ]
            keyword_score = sum(frequency_lookup.get(token, 0.0) for token in informative)
            score = keyword_score / max(len(informative), 1)

            if candidate["position_in_section"] == 0:
                score += 0.25
            elif candidate["position_in_section"] == 1:
                score += 0.1

            if any(char.isdigit() for char in candidate["text"]):
                score += 0.15

            if ":" in candidate["text"] or ";" in candidate["text"]:
                score += 0.1

            if focus_terms and focus_terms.intersection(informative):
                score += 0.45

            title_terms = {
                token
                for token in self._tokens(candidate["section_title"])
                if token not in STOPWORDS
            }
            if title_terms.intersection(informative):
                score += 0.15

            if 8 <= len(informative) <= 28:
                score += 0.08

            candidates.append(
                SentenceCandidate(
                    text=candidate["text"],
                    tokens=candidate["tokens"],
                    source_name=candidate["source_name"],
                    section_title=candidate["section_title"],
                    section_key=candidate["section_key"],
                    word_count=candidate["word_count"],
                    score=score,
                    global_index=candidate["global_index"],
                    position_in_section=candidate["position_in_section"],
                )
            )

        return candidates

    def _select_candidates(self, candidates, content_budget):
        by_section = defaultdict(list)
        for candidate in candidates:
            by_section[candidate.section_key].append(candidate)

        selected = []
        remaining = content_budget
        selected_indices = set()

        section_best = sorted(
            (max(items, key=lambda item: item.score) for items in by_section.values()),
            key=lambda item: item.score,
            reverse=True,
        )

        for candidate in section_best:
            if candidate.word_count > remaining:
                continue
            selected.append(candidate)
            selected_indices.add(candidate.global_index)
            remaining -= candidate.word_count
            if remaining <= 0:
                break

        ranked_candidates = sorted(
            candidates,
            key=lambda item: (item.score, -item.word_count),
            reverse=True,
        )

        reserve = []
        for candidate in ranked_candidates:
            if candidate.global_index in selected_indices:
                continue

            if self._is_too_similar(candidate, selected):
                continue

            reserve.append(candidate)
            if candidate.word_count <= remaining:
                selected.append(candidate)
                selected_indices.add(candidate.global_index)
                remaining -= candidate.word_count
                if remaining <= 0:
                    break

        if not selected:
            best = max(candidates, key=lambda item: item.score)
            selected = [best]
            reserve = [candidate for candidate in ranked_candidates if candidate.global_index != best.global_index]

        selected.sort(key=lambda item: item.global_index)
        return selected, reserve

    def _render_output(self, title, profile, selected, reserve, word_budget):
        mode = profile["mode"]

        if mode == "flashcards":
            rendered = self._render_flashcards(title, selected, reserve, word_budget)
        elif mode == "study_guide":
            rendered = self._render_study_guide(title, profile, selected, word_budget)
        else:
            rendered = self._render_sectioned_notes(title, profile, selected, word_budget)

        rendered_word_count = self._word_count(rendered)
        if rendered_word_count < max(1, math.floor(word_budget * 0.75)) and reserve:
            if mode == "flashcards":
                rendered = self._render_flashcards(title, selected, reserve[:6], word_budget)
            elif mode == "study_guide":
                rendered = self._render_study_guide(title, profile, selected + reserve[:4], word_budget)
            else:
                rendered = self._render_sectioned_notes(title, profile, selected + reserve[:4], word_budget)

        return rendered

    def _render_sectioned_notes(self, title, profile, selected, word_budget):
        buckets = {section_name: [] for section_name, _keywords in profile["sections"]}
        if not buckets:
            buckets = {"Notes": []}

        section_names = list(buckets.keys())
        default_section = section_names[1] if len(section_names) > 1 else section_names[0]

        for candidate in selected:
            section_name = self._route_candidate(candidate, profile, default_section)
            buckets.setdefault(section_name, []).append(candidate)

        lines = []
        used_words = 0
        if title:
            used_words = self._append_line(lines, f"# {title}", used_words, word_budget)
            self._append_blank_line(lines)

        for section_name in section_names:
            items = buckets.get(section_name, [])
            if not items:
                continue
            candidate_lines = [f"## {section_name}"]
            for candidate in items:
                candidate_lines.append(f"- {self._format_candidate_text(candidate)}")

            added_any = False
            temp_lines = []
            temp_used = used_words
            for index, line in enumerate(candidate_lines):
                if index == 0:
                    next_used = self._append_line(temp_lines, line, temp_used, word_budget)
                    if next_used == temp_used:
                        break
                    temp_used = next_used
                    continue

                next_used = self._append_line(temp_lines, line, temp_used, word_budget)
                if next_used == temp_used:
                    break
                temp_used = next_used
                added_any = True

            if not added_any:
                continue

            lines.extend(temp_lines)
            used_words = temp_used
            self._append_blank_line(lines)

        return "\n".join(lines).strip()

    def _render_study_guide(self, title, profile, selected, word_budget):
        buckets = {section_name: [] for section_name, _keywords in profile["sections"]}
        section_names = list(buckets.keys())
        default_section = section_names[0]

        for candidate in selected:
            section_name = self._route_candidate(candidate, profile, default_section)
            buckets.setdefault(section_name, []).append(candidate)

        lines = []
        used_words = 0
        if title:
            used_words = self._append_line(lines, f"# {title}", used_words, word_budget)
            self._append_blank_line(lines)

        if buckets.get("Core Topics"):
            used_words = self._append_section_with_items(
                lines,
                "## Core Topics",
                [f"- {self._format_candidate_text(candidate)}" for candidate in buckets["Core Topics"]],
                used_words,
                word_budget,
            )

        if buckets.get("Priority Review"):
            used_words = self._append_section_with_items(
                lines,
                "## Priority Review",
                [f"- {self._format_candidate_text(candidate)}" for candidate in buckets["Priority Review"]],
                used_words,
                word_budget,
            )

        ordered_sections = []
        for candidate in selected:
            if candidate.section_title not in {"General", "Source Notes"} and candidate.section_title not in ordered_sections:
                ordered_sections.append(candidate.section_title)

        if ordered_sections:
            used_words = self._append_section_with_items(
                lines,
                "## Suggested Study Order",
                [f"{index}. {section_title}" for index, section_title in enumerate(ordered_sections, start=1)],
                used_words,
                word_budget,
            )

        quick_checks = self._make_quick_checks(selected[:4])
        if quick_checks:
            used_words = self._append_section_with_items(
                lines,
                "## Quick Checks",
                quick_checks,
                used_words,
                word_budget,
            )

        return "\n".join(lines).strip()

    def _render_flashcards(self, title, selected, reserve, word_budget):
        cards = []
        for candidate in selected + reserve:
            flashcard = self._make_flashcard(candidate)
            if not flashcard:
                continue
            if flashcard in cards:
                continue
            cards.append(flashcard)
            if len(cards) >= 12:
                break

        lines = []
        used_words = 0
        if title:
            used_words = self._append_line(lines, f"# {title}", used_words, word_budget)
            self._append_blank_line(lines)

        for index, (question, answer) in enumerate(cards, start=1):
            used_words = self._append_block(
                lines,
                [
                    f"Flashcard {index}",
                    f"Q: {question}",
                    f"A: {answer}",
                ],
                used_words,
                word_budget,
            )

        if not cards:
            fallback = selected[:6]
            for index, candidate in enumerate(fallback, start=1):
                used_words = self._append_block(
                    lines,
                    [
                        f"Flashcard {index}",
                        f"Q: What is one key point from {candidate.section_title.lower()}?",
                        f"A: {self._format_candidate_text(candidate)}",
                    ],
                    used_words,
                    word_budget,
                )

        return "\n".join(lines).strip()

    def _route_candidate(self, candidate, profile, default_section):
        best_section = default_section
        best_score = -1
        candidate_terms = {
            token
            for token in candidate.tokens + self._tokens(candidate.section_title)
            if token not in STOPWORDS
        }

        for section_name, keywords in profile["sections"]:
            score = len(candidate_terms.intersection(keywords))
            if score > best_score:
                best_score = score
                best_section = section_name

        return best_section

    def _format_candidate_text(self, candidate):
        text = re.sub(r"\s+", " ", candidate.text).strip()
        if candidate.section_title not in {"General", "Source Notes"}:
            section_title = candidate.section_title.strip()
            if section_title and section_title.lower() not in text.lower():
                if self._word_count(section_title) <= 5:
                    return f"{section_title}: {text}"
        return text

    def _make_quick_checks(self, candidates):
        checks = []
        seen = set()
        for candidate in candidates:
            section_title = candidate.section_title.lower()
            if section_title in {"general", "source notes"}:
                section_title = "the material"
            prompt = f"- Review: What is the key idea about {section_title}?"
            if prompt in seen:
                continue
            seen.add(prompt)
            checks.append(prompt)
        return checks[:4]

    def _make_flashcard(self, candidate):
        sentence = candidate.text.strip().rstrip(".")
        if not sentence:
            return None

        match = DEFINITION_RE.match(sentence)
        if match:
            term = match.group("term").strip(" :-")
            meaning = match.group("meaning").strip()
            if 1 <= self._word_count(term) <= 8:
                return (f"What is {term}?", meaning)

        if ":" in sentence:
            left, right = sentence.split(":", 1)
            if 1 <= self._word_count(left) <= 8 and self._word_count(right) >= 4:
                return (f"What should you know about {left.strip()}?", right.strip())

        if candidate.section_title not in {"General", "Source Notes"}:
            return (
                f"What is one key point about {candidate.section_title.lower()}?",
                sentence,
            )

        return (
            "What is one key point from the material?",
            sentence,
        )

    def _estimate_header_words(self, title, profile):
        words = self._word_count(title)
        mode = profile["mode"]

        if mode == "flashcards":
            return words + 18

        if mode == "study_guide":
            return words + 16

        section_names = [section_name for section_name, _keywords in profile["sections"][:4]]
        return words + sum(self._word_count(section_name) for section_name in section_names)

    def _parse_sources(self, compiled_text):
        chunks = [
            chunk.strip()
            for chunk in SOURCE_SEPARATOR_RE.split(compiled_text or "")
            if chunk.strip()
        ]
        parsed_sources = []

        for chunk in chunks:
            if chunk.startswith("Source:"):
                header, body = chunk.split("\n", 1)
                parsed_sources.append((header.replace("Source:", "", 1).strip(), body.strip()))
            else:
                parsed_sources.append(("Source", chunk.strip()))

        return parsed_sources

    def _parse_sections(self, body_text):
        sections = []
        current_title = "General"
        current_lines = []

        for raw_line in body_text.splitlines():
            line = raw_line.strip()
            if not line:
                if current_lines and current_lines[-1] != "":
                    current_lines.append("")
                continue

            if line.startswith("# "):
                if current_lines:
                    sections.append((current_title, "\n".join(current_lines).strip()))
                current_title = line[2:].strip() or "General"
                current_lines = []
                continue

            current_lines.append(line)

        if current_lines:
            sections.append((current_title, "\n".join(current_lines).strip()))

        return sections or [("General", body_text.strip())]

    def _split_into_sentences(self, text):
        sentences = []
        paragraphs = [paragraph.strip() for paragraph in re.split(r"\n{2,}", text) if paragraph.strip()]

        for paragraph in paragraphs:
            pieces = SENTENCE_SPLIT_RE.split(paragraph)
            if len(pieces) == 1:
                pieces = re.split(r";\s+", paragraph)

            for piece in pieces:
                sentence = re.sub(r"\s+", " ", piece).strip(" -")
                if sentence:
                    sentences.append(sentence)

        return sentences

    def _extract_focus_terms(self, custom_instructions, prompt):
        combined = f"{prompt['name']} {prompt['category']} {custom_instructions or ''}"
        return {
            token
            for token in self._tokens(combined)
            if token not in STOPWORDS and len(token) > 3
        }

    def _tokens(self, text):
        return [token.lower() for token in WORD_RE.findall(text or "")]

    def _word_count(self, text):
        return len(WORD_RE.findall(text or ""))

    def _is_too_similar(self, candidate, selected):
        candidate_terms = {
            token for token in candidate.tokens
            if token not in STOPWORDS and len(token) > 2
        }
        if len(candidate_terms) < 4:
            return False

        for existing in selected:
            existing_terms = {
                token for token in existing.tokens
                if token not in STOPWORDS and len(token) > 2
            }
            overlap = len(candidate_terms.intersection(existing_terms))
            if overlap / max(len(candidate_terms), 1) >= 0.8:
                return True

        return False

    def _truncate_to_word_limit(self, text, max_words):
        if self._word_count(text) <= max_words:
            return text.strip()

        lines = []
        used_words = 0

        for raw_line in text.splitlines():
            line = raw_line.rstrip()
            if not line:
                if lines and lines[-1] != "":
                    lines.append("")
                continue

            line_words = self._word_count(line)
            if used_words + line_words <= max_words:
                lines.append(line)
                used_words += line_words
                continue

            remaining = max_words - used_words
            if remaining <= 0:
                break

            prefix = ""
            content = line.strip()
            if content.startswith("- "):
                prefix = "- "
                content = content[2:]

            clipped = self._take_words(content, remaining)
            if clipped:
                lines.append(f"{prefix}{clipped}".rstrip())
            break

        return "\n".join(lines).strip()

    def _take_words(self, text, word_limit):
        if word_limit <= 0:
            return ""

        pieces = text.split()
        kept = []
        used_words = 0

        for piece in pieces:
            piece_words = self._word_count(piece)
            if piece_words == 0:
                if kept:
                    kept.append(piece)
                continue

            if used_words + piece_words > word_limit:
                break

            kept.append(piece)
            used_words += piece_words

        return " ".join(kept).strip()

    def _append_line(self, lines, line, used_words, word_budget):
        line_word_count = self._word_count(line)
        if line_word_count and used_words + line_word_count > word_budget:
            return used_words

        lines.append(line)
        return used_words + line_word_count

    def _append_blank_line(self, lines):
        if lines and lines[-1] != "":
            lines.append("")

    def _append_block(self, lines, block_lines, used_words, word_budget):
        block_word_count = sum(self._word_count(line) for line in block_lines if line)
        if block_word_count == 0:
            return used_words

        if used_words + block_word_count > word_budget:
            return used_words

        lines.extend(block_lines)
        self._append_blank_line(lines)
        return used_words + block_word_count

    def _append_section_with_items(self, lines, heading, item_lines, used_words, word_budget):
        temp_lines = []
        temp_used = self._append_line(temp_lines, heading, used_words, word_budget)
        if temp_used == used_words:
            return used_words

        added_any = False
        for line in item_lines:
            next_used = self._append_line(temp_lines, line, temp_used, word_budget)
            if next_used == temp_used:
                break
            temp_used = next_used
            added_any = True

        if not added_any:
            return used_words

        lines.extend(temp_lines)
        self._append_blank_line(lines)
        return temp_used
