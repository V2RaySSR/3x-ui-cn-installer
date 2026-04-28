#!/usr/bin/env python3
"""根据 translations.yml 生成中文安装脚本。"""

from __future__ import annotations

import argparse
import os
import re
import stat
import sys
import unicodedata
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


项目根目录 = Path(__file__).resolve().parents[1]
默认上游脚本 = 项目根目录 / "upstream" / "install.sh"
默认翻译表 = 项目根目录 / "translations.yml"
默认输出脚本 = 项目根目录 / "generated" / "install-cn.sh"


def 读取翻译表(路径: Path) -> list[dict[str, str]]:
    with 路径.open("r", encoding="utf-8") as 文件:
        文本 = 文件.read()

    if yaml is None:
        return 读取简单翻译表(文本)

    数据 = yaml.safe_load(文本) or {}

    替换列表 = 数据.get("替换")
    if not isinstance(替换列表, list):
        raise ValueError("translations.yml 必须包含列表字段：替换")

    结果: list[dict[str, str]] = []
    for 序号, 项 in enumerate(替换列表, start=1):
        if not isinstance(项, dict):
            raise ValueError(f"第 {序号} 条翻译必须是对象")
        原文 = 项.get("原文")
        译文 = 项.get("译文")
        if not isinstance(原文, str) or not isinstance(译文, str):
            raise ValueError(f"第 {序号} 条翻译必须包含字符串字段：原文、译文")
        if 原文 == "":
            raise ValueError(f"第 {序号} 条翻译的原文不能为空")
        结果.append({"原文": 原文, "译文": 译文})

    return 结果


def 读取简单翻译表(文本: str) -> list[dict[str, str]]:
    结果: list[dict[str, str]] = []
    当前: dict[str, str] = {}

    for 行 in 文本.splitlines():
        去空白 = 行.strip()
        if not 去空白 or 去空白.startswith("#") or 去空白 == "替换:":
            continue
        if 去空白.startswith("- 原文:"):
            if 当前:
                结果.append(校验简单翻译项(当前, len(结果) + 1))
            当前 = {"原文": 去引号(去空白.removeprefix("- 原文:").strip())}
        elif 去空白.startswith("译文:"):
            当前["译文"] = 去引号(去空白.removeprefix("译文:").strip())

    if 当前:
        结果.append(校验简单翻译项(当前, len(结果) + 1))

    return 结果


def 去引号(值: str) -> str:
    if len(值) >= 2 and 值[0] == 值[-1] and 值[0] in {"'", '"'}:
        return 值[1:-1]
    return 值


def 校验简单翻译项(项: dict[str, str], 序号: int) -> dict[str, str]:
    原文 = 项.get("原文")
    译文 = 项.get("译文")
    if not 原文 or 译文 is None:
        raise ValueError(f"第 {序号} 条翻译必须包含：原文、译文")
    return {"原文": 原文, "译文": 译文}


def 生成中文脚本(原始内容: str, 翻译列表: list[dict[str, str]]) -> str:
    行列表 = []
    多行输出中 = False
    翻译列表 = sorted(翻译列表, key=lambda 项: len(项["原文"]), reverse=True)

    for 行 in 原始内容.splitlines(keepends=True):
        应翻译 = 多行输出中 or 是输出语句(行)
        if 应翻译:
            for 项 in 翻译列表:
                行 = 行.replace(项["原文"], 项["译文"])
        行列表.append(行)

        if 是多行输出起点(行) or (多行输出中 and 双引号数量为奇数(行)):
            多行输出中 = not 多行输出中

    内容 = "".join(行列表)
    内容 = 格式化中文命令菜单(内容)

    文件头 = """# 此文件由 scripts/translate.py 自动生成，请不要直接编辑。
# 如需调整中文内容，请修改 translations.yml 后重新生成。

"""
    if 内容.startswith("#!"):
        第一行, 分隔符, 剩余内容 = 内容.partition("\n")
        return f"{第一行}\n{文件头}{剩余内容 if 分隔符 else ''}"
    return 文件头 + 内容


