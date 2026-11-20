# telegram-language-pack

Telegram 客户端简体中文语言包，纯文本，可自行校验与修改。
Simplified Chinese language pack for Telegram. Plain text, verifiable, forkable.

[![validate](https://github.com/zxrui87-hub/telegram-language-pack/actions/workflows/validate.yml/badge.svg)](../../actions/workflows/validate.yml)

---

## 这是什么

一份 Telegram 界面文案的键值对照表。应用后只替换界面文字，**不修改客户端、不改版本号、不接触账号**。

| 项目 | 说明 |
|---|---|
| 格式 | UTF-8 JSON，无 BOM |
| 体积 | 小于 20 KB |
| 内容 | `name` / `version` / `updated` / `strings` 四个字段 |
| 许可 | 语言包文本 CC0-1.0，脚本 MIT |

## 文件

```
pack/tg-zh-hans-v0.1.json     语言包本体
scripts/verify.py             校验脚本（结构、BOM、重复键、哈希）
CHANGELOG.md                  版本记录
.github/workflows/validate.yml 提交时自动校验
```

## 用法

```bash
git clone https://github.com/zxrui87-hub/telegram-language-pack.git
cd telegram-language-pack
python scripts/verify.py pack/tg-zh-hans-v0.1.json
```

输出示例：

```
file      pack/tg-zh-hans-v0.1.json
size      560 B
sha256    e32a57d04bddb0fcf9dd709b881e24b05505cf7b14168c1caad2d1825f0b040e
keys      12
encoding  utf-8 (no BOM)
result    OK
```

在 Telegram 中应用：`设置 → 语言 → 添加语言`，或通过语言包链接导入。详细步骤见
[tg-cn.example/install](https://telegramtike.com/install.html)。

## 校验脚本做什么

1. 拒绝带 BOM 的文件（客户端会解析失败）
2. 检查四个必需字段
3. 检测重复键（JSON 解析器默认静默覆盖，脚本会报错）
4. 检查所有值是非空字符串
5. 输出 SHA-256 与体积，便于和发布页比对

退出码：`0` 通过，`1` 失败。可直接用于 CI。

## 自己改一版

```bash
cp pack/tg-zh-hans-v0.1.json pack/tg-zh-hans-v0.2.json
# 改 strings 里的值，键名保持不变
python scripts/verify.py pack/tg-zh-hans-v0.2.json
```

键名由客户端定义，**改键名等于让这一条失效**。命名规则见
[语言包说明](https://telegramtike.com/language-pack.html)。

## 参与翻译

见 [CONTRIBUTING.md](CONTRIBUTING.md)。提 PR 前请先跑一次 `verify.py`，CI 也会跑。

## 为什么只提供文本包

重新打包的"中文版客户端"会把登录凭证暴露给第三方代码，二次签名后还无法正常更新。
文本包能解决的问题，不需要用安装包解决。完整说明：
[为什么没有单独的 Telegram 中文版](https://telegramtike.com/why.html)。

## License

- `pack/*.json`：CC0-1.0（公共领域）
- `scripts/*`：MIT

---

### English

A plain-text Simplified Chinese language pack for Telegram. Applying it only replaces UI
strings — it does not modify the client, change its version, or touch your account.

Run `python scripts/verify.py pack/tg-zh-hans-v0.1.json` to check encoding (no BOM),
required fields, duplicate keys, and to print the SHA-256 for comparison with the
[published checksum](https://telegramtike.com/download.html).

Text-only by design: repackaged "Chinese edition" clients route your login through
third-party code and break official updates.
