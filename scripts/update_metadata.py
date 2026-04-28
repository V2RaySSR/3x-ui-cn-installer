#!/usr/bin/env python3
"""更新同步元数据，并写入 README 展示区块。"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


项目根目录 = Path(__file__).resolve().parents[1]
元数据路径 = 项目根目录 / "generated" / "metadata.json"
README路径 = 项目根目录 / "README.md"
开始标记 = "<!-- sync-info:start -->"
结束标记 = "<!-- sync-info:end -->"


def 当前时间() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S CST")


def main() -> int:
    时间 = os.environ.get("SYNC_TIME") or 当前时间()
    元数据 = {
        "official_script_synced_at": 时间,
        "chinese_script_generated_at": 时间,
        "timezone": "Asia/Shanghai",
    }

    元数据路径.parent.mkdir(parents=True, exist_ok=True)
    元数据路径.write_text(json.dumps(元数据, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    内容 = README路径.read_text(encoding="utf-8")
    新区块 = "\n".join(
        [
            开始标记,
            f"官方脚本同步时间：`{时间}`",
            f"中文脚本生成时间：`{时间}`",
            结束标记,
        ]
    )

    if 开始标记 in 内容 and 结束标记 in 内容:
        前半段 = 内容.split(开始标记, 1)[0].rstrip()
        后半段 = 内容.split(结束标记, 1)[1].lstrip()
        内容 = f"{前半段}\n\n{新区块}\n\n{后半段}"
    else:
        标题 = "## 中文安装 3x-ui"
        内容 = 内容.replace(标题, f"{标题}\n\n{新区块}", 1)

    with README路径.open("w", encoding="utf-8", newline="\n") as 文件:
        文件.write(内容)
    print(f"已更新同步元数据：{时间}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
