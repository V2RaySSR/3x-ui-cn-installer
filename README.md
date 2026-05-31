# 3x-ui 中文安装器

[![CI](https://github.com/V2RaySSR/3x-ui-cn-installer/actions/workflows/sync.yml/badge.svg?branch=main&label=CI)](https://github.com/V2RaySSR/3x-ui-cn-installer/actions/workflows/sync.yml)

自动同步官方 [3x-ui](https://github.com/MHSanaei/3x-ui) 安装脚本，并生成中文本地化安装脚本。

本项目只做一件事：

> 保持官方安装逻辑不变，仅汉化安装过程中的交互提示、菜单文字和状态文字。

## 中文安装 3x-ui

<!-- sync-info:start -->
### 最近一次官方同步状态

- 官方来源：`MHSanaei/3x-ui` 的 `main` 分支
- 官方 commit：`b1c141a515da`
- 同步时间：`2026-06-01 01:42:02 CST`
- 官方脚本变更：`install.sh +0 -0`，`x-ui.sh +0 -0`
- 未翻译用户可见文案：`0` 条
- 校验状态：`通过，未修改官方安装逻辑`
- 详细状态：[`generated/sync-status.md`](generated/sync-status.md)
<!-- sync-info:end -->

```bash
bash <(curl -Ls https://raw.githubusercontent.com/V2RaySSR/3x-ui-cn-installer/latest/generated/install-cn.sh)
```

## 文件说明

- `generated/install-cn.sh`：中文安装脚本，用户直接执行这个文件
- `generated/x-ui-cn.sh`：安装后的中文 `x-ui` 管理脚本
- `generated/metadata.json`：最近一次官方同步和中文生成时间
- `generated/sync-status.md`：完整同步记录，README 首页只展示最近一次
- `upstream/install.sh`：同步自官方的原始安装脚本
- `upstream/x-ui.sh`：同步自官方的原始管理脚本
- `translations.yml`：中文翻译映射表
- `scripts/translate.py`：中文脚本生成器，包含中文菜单宽度排版逻辑
- `scripts/validate.py`：生成结果验证器
- `.github/workflows/sync.yml`：自动同步和 PR 工作流

## 自动更新

仓库每天自动检查官方安装脚本。

如果官方脚本发生变化，GitHub Actions 会自动：

1. 同步官方最新版 `install.sh` 和 `x-ui.sh`
2. 重新生成 `generated/install-cn.sh` 和 `generated/x-ui-cn.sh`
3. 执行发布前校验
4. 自动更新 `latest` 分支，用户安装命令会立即使用新版
5. 同时创建同步 PR，便于后续补充翻译并合并到 `main`

`main` 用于人工审核和归档，`latest` 用于自动发布给用户。
