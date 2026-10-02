"""요청 제출 이벤트를 기록한다. 프롬프트 본문은 저장하지 않는다."""

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


def main():
    event = json.load(sys.stdin)
    if event.get("hook_event_name") != "UserPromptSubmit":
        return

    output = Path(__file__).resolve().parents[1] / "output"
    output.mkdir(exist_ok=True)
    record = {
        "event": "UserPromptSubmit",
        "time": datetime.now(timezone.utc).isoformat(),
    }
    with (output / "hook-events.jsonl").open("a", encoding="utf-8") as log:
        log.write(json.dumps(record) + "\n")


if __name__ == "__main__":
    main()