def 格式化中文命令菜单(内容: str) -> str:
    菜单模式 = re.compile(
        r'echo -e "┌───────────────────────────────────────────────────────┐\n'
        r'│  \$\{blue\}x-ui 控制菜单用法（子命令）：\$\{plain\}.*?'
        r'└───────────────────────────────────────────────────────┘"',
        re.S,
    )
    return 菜单模式.sub(生成中文命令菜单源码(), 内容)


def 生成中文命令菜单源码() -> str:
    命令列表 = [
        ("x-ui", "管理脚本"),
        ("x-ui start", "启动"),
        ("x-ui stop", "停止"),
        ("x-ui restart", "重启"),
        ("x-ui status", "当前状态"),
        ("x-ui settings", "当前设置"),
        ("x-ui enable", "启用开机自启"),
        ("x-ui disable", "禁用开机自启"),
        ("x-ui log", "查看日志"),
        ("x-ui banlog", "查看 Fail2ban 封禁日志"),
        ("x-ui update", "更新"),
        ("x-ui legacy", "旧版"),
        ("x-ui install", "安装"),
        ("x-ui uninstall", "卸载"),
    ]
    内宽 = 63
    命令列宽 = 24
    标题 = "x-ui 控制菜单用法（子命令）："
    行列表 = [f'echo -e "┌{"─" * 内宽}┐']
    行列表.append(f"│  ${{blue}}{标题}${{plain}}{空格(内宽 - 2 - 显示宽度(标题))}│")
    行列表.append(f"│{空格(内宽)}│")

    for 命令, 说明 in 命令列表:
        左侧 = f"  ${{blue}}{命令}${{plain}}"
        左侧宽度 = 2 + 显示宽度(命令)
        中间空格数 = 命令列宽 - 左侧宽度
        文本宽度 = 左侧宽度 + 中间空格数 + 2 + 显示宽度(说明)
        行列表.append(f"│{左侧}{空格(中间空格数)}- {说明}{空格(内宽 - 文本宽度)}│")

    行列表.append(f'└{"─" * 内宽}┘"')
    return "\n".join(行列表)


def 显示宽度(文本: str) -> int:
    宽度 = 0
    for 字符 in 文本:
        if unicodedata.combining(字符):
            continue
        宽度 += 2 if unicodedata.east_asian_width(字符) in {"F", "W"} else 1
    return 宽度


def 空格(数量: int) -> str:
    return " " * max(0, 数量)


def 是输出语句(行: str) -> bool:
    return re.search(r"(^|\s)(echo|printf)\b", 行) is not None or re.search(r"(^|\s)read\s+(-[A-Za-z]+\s+)*['\"]", 行) is not None


def 是多行输出起点(行: str) -> bool:
    return 是输出语句(行) and 双引号数量为奇数(行)


def 双引号数量为奇数(行: str) -> bool:
    数量 = 0
    转义中 = False
    for 字符 in 行:
        if 转义中:
            转义中 = False
            continue
        if 字符 == "\\":
            转义中 = True
            continue
        if 字符 == '"':
            数量 += 1
    return 数量 % 2 == 1


def 设置可执行权限(路径: Path) -> None:
    当前权限 = 路径.stat().st_mode
    路径.chmod(当前权限 | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main() -> int:
    解析器 = argparse.ArgumentParser(description="生成 3x-ui 中文安装脚本")
    解析器.add_argument("--upstream", type=Path, default=默认上游脚本, help="官方原始 install.sh 路径")
    解析器.add_argument("--translations", type=Path, default=默认翻译表, help="中文翻译表路径")
    解析器.add_argument("--output", type=Path, default=默认输出脚本, help="生成的中文脚本路径")
    参数 = 解析器.parse_args()

    if not 参数.upstream.exists():
        print(f"找不到官方安装脚本：{参数.upstream}", file=sys.stderr)
        return 1

    原始内容 = 参数.upstream.read_text(encoding="utf-8")
    翻译列表 = 读取翻译表(参数.translations)
    中文内容 = 生成中文脚本(原始内容, 翻译列表)

    参数.output.parent.mkdir(parents=True, exist_ok=True)
    with 参数.output.open("w", encoding="utf-8", newline="\n") as 文件:
        文件.write(中文内容)
    设置可执行权限(参数.output)

    print(f"已生成中文安装脚本：{参数.output}")
    print(f"已应用翻译条目：{len(翻译列表)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
