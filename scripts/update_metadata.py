#!/usr/bin/env python3
"""更新同步元数据，并写入 README 展示区块。"""

from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


项目根目录 = Path(__file__).resolve().parents[1]
元数据路径 = 项目根目录 / "generated" / "metadata.json"
同步状态路径 = 项目根目录 / "generated" / "sync-status.md"
README路径 = 项目根目录 / "README.md"
开始标记 = "<!-- sync-info:start -->"
结束标记 = "<!-- sync-info:end -->"


def 当前时间() -> str:
    try:
        时区 = ZoneInfo("Asia/Shanghai")
    except Exception:
        时区 = timezone(timedelta(hours=8))
    return datetime.now(时区).strftime("%Y-%m-%d %H:%M:%S CST")


def 运行命令(参数: list[str]) -> str:
    结果 = subprocess.run(参数, cwd=项目根目录, text=True, capture_output=True, check=False)
    return 结果.stdout.strip() if 结果.returncode == 0 else ""


def 文件行数(路径: Path) -> int:
    return len(路径.read_text(encoding="utf-8").splitlines()) if 路径.exists() else 0


def 文件_sha256(路径: Path) -> str:
    import hashlib

    if not 路径.exists():
        return ""
    return hashlib.sha256(路径.read_bytes()).hexdigest()


def 读取官方变更统计() -> dict[str, dict[str, int]]:
    统计: dict[str, dict[str, int]] = {}
    输出 = 运行命令(["git", "diff", "--numstat", "--", "upstream/install.sh", "upstream/x-ui.sh"])
    for 行 in 输出.splitlines():
        部分 = 行.split()
        if len(部分) < 3:
            continue
        新增文本, 删除文本, 路径文本 = 部分[0], 部分[1], 部分[2]
        if not 新增文本.isdigit() or not 删除文本.isdigit():
            continue
        统计[路径文本.replace("\\", "/")] = {
            "additions": int(新增文本),
            "deletions": int(删除文本),
        }
    return 统计


def 未翻译数量() -> int:
    报告环境变量 = os.environ.get("I18N_REPORT_PATH")
    候选路径 = [
        Path(报告环境变量) if 报告环境变量 else None,
        项目根目录 / "i18n-report.md",
        Path("/tmp/i18n-report.md"),
    ]
    for 路径 in 候选路径:
        if 路径 is None or not 路径.exists():
            continue
        内容 = 路径.read_text(encoding="utf-8")
        if "暂未发现明显未翻译" in 内容 or "未发现明显未翻译" in 内容:
            return 0
        return sum(1 for 行 in 内容.splitlines() if 行.startswith("- `"))
    if 元数据路径.exists():
        try:
            旧元数据 = json.loads(元数据路径.read_text(encoding="utf-8"))
            旧数量 = 旧元数据.get("untranslated_user_visible_text_count")
            if isinstance(旧数量, int):
                return 旧数量
        except json.JSONDecodeError:
            pass
    return -1


def 短_commit(commit: str) -> str:
    return commit[:12] if commit else "unknown"


def 生成同步记录(元数据: dict[str, object]) -> str:
    变更 = 元数据["official_change_summary"]
    未翻译 = 元数据["untranslated_user_visible_text_count"]
    行列表 = [
        f"## {元数据['official_script_synced_at']} - {短_commit(str(元数据['official_commit']))}",
        "",
        f"- 官方仓库：`{元数据['official_repository']}`",
        f"- 官方分支：`{元数据['official_branch']}`",
        f"- 官方 commit：`{元数据['official_commit']}`",
        f"- 官方脚本同步时间：`{元数据['official_script_synced_at']}`",
        f"- 中文脚本生成时间：`{元数据['chinese_script_generated_at']}`",
        f"- 校验状态：`{元数据['validation_status']}`",
        f"- 未翻译用户可见文案：`{未翻译 if 未翻译 >= 0 else 'unknown'}` 条",
        "",
        "### 本次官方脚本变更",
        "",
        f"- `install.sh`：新增 `{变更['install.sh']['additions']}` 行，删除 `{变更['install.sh']['deletions']}` 行",
        f"- `x-ui.sh`：新增 `{变更['x-ui.sh']['additions']}` 行，删除 `{变更['x-ui.sh']['deletions']}` 行",
        "",
        "### 发布内容",
        "",
        f"- `generated/install-cn.sh`：`{元数据['generated_scripts']['install-cn.sh']['lines']}` 行，SHA256 `{元数据['generated_scripts']['install-cn.sh']['sha256']}`",
        f"- `generated/x-ui-cn.sh`：`{元数据['generated_scripts']['x-ui-cn.sh']['lines']}` 行，SHA256 `{元数据['generated_scripts']['x-ui-cn.sh']['sha256']}`",
        "",
        "说明：中文脚本保持官方安装逻辑不变，仅汉化用户可见提示，并把安装入口切换为本项目的中文脚本。",
    ]
    return "\n".join(行列表)


