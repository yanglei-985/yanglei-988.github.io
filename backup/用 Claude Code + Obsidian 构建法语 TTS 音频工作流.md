# 用 Claude Code + Obsidian 构建法语 TTS 音频工作流

从零到一的完整搭建教程

> **最终效果**：在 Obsidian 里选中一段法语，说一句【生成音频】，Claude Code 自动合成语音并将 `![[audio.mp3]]` 插入当前笔记。

---

## 第一章：这个工作流是什么？

在正式动手之前，先搞清楚我们要做什么，以及为什么要这样做。

### 1.1 工作流的最终效果

安装完成后，你的使用方式非常简单：

1. 在 Obsidian 打开一篇笔记
2. 在终端的 Claude Code 里输入：`生成音频 Bonjour, comment allez-vous ?`
3. 等待几秒钟
4. 笔记末尾自动出现 `![[bonjour_20260410.mp3]]`，点击即可播放

### 1.2 底层原理：四个角色的分工

整个系统由四个部分协作完成，就像一个流水线工厂：

| 角色 | 技术名称 | 负责的事情 |
|------|--------|---------|
| 大脑 | Claude Code + Skill | 理解你的指令，决定调用哪个脚本、怎么调用 |
| 嘴巴 | edge-tts (微软神经语音) | 把文字转成逼真的法语语音 MP3 |
| 门卫 | Obsidian Local REST API | 接收外部请求，把内容写入笔记 |
| 仓库 | Obsidian Vault 文件系统 | 存储音频文件和笔记内容 |

### 1.3 数据是怎么流动的？

当你说【生成音频 Bonjour】，背后发生了以下五个步骤：

1. **你输入指令** → Claude Code 识别到【生成音频】触发词，读取 `obsidian-french-tts` 这个 skill 的说明书（SKILL.md）

2. **调用 Python 脚本** → 根据说明书，Claude Code 在终端执行 `tts_generate.py`，把法语文本发给微软 edge-tts 服务

3. **语音合成** → edge-tts 通过网络请求微软服务器，返回 MP3 音频，保存到 Obsidian vault 的 `assets/audio/` 文件夹

4. **写入笔记** → Claude Code 通过 curl 命令，向 Obsidian 的本地 API（端口 27123）发送请求，告诉它在当前打开的笔记末尾追加 `![[文件名.mp3]]`

5. **完成** → Obsidian 收到请求，笔记里出现音频嵌入，点击即可播放

---

## 第二章：安装前的准备

### 2.1 需要什么软件？

在开始之前，确保你的电脑上已经安装以下软件：

- Claude Code（命令行版本）
- Obsidian 笔记软件
- Python 3.8 或更高版本
- 网络连接（edge-tts 需要访问微软服务器）

### 2.2 安装 edge-tts

edge-tts 是微软提供的文字转语音库，通过 pip 安装。

在 Ubuntu 24.04 上，系统会阻止直接安装：

```bash
pip install edge-tts
```

会报错：`error: externally-managed-environment`

**解决方法**：加上 `--break-system-packages` 参数强制安装：

```bash
pip install edge-tts --break-system-packages
```

> **为什么会报这个错？**
> 
> Ubuntu 24.04 引入了 PEP 668 保护机制，防止 pip 污染系统 Python 环境。加上 `--break-system-packages` 参数可以绕过这个保护，适合个人工作环境。

### 2.3 在 Obsidian 安装 Local REST API 插件

这个插件让外部程序（Claude Code）能够控制 Obsidian。

**安装步骤**：

1. 打开 Obsidian → 设置（齿轮图标）
2. 选择「第三方插件」→ 关闭「安全模式」
3. 点击「浏览」→ 搜索「Local REST API」
4. 安装并启用
5. 进入插件设置，找到 API Key（一串长字符），复制保存
6. 开启「Enable Non-encrypted (HTTP) Server」开关（默认是关的！）

> ⚠️ **注意**：HTTP 开关默认是关闭的，必须手动打开，否则 curl 会报「连接被拒绝」错误。

---

## 第三章：安装 Skill

### 3.1 什么是 Skill？

Claude Code 的 Skill 是一本「说明书」，放在 `~/.claude/skills/` 目录下。当你输入某些触发词时，Claude Code 会自动读取对应的说明书，按照里面的步骤执行操作。

`obsidian-french-tts` 这个 skill 包含两个文件：

- **SKILL.md**：说明书，告诉 Claude Code 整个工作流怎么执行
- **scripts/tts_generate.py**：Python 脚本，负责调用 edge-tts 生成音频

### 3.2 安装步骤

下载 `obsidian-french-tts.skill` 文件后，在终端执行：

```bash
claude skills add ~/Downloads/obsidian-french-tts.skill
```

**验证安装成功**：

```bash
claude skills list
```

看到 `obsidian-french-tts` 出现在列表里即为成功。

---

## 第四章：配置环境变量

### 4.1 什么是环境变量？

