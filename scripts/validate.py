#!/usr/bin/env python3
"""验证生成的中文安装脚本是否安全、可发布。"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import translate


项目根目录 = Path(__file__).resolve().parents[1]
默认上游脚本 = 项目根目录 / "upstream" / "install.sh"
默认生成脚本 = 项目根目录 / "generated" / "install-cn.sh"
默认上游管理脚本 = 项目根目录 / "upstream" / "x-ui.sh"
默认生成管理脚本 = 项目根目录 / "generated" / "x-ui-cn.sh"
默认报告 = 项目根目录 / "i18n-report.md"

英文提示模式 = re.compile(r"[A-Za-z][A-Za-z ]{3,}")
变量含中文模式 = re.compile(r"\$\{[^}]*[\u4e00-\u9fff][^}]*\}")

允许英文片段 = (
    "ACME",
    "API",
    "Arch",
    "Cert",
    "CPU",
    "ED25519",
    "Fail2ban",
    "GitHub",
    "HTTP",
    "IP",
    "IPv4",
    "IPv6",
    "Key",
    "Let's Encrypt",
    "Reloadcmd",
    "SSL",
    "WebBasePath",
    "acme.sh",
    "cron",
    "curl",
    "etckeeper",
    "fullchain",
    "https",
    "nginx",
    "privatekey",
    "privkey",
    "rc-service",
    "reloadcmd",
    "root",
    "systemctl",
    "systemd",
    "tar.gz",
    "x-ui",
    "arch",
    "armv",
)


def 去除生成文件头(内容: str) -> str:
    行列表 = 内容.splitlines(keepends=True)
    if len(行列表) >= 4 and 行列表[0].startswith("#!") and "自动生成" in 行列表[1]:
        return 行列表[0] + "".join(行列表[4:])
    return 内容


def 输出区域标记(内容: str) -> list[bool]:
    标记: list[bool] = []
    多行输出中 = False

    for 行 in 内容.splitlines(keepends=True):
        当前是输出 = 多行输出中 or translate.是输出语句(行)
        标记.append(当前是输出)

        if translate.是多行输出起点(行) or (多行输出中 and translate.双引号数量为奇数(行)):
            多行输出中 = not 多行输出中

    return 标记


def 检查非输出逻辑未改变(上游内容: str, 生成内容: str) -> list[str]:
    问题: list[str] = []
    上游行 = 上游内容.splitlines(keepends=True)
    生成行 = 去除生成文件头(生成内容).splitlines(keepends=True)
    标记 = 输出区域标记(上游内容)

    if len(上游行) != len(生成行):
        return [f"行数不一致：官方 {len(上游行)} 行，生成脚本 {len(生成行)} 行"]

    for 行号, (原行, 新行, 可翻译) in enumerate(zip(上游行, 生成行, 标记), start=1):
        if not 可翻译 and 原行 != 新行:
            if 是允许的下载地址替换(原行, 新行):
                continue
            问题.append(f"第 {行号} 行非输出逻辑发生变化")
            if len(问题) >= 20:
                问题.append("非输出逻辑变化超过 20 处，已停止继续列出")
                break

    return 问题


def 是允许的下载地址替换(原行: str, 新行: str) -> bool:
    官方地址 = "https://raw.githubusercontent.com/MHSanaei/3x-ui/main/x-ui.sh"
    中文地址 = "https://raw.githubusercontent.com/V2RaySSR/3x-ui-cn-installer/main/generated/x-ui-cn.sh"
    return 官方地址 in 原行 and 中文地址 in 新行 and 原行.replace(官方地址, 中文地址) == 新行


def 检查_bash_语法(路径: Path) -> str | None:
    结果 = subprocess.run(["bash", "-n", str(路径)], text=True, capture_output=True)
    if 结果.returncode != 0:
        return 结果.stderr.strip() or 结果.stdout.strip() or "bash -n 检查失败"
    return None


def 检查变量未被汉化(内容: str) -> list[str]:
    问题: list[str] = []
    for 行号, 行 in enumerate(内容.splitlines(), start=1):
        if 变量含中文模式.search(行):
            问题.append(f"第 {行号} 行 Bash 变量中出现中文：{行.strip()}")
    return 问题


def 检查菜单边框对齐(内容: str) -> list[str]:
    匹配列表 = list(re.finditer(r"[┌╔][^\n]+\n.*?[└╚][─]+[┘╝]", 内容, re.S))
    if not 匹配列表:
        return ["未找到菜单边框，无法验证菜单对齐"]

    for 序号, 匹配 in enumerate(匹配列表, start=1):
        行列表 = 匹配.group(0).splitlines()
        宽度列表 = [显示宽度(去除_ansi_占位符(行)) for 行 in 行列表]
        if len(set(宽度列表)) != 1:
            return [f"第 {序号} 个菜单边框未对齐，行宽为：{宽度列表}"]
    return []


def 去除_ansi_占位符(文本: str) -> str:
    return re.sub(r"\$\{[^}]+\}", "", 文本)


def 显示宽度(文本: str) -> int:
    宽度 = 0
    for 字符 in 文本:
        if unicodedata.combining(字符):
            continue
        宽度 += 2 if unicodedata.east_asian_width(字符) in {"F", "W"} else 1
    return 宽度


def 提取可能未翻译文案(生成内容: str) -> list[str]:
    结果: list[str] = []
    已见: set[str] = set()
    标记 = 输出区域标记(去除生成文件头(生成内容))

    for 行, 是输出 in zip(去除生成文件头(生成内容).splitlines(), 标记):
        if not 是输出:
            continue
        if "grep -q" in 行 or "echo \"$" in 行 or "echo \"${" in 行:
            continue
        候选 = 清理输出行(行)
        if not 候选:
            continue
        if not 英文提示模式.search(候选):
            continue
        if all(片段 not in 候选 for 片段 in 允许英文片段):
            if 候选 not in 已见:
                结果.append(候选)
                已见.add(候选)

    return 结果


def 清理输出行(行: str) -> str:
    内容 = 提取引号内容(行.strip())
    if 内容 is None:
        return ""
    内容 = re.sub(r"\$\{[^}]+\}", "", 内容)
    内容 = re.sub(r"\$[A-Za-z_][A-Za-z0-9_]*", "", 内容)
    内容 = re.sub(r"\\033\[[^']+", "", 内容)
    内容 = re.sub(r"\\n|\\t", " ", 内容)
    内容 = re.sub(r"[│┌┐└┘─═#]+", " ", 内容)
    内容 = re.sub(r"\s+", " ", 内容)
    内容 = 内容.strip(" '\"")
    return 内容


def 提取引号内容(行: str) -> str | None:
    起点 = None
    引号 = None
    for 索引, 字符 in enumerate(行):
        if 字符 in {"'", '"'}:
            起点 = 索引 + 1
            引号 = 字符
            break
    if 起点 is None or 引号 is None:
        return None

    结果: list[str] = []
    转义中 = False
    for 字符 in 行[起点:]:
        if 转义中:
            结果.append(字符)
            转义中 = False
            continue
        if 字符 == "\\":
            转义中 = True
            结果.append(字符)
            continue
        if 字符 == 引号:
            break
        结果.append(字符)
    return "".join(结果)


def 写报告(路径: Path, 未翻译: list[str], 阻断问题: list[str]) -> None:
    行列表 = [
        "# 中文安装脚本同步报告",
        "",
        "## 验证结果",
        "",
    ]

    if 阻断问题:
        行列表.append("发现阻断问题：")
        行列表.extend(f"- {问题}" for 问题 in 阻断问题)
    else:
        行列表.append("- 生成脚本语法检查通过")
        行列表.append("- 非输出逻辑与官方脚本保持一致")
        行列表.append("- 未发现 Bash 变量被中文误替换")
        行列表.append("- 命令菜单边框显示宽度一致")

    行列表.extend(["", "## 可能需要补充翻译的文案", ""])
    if 未翻译:
        行列表.extend(f"- `{文案}`" for 文案 in 未翻译)
    else:
        行列表.append("- 暂未发现明显未翻译的用户可见英文文案")

    路径.write_text("\n".join(行列表) + "\n", encoding="utf-8")


def main() -> int:
    解析器 = argparse.ArgumentParser(description="验证生成的中文安装脚本")
    解析器.add_argument("--upstream", type=Path, default=默认上游脚本)
    解析器.add_argument("--generated", type=Path, default=默认生成脚本)
    解析器.add_argument("--report", type=Path, default=默认报告)
    参数 = 解析器.parse_args()

    上游内容 = 参数.upstream.read_text(encoding="utf-8")
    生成内容 = 参数.generated.read_text(encoding="utf-8")

    阻断问题: list[str] = []
    阻断问题.extend(检查非输出逻辑未改变(上游内容, 生成内容))
    阻断问题.extend(检查变量未被汉化(生成内容))
    阻断问题.extend(检查菜单边框对齐(生成内容))

    if 默认上游管理脚本.exists() and 默认生成管理脚本.exists():
        上游管理内容 = 默认上游管理脚本.read_text(encoding="utf-8")
        生成管理内容 = 默认生成管理脚本.read_text(encoding="utf-8")
        阻断问题.extend(f"管理脚本：{问题}" for 问题 in 检查非输出逻辑未改变(上游管理内容, 生成管理内容))
        阻断问题.extend(f"管理脚本：{问题}" for 问题 in 检查变量未被汉化(生成管理内容))
        阻断问题.extend(f"管理脚本：{问题}" for 问题 in 检查菜单边框对齐(生成管理内容))

    语法问题 = 检查_bash_语法(参数.generated)
    if 语法问题:
        阻断问题.append(f"生成脚本语法错误：{语法问题}")
    if 默认生成管理脚本.exists():
        管理脚本语法问题 = 检查_bash_语法(默认生成管理脚本)
        if 管理脚本语法问题:
            阻断问题.append(f"管理脚本语法错误：{管理脚本语法问题}")

    未翻译 = 提取可能未翻译文案(生成内容)
    写报告(参数.report, 未翻译, 阻断问题)

    if 未翻译:
        print(f"发现 {len(未翻译)} 条可能需要补充翻译的文案，详见：{参数.report}")
    else:
        print("未发现明显未翻译的用户可见英文文案")

    if 阻断问题:
        print("验证失败：")
        for 问题 in 阻断问题:
            print(f"- {问题}")
        return 1

    print("验证通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