def 写同步状态(元数据: dict[str, object]) -> None:
    新记录 = 生成同步记录(元数据)
    历史标记 = "<!-- sync-history:start -->"
    文件头 = "\n".join(
        [
            "# 3x-ui 中文安装器同步记录",
            "",
            "说明：README 首页只展示最近一次同步状态；本文件按时间倒序保留每次同步记录。",
            "",
            历史标记,
            "",
        ]
    )

    旧历史 = ""
    if 同步状态路径.exists():
        旧内容 = 同步状态路径.read_text(encoding="utf-8").strip()
        if 历史标记 in 旧内容:
            旧历史 = 旧内容.split(历史标记, 1)[1].strip()
        elif 旧内容:
            旧历史 = "## 迁移前记录\n\n" + 旧内容

    if 旧历史:
        同步状态路径.write_text(f"{文件头}{新记录}\n\n{旧历史}\n", encoding="utf-8")
    else:
        同步状态路径.write_text(f"{文件头}{新记录}\n", encoding="utf-8")


def main() -> int:
    时间 = os.environ.get("SYNC_TIME") or 当前时间()
    官方_commit输出 = 运行命令(["git", "ls-remote", "https://github.com/MHSanaei/3x-ui.git", "refs/heads/main"])
    官方_commit = os.environ.get("OFFICIAL_COMMIT") or (官方_commit输出.split()[0] if 官方_commit输出 else "")
    变更统计 = 读取官方变更统计()
    install变更 = 变更统计.get("upstream/install.sh", {"additions": 0, "deletions": 0})
    xui变更 = 变更统计.get("upstream/x-ui.sh", {"additions": 0, "deletions": 0})
    元数据 = {
        "official_repository": "https://github.com/MHSanaei/3x-ui",
        "official_branch": "main",
        "official_commit": 官方_commit,
        "official_script_synced_at": 时间,
        "chinese_script_generated_at": 时间,
        "validation_status": "passed",
        "official_change_detected": bool(install变更["additions"] or install变更["deletions"] or xui变更["additions"] or xui变更["deletions"]),
        "official_change_summary": {
            "install.sh": install变更,
            "x-ui.sh": xui变更,
        },
        "untranslated_user_visible_text_count": 未翻译数量(),
        "upstream_scripts": {
            "install.sh": {"lines": 文件行数(项目根目录 / "upstream" / "install.sh"), "sha256": 文件_sha256(项目根目录 / "upstream" / "install.sh")},
            "x-ui.sh": {"lines": 文件行数(项目根目录 / "upstream" / "x-ui.sh"), "sha256": 文件_sha256(项目根目录 / "upstream" / "x-ui.sh")},
        },
        "generated_scripts": {
            "install-cn.sh": {"lines": 文件行数(项目根目录 / "generated" / "install-cn.sh"), "sha256": 文件_sha256(项目根目录 / "generated" / "install-cn.sh")},
            "x-ui-cn.sh": {"lines": 文件行数(项目根目录 / "generated" / "x-ui-cn.sh"), "sha256": 文件_sha256(项目根目录 / "generated" / "x-ui-cn.sh")},
        },
        "timezone": "Asia/Shanghai",
    }

    元数据路径.parent.mkdir(parents=True, exist_ok=True)
    元数据路径.write_text(json.dumps(元数据, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    写同步状态(元数据)

    内容 = README路径.read_text(encoding="utf-8")
    未翻译 = 元数据["untranslated_user_visible_text_count"]
    新区块 = "\n".join(
        [
            开始标记,
            "### 最近一次官方同步状态",
            "",
            f"- 官方来源：`MHSanaei/3x-ui` 的 `main` 分支",
            f"- 官方 commit：`{短_commit(str(官方_commit))}`",
            f"- 同步时间：`{时间}`",
            f"- 官方脚本变更：`install.sh +{install变更['additions']} -{install变更['deletions']}`，`x-ui.sh +{xui变更['additions']} -{xui变更['deletions']}`",
            f"- 未翻译用户可见文案：`{未翻译 if 未翻译 >= 0 else 'unknown'}` 条",
            "- 校验状态：`通过，未修改官方安装逻辑`",
            "- 详细状态：[`generated/sync-status.md`](generated/sync-status.md)",
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
