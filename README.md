# 3x-ui 中文安装器

[![CI](https://github.com/V2RaySSR/3x-ui-cn-installer/actions/workflows/sync.yml/badge.svg?branch=main&label=CI)](https://github.com/V2RaySSR/3x-ui-cn-installer/actions/workflows/sync.yml)

自动同步官方 [3x-ui](https://github.com/MHSanaei/3x-ui) 安装脚本，并生成中文本地化安装脚本。

本项目只做一件事：

> 保持官方安装逻辑不变，仅汉化安装过程中的交互提示、菜单文字和状态文字。

## 中文安装 3x-ui

<!-- sync-info:start -->
官方脚本同步时间：`2026-04-29 09:16:22 CST`
中文脚本生成时间：`2026-04-29 09:16:22 CST`
<!-- sync-info:end -->

```bash
bash <(curl -Ls https://raw.githubusercontent.com/V2RaySSR/3x-ui-cn-installer/latest/generated/install-cn.sh)
```

## 文件说明

- `generated/install-cn.sh`：中文安装脚本，用户直接执行这个文件
- `generated/x-ui-cn.sh`：安装后的中文 `x-ui` 管理脚本
- `generated/metadata.json`：最近一次官方同步和中文生成时间
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