环境变量是操作系统提供的一种「全局配置」机制。就像你把常用的电话号码存到通讯录里，程序就不需要每次都问你「API Key 是什么」，直接从环境变量里读取。

### 4.2 需要设置哪些变量？

这个工作流需要两个环境变量：

| 变量名 | 示例值 | 说明 |
|-------|-------|------|
| `OBSIDIAN_API_KEY` | `f5df51ff...add18` | Local REST API 插件里的认证密钥 |
| `OBSIDIAN_VAULT_PATH` | `/home/yanglei/文档/Obsidian Vault` | 你的 Obsidian 笔记库根目录路径 |

### 4.3 设置方法（永久生效）

在终端执行以下命令（把引号里的内容换成你自己的）：

```bash
echo 'export OBSIDIAN_API_KEY="你的API Key"' >> ~/.bashrc
echo 'export OBSIDIAN_VAULT_PATH="/你的vault路径"' >> ~/.bashrc
source ~/.bashrc
```

**验证设置成功**：

```bash
echo $OBSIDIAN_API_KEY
```

如果输出了你的 API Key，说明设置成功。

### 4.4 测试 API 是否连通

在终端执行：

```bash
curl -s http://localhost:27123/ -H "Authorization: Bearer $OBSIDIAN_API_KEY"
```

如果返回一大段 JSON 配置信息，说明 Obsidian Local REST API 连接正常，可以进行下一步。

如果没有任何输出或报错，回到第二章 2.3 节检查 HTTP 开关是否已打开。

---

## 第五章：遇到的常见问题

### 5.1 字幕保存失败：Unsupported file extension

**错误信息**：保存字幕文件失败: `Unsupported file extension: .../S1T1`

**原因**：输出文件名没有扩展名，软件不知道要保存成什么格式。

**解决**：在文件名后面加上 `.srt` 或 `.vtt`，例如把 `S1T1` 改成 `S1T1.srt`。

### 5.2 pip 报错：externally-managed-environment

**原因**：Ubuntu 24.04 的系统保护机制阻止 pip 安装包。

**解决**：

```bash
pip install edge-tts --break-system-packages
```

### 5.3 curl 没有任何返回

**原因**：Obsidian Local REST API 插件的 HTTP 服务没有开启。

**解决**：Obsidian 设置 → 第三方插件 → Local REST API → 开启「Enable Non-encrypted (HTTP) Server」开关。

### 5.4 Claude Code 一直转圈没有反应

**原因**：环境变量 `OBSIDIAN_API_KEY` 未设置，或 Obsidian 没有打开，导致 API 请求超时。

**解决**：确认 Obsidian 处于打开状态，且当前有一个笔记处于激活状态。再次检查环境变量是否正确设置。

---

## 第六章：日常使用方法

### 6.1 基本用法

在 Claude Code 终端输入（多种触发方式均可）：

```
生成音频 Bonjour, comment allez-vous ?
```

```
/obsidian-french-tts 读这段：Je suis étudiant en français.
```

```
tts Merci beaucoup pour votre aide.
```

### 6.2 指定声音

默认使用女声 Denise，可以指定其他声音：

| 别名 | 完整名称 | 特点 |
|------|--------|------|
| `denise`（默认） | `fr-FR-DeniseNeural` | 女声，自然流畅 |
| `henri` | `fr-FR-HenriNeural` | 男声，清晰 |
| `eloise` | `fr-FR-EloiseNeural` | 女声，温暖 |
| `vivienne` | `fr-FR-VivienneNeural` | 女声，富有表现力 |
| `remi` | `fr-FR-RemyMultilingualNeural` | 男声，多语言 |

### 6.3 使用前的检查清单

每次使用前确认：

- ✓ Obsidian 处于打开状态
- ✓ 有一篇笔记处于激活状态（编辑器里有内容）
- ✓ 终端里已 `source ~/.bashrc`（或重新开过终端）
- ✓ 网络连接正常（edge-tts 需要联网）

---

## 附录：核心技术概念简介

### REST API 是什么？

API（应用程序编程接口）是程序之间「打电话」的标准协议。REST API 是其中最常见的一种，通过 HTTP 请求传递数据。Local REST API 插件相当于在 Obsidian 里开了一个「接线员」，专门接收来自外部的指令。

### curl 是什么？

curl 是终端里的「HTTP 客户端」，可以向任何 HTTP 服务器发送请求。`curl http://localhost:27123/` 的意思是「向本机 27123 端口发送一个请求」。

### 环境变量是什么？

环境变量是操作系统提供的全局键值存储。你可以把它理解为操作系统的「通讯录」，任何程序都可以查询，不需要每次运行时手动输入配置。

### edge-tts 和微软的关系？

edge-tts 是一个开源 Python 库，通过调用微软 Edge 浏览器的在线语音合成 API 实现文字转语音。生成音频时需要联网，音频质量等同于微软官方 Azure 语音服务。

---

