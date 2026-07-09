from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from app.schemas.timeline import TimelineAnswer
from app.schemas.timeline import TimelineBuildRequest
from app.schemas.timeline import TimelineEvent


class TimelineService:
    _time_prefix = re.compile(
        r"^\s*(?P<time>(?:\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APap][Mm])?))\s*[-:]\s*(?P<event>.+)$"
    )
    _inline_time = re.compile(
        r"\b(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APap][Mm])?)\b"
    )

    def build(
        self,
        answers: list[TimelineAnswer | dict[str, Any] | str] | TimelineBuildRequest,
    ) -> list[dict[str, Any]]:
        items = self._coerce_answers(answers)
        timeline: list[TimelineEvent] = []

        for index, item in enumerate(items):
            timeline.extend(self._events_from_answer(item, index))

        timeline.sort(key=self._sort_key)
        return [event.model_dump(mode="json") for event in timeline]

    def _coerce_answers(
        self,
        answers: list[TimelineAnswer | dict[str, Any] | str] | TimelineBuildRequest,
    ) -> list[TimelineAnswer | dict[str, Any] | str]:
        if isinstance(answers, TimelineBuildRequest):
            return answers.answers
        return answers

    def _events_from_answer(
        self,
        answer: TimelineAnswer | dict[str, Any] | str,
        fallback_order: int,
    ) -> list[TimelineEvent]:
        if isinstance(answer, TimelineAnswer):
            payload = answer.model_dump()
        elif isinstance(answer, dict):
            payload = answer
        else:
            payload = {"answer": answer}

        source = self._normalize_text(
            payload.get("source")
            or payload.get("question")
            or "chatbot_answer"
        )

        text = self._normalize_text(
            payload.get("event")
            or payload.get("answer")
            or payload.get("text")
            or ""
        )

        if not text:
            return []

        pieces = self._split_into_events(text)
        explicit_timestamp = payload.get("timestamp")
        order = int(payload.get("order") or fallback_order)

        events: list[TimelineEvent] = []
        for offset, piece in enumerate(pieces):
            time_label, event_text = self._parse_event(piece)
            if explicit_timestamp is not None and not time_label:
                time_label = self._format_timestamp(explicit_timestamp)

            events.append(
                TimelineEvent(
                    time=time_label,
                    event=event_text,
                    source=source,
                    order=order * 100 + offset,
                )
            )

        return events

    def _split_into_events(self, text: str) -> list[str]:
        lines = [
            self._normalize_text(line)
            for line in re.split(r"[\n\r;]+", text)
        ]
        return [line for line in lines if line]

    def _parse_event(self, text: str) -> tuple[str | None, str]:
        match = self._time_prefix.match(text)
        if match:
            return match.group("time"), self._normalize_text(match.group("event"))

        inline = self._inline_time.search(text)
        if inline:
            time_label = inline.group("time")
            event_text = self._normalize_text(
                text[: inline.start()] + text[inline.end() :]
            )
            return time_label, event_text

        return None, text

    def _sort_key(self, event: TimelineEvent) -> tuple[int, str, int]:
        parsed_time = self._parse_time_label(event.time)
        if parsed_time is None:
            return (1, "", event.order)
        return (0, parsed_time, event.order)

    def _parse_time_label(self, value: str | None) -> str | None:
        if not value:
            return None
        candidate = value.strip().upper().replace(" ", "")
        formats = ("%H:%M:%S", "%H:%M", "%I:%M:%S%p", "%I:%M%p")
        for time_format in formats:
            try:
                parsed = datetime.strptime(candidate, time_format)
                return parsed.strftime("%H:%M:%S")
            except ValueError:
                continue
        return candidate

    def _format_timestamp(self, value: Any) -> str | None:
        if isinstance(value, datetime):
            return value.strftime("%H:%M:%S")

        if isinstance(value, str):
            parsed = self._parse_time_label(value)
            return parsed

        return None

    def _normalize_text(self, text: Any) -> str:
        if not isinstance(text, str):
            return ""
        return re.sub(r"\s+", " ", text).strip()

