# 3x-ui 中文安装器

这个仓库用于自动同步官方 [3x-ui](https://github.com/MHSanaei/3x-ui) 安装脚本，并生成中文本地化安装脚本。

项目原则很简单：

- 只汉化安装过程中的交互提示、菜单文字、状态文字
- 不修改官方安装脚本的核心逻辑
- 通过 GitHub Actions 自动跟随官方更新
- 官方脚本变化后自动生成中文脚本并创建 PR，方便人工确认

## 使用方式

```bash
bash <(curl -Ls https://raw.githubusercontent.com/V2RaySSR/3x-ui-cn-installer/main/generated/install-cn.sh)
```

## 目录说明

```text
3x-ui-cn-installer/
├── README.md
├── translations.yml
├── scripts/translate.py
├── upstream/install.sh
├── generated/install-cn.sh
└── .github/workflows/sync.yml
```

说明：

- `translations.yml`：中文翻译映射表
- `scripts/translate.py`：根据翻译映射生成中文安装脚本
- `upstream/install.sh`：自动同步的官方原始安装脚本
- `generated/install-cn.sh`：生成后的中文安装脚本，最终用户执行这个文件
- `.github/workflows/sync.yml`：自动同步、自动生成、自动创建 PR

## 本地生成

先获取官方安装脚本：

```bash
curl -L https://raw.githubusercontent.com/MHSanaei/3x-ui/master/install.sh -o upstream/install.sh
```

然后生成中文脚本：

```bash
python3 scripts/translate.py
```

生成结果会写入：

```text
generated/install-cn.sh
```

## 翻译规则

翻译内容统一维护在 `translations.yml`。

每条翻译包含：

```yaml
- 原文: "Install"
  译文: "安装"
```

脚本生成时会按顺序做文本替换。为了尽量减少误改，建议优先添加完整提示语，而不是过短的单词。

## 自动同步

GitHub Actions 会在每天自动运行，也可以在仓库页面手动触发。

自动流程：

1. 拉取官方最新版 `install.sh`
2. 使用 `translations.yml` 生成 `generated/install-cn.sh`
3. 如果内容有变化，自动创建一个 PR

## 维护原则

这个仓库只做中文本地化，不承诺修改安装逻辑。

如果官方脚本发生较大变化，优先更新 `translations.yml`，而不是直接编辑 `generated/install-cn.sh`。
