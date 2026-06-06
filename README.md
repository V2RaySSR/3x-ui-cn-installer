<div align="center">

# 3x-ui v2.9.3 中文固定版

配合 V2RaySSR 视频教程使用的 3x-ui 中文一键安装脚本。

[![Version](https://img.shields.io/badge/3x--ui-v2.9.3-2f81f7?style=for-the-badge)](https://github.com/V2RaySSR/3x-ui-cn-installer/releases/tag/v2.9.3-cn)
[![Installer](https://img.shields.io/badge/installer-Chinese-238636?style=for-the-badge)](install-cn.sh)
[![Mode](https://img.shields.io/badge/mode-fixed_version-6e7681?style=for-the-badge)](README.md)
[![Release](https://img.shields.io/badge/assets-self_hosted-8957e5?style=for-the-badge)](https://github.com/V2RaySSR/3x-ui-cn-installer/releases/tag/v2.9.3-cn)

</div>

## 一键安装

```bash
bash <(curl -Ls https://raw.githubusercontent.com/V2RaySSR/3x-ui-cn-installer/main/install-cn.sh)
```

## 项目说明

| 项目 | 说明 |
| --- | --- |
| 固定版本 | `3x-ui v2.9.3` |
| 教程时间 | 2026 年 4 月 30 日录制教程时使用的版本 |
| 安装脚本 | [`install-cn.sh`](install-cn.sh) |
| 管理菜单 | [`x-ui-cn.sh`](x-ui-cn.sh) |
| 固定资源 | [`v2.9.3-cn`](https://github.com/V2RaySSR/3x-ui-cn-installer/releases/tag/v2.9.3-cn) |
| 适合用户 | 第一次搭建、正在跟着视频操作的新手朋友 |

这个仓库现在只做一件事：保存并提供视频教程同款的 `3x-ui v2.9.3` 中文固定版。

如果你是第一次搭建，或者你是跟着我的视频一步一步操作，推荐你直接使用这个版本。这样你看到的安装流程、面板界面、按钮位置和视频里基本一致，不会因为官方新版大改界面而突然对不上。

## 为什么固定版本

官方项目一直在更新，这是好事，但对新手来说也会带来一个问题：教程录制时是一个界面，过一段时间官方新版可能变成另一个界面。你跟着视频操作时，如果按钮名字、菜单位置、安装流程都变了，就很容易卡住。

所以本仓库不再追随官方最新版，而是固定保存视频教程同款版本：

| 固定内容 | 状态 |
| --- | --- |
| 面板版本 | 固定为 `3x-ui v2.9.3` |
| 中文安装脚本 | 固定为仓库根目录 `install-cn.sh` |
| 中文管理菜单 | 固定为仓库根目录 `x-ui-cn.sh` |
| 安装资源 | 固定保存在本仓库 Release |
| 自动同步官方脚本 | 已移除 |
| 自动翻译官方最新版 | 已移除 |

简单说：如果你是小白，想要和视频里的步骤一致，就用这个仓库。

## 固定资源

本仓库已经把 `v2.9.3` 当时发布的安装包保存到自己的 Release 里。安装脚本下载面板时，会从 `V2RaySSR/3x-ui-cn-installer` 自己的 Release 获取资源，不再依赖官方仓库的最新版接口，也不再去官方仓库拉安装脚本或服务文件。

| 类型 | 文件 |
| --- | --- |
| Linux 安装包 | `x-ui-linux-amd64.tar.gz` |
| Linux 安装包 | `x-ui-linux-arm64.tar.gz` |
| Linux 安装包 | `x-ui-linux-386.tar.gz` |
| Linux 安装包 | `x-ui-linux-armv5.tar.gz` |
| Linux 安装包 | `x-ui-linux-armv6.tar.gz` |
| Linux 安装包 | `x-ui-linux-armv7.tar.gz` |
| Linux 安装包 | `x-ui-linux-s390x.tar.gz` |
| Windows 安装包 | `x-ui-windows-amd64.zip` |
| Geo 数据文件 | `geoip.dat` / `geosite.dat` |
| Geo 数据文件 | `geoip_IR.dat` / `geosite_IR.dat` |
| Geo 数据文件 | `geoip_RU.dat` / `geosite_RU.dat` |
| Alpine 服务脚本 | `assets/x-ui.rc` |

文件校验值见 [`CHECKSUMS.sha256`](CHECKSUMS.sha256)。

## 给有基础的朋友

如果你已经熟悉 Linux、Xray、Reality 协议和面板配置，也可以自行尝试官方更新的版本。只是新版的界面、菜单和教程里的步骤可能不同，需要你自己判断。

如果你是第一次安装，建议先不要追新。先跟着视频把环境跑通，比一上来研究最新版变化更稳。

## 仓库文件

| 文件 | 用途 |
| --- | --- |
| [`install-cn.sh`](install-cn.sh) | 中文固定版一键安装脚本 |
| [`x-ui-cn.sh`](x-ui-cn.sh) | 安装后的中文 `x-ui` 管理菜单 |
| [`assets/x-ui.rc`](assets/x-ui.rc) | Alpine/OpenRC 服务脚本 |
| [`CHECKSUMS.sha256`](CHECKSUMS.sha256) | 固定资源的 sha256 校验值 |

## 官方项目

本仓库是为了配合 V2RaySSR 视频教程而整理的中文固定版。官方原项目地址如下：

[`MHSanaei/3x-ui`](https://github.com/MHSanaei/3x-ui)
