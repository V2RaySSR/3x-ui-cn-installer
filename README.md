# 3x-ui v2.9.3 中文固定版安装脚本

这是配合 V2RaySSR 视频教程使用的 3x-ui 中文固定版安装脚本。

如果你是第一次搭建，或者你是跟着我的视频一步一步操作，推荐你直接使用这个版本。这个仓库固定的是我在 **2026 年 4 月 30 日录制教程时使用的 3x-ui v2.9.3**，这样你看到的安装流程、面板界面、按钮位置和视频里基本一致，不会因为官方新版大改界面而突然对不上。

## 一键安装

```bash
bash <(curl -Ls https://raw.githubusercontent.com/V2RaySSR/3x-ui-cn-installer/main/install-cn.sh)
```

## 为什么固定这个版本

官方项目一直在更新，这是好事，但对新手来说也会带来一个问题：教程录制时是一个界面，过一段时间官方新版可能变成另一个界面。你跟着视频操作时，如果按钮名字、菜单位置、安装流程都变了，就很容易卡住。

所以这个仓库不再追随官方最新版，而是固定保存视频教程同款版本：

- 固定面板版本：`3x-ui v2.9.3`
- 固定中文安装脚本：`install-cn.sh`
- 固定中文管理菜单：`x-ui-cn.sh`
- 固定安装资源：保存在本仓库的 `v2.9.3-cn` Release
- 不再自动同步官方脚本
- 不再自动翻译官方最新版

简单说：如果你是小白，想要和视频里的步骤一致，就用这个仓库。

## 固定资源说明

本仓库已经把 `v2.9.3` 当时发布的安装包保存到自己的 Release 里。安装脚本下载面板时，会从 `V2RaySSR/3x-ui-cn-installer` 自己的 Release 获取资源，不再依赖官方仓库的最新版接口，也不再去官方仓库拉安装脚本或服务文件。

已固定保存的资源包括：

- `x-ui-linux-amd64.tar.gz`
- `x-ui-linux-arm64.tar.gz`
- `x-ui-linux-386.tar.gz`
- `x-ui-linux-armv5.tar.gz`
- `x-ui-linux-armv6.tar.gz`
- `x-ui-linux-armv7.tar.gz`
- `x-ui-linux-s390x.tar.gz`
- `x-ui-windows-amd64.zip`
- `geoip.dat` / `geosite.dat`
- `geoip_IR.dat` / `geosite_IR.dat`
- `geoip_RU.dat` / `geosite_RU.dat`
- `assets/x-ui.rc`

文件校验值见 [`CHECKSUMS.sha256`](CHECKSUMS.sha256)。

## 给有基础的朋友

如果你已经熟悉 Linux、Xray、Reality 协议和面板配置，也可以自行尝试官方更新的版本。只是新版的界面、菜单和教程里的步骤可能不同，需要你自己判断。

如果你是第一次安装，建议先不要追新。先跟着视频把环境跑通，比一上来研究最新版变化更稳。

## 仓库文件

- `install-cn.sh`：中文固定版一键安装脚本
- `x-ui-cn.sh`：安装后的中文 `x-ui` 管理菜单
- `assets/x-ui.rc`：Alpine/OpenRC 服务脚本
- `CHECKSUMS.sha256`：固定资源的 sha256 校验值

这个仓库现在只做一件事：保存并提供视频教程同款的 3x-ui v2.9.3 中文固定版。
