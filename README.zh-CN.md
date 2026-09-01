# PDF Toolkit
[![CI](https://github.com/Senyu-Lab/pdf-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Senyu-Lab/pdf-toolkit/actions/workflows/ci.yml)

[English](README.md) | [简体中文](README.zh-CN.md)

一个用于合并、拆分和编辑 PDF 文件的简单 Python 工具。

PDF Toolkit 同时提供命令行界面（CLI）和基于 PySide6 构建的图形用户界面（GUI）。

## 功能

* 将多个 PDF 文件合并为一个 PDF
* 按页码范围拆分 PDF
* 删除 PDF 中指定的页面或页面范围
* 支持多个页面范围
* 验证用户输入和页码范围
* 支持拖放 PDF 文件
* 合并 PDF 时支持通过拖放调整文件顺序
* 使用 SQLite 持久化保存操作历史
* 查看操作详细信息
* 删除选中的历史记录
* 清空操作历史
* 命令行界面（CLI）
* 基于 PySide6 的图形用户界面（GUI）
* 多语言 GUI 支持

  * English
  * 中文
  * 日本語
* Windows 可执行程序

## 环境要求

* Python 3.10+
* PyMuPDF
* PySide6
* pytest
* pytest-qt
* Ruff
* PyInstaller

## 安装

克隆仓库并安装依赖：

```bash
git clone https://github.com/Senyu-Lab/pdf-toolkit.git
cd pdf-toolkit
pip install -r requirements.txt
```

## 使用方法

PDF Toolkit 同时提供命令行界面和图形用户界面。

### CLI

将 PDF 文件放入 `input` 文件夹。

运行：

```bash
python main.py
```

然后根据菜单选择相应操作。

### GUI

运行：

```bash
python gui_main.py
```

GUI 当前提供以下功能：

* 合并 PDF
* 拆分 PDF
* 删除 PDF 页面
* 操作历史

GUI 同时支持直接拖放 PDF 文件。

## 多语言支持

GUI 当前支持三种语言：

* English
* 中文
* 日本語

国际化系统与核心 PDF 处理逻辑相互独立。

翻译资源位于：

```text
gui/
└── i18n/
    ├── __init__.py
    ├── manager.py
    └── translations.py
```

语言管理器提供了统一的界面文本管理方式。

如果需要添加其他语言，可以扩展翻译资源，而无需修改核心 PDF 处理逻辑。

## 数据库与操作历史

PDF Toolkit 使用 SQLite 在本地持久化保存 PDF 操作历史。

数据库层与 GUI 和 PDF 处理逻辑相互独立。SQL 语句单独维护，与 Python 代码分离，从而保持数据库层的模块化和可维护性。

历史记录系统会记录 Merge 和 Split 等 PDF 操作，包括操作状态、输入文件、输出文件以及发生错误时的错误信息。

### History 功能

History 界面提供：

* 查看操作历史
* 刷新历史记录
* 删除选中的历史记录
* 清空全部历史记录
* 查看操作详细信息
* 区分成功和失败的操作

### 数据库功能

数据库层提供：

* SQLite 数据库初始化
* 数据库连接管理
* 操作历史 Repository
* 添加操作记录
* 查询操作记录
* 删除操作记录
* 清空操作记录
* 输入验证
* 自动化数据库测试

## Windows 可执行程序

GitHub Releases 提供预构建的 Windows x64 可执行程序。

### 下载

当前版本：

```text
v1.2.0
```

Windows 发布包：

```text
PDF-Toolkit-Windows-x64-v1.2.0.zip
```

下载并解压 ZIP 文件后，运行：

```text
PDF-Toolkit.exe
```

打包后的 Windows 版本无需安装 Python 即可运行。

## 合并 PDF

选择：

```text
1. Merge PDFs
```

程序会将输入目录中的 PDF 文件合并为指定的输出文件。

例如：

```text
output/merged.pdf
```

### GUI 合并

在 GUI 中，可以通过文件选择对话框添加 PDF 文件，也可以直接将 PDF 文件拖入文件列表。

可以通过拖动文件调整 PDF 的合并顺序。

程序会自动阻止重复添加相同的 PDF 文件。

成功或失败的 Merge 操作都会记录到操作历史中。

## 拆分 PDF

选择：

```text
2. Split PDF
```

输入页面范围：

```text
2-5, 8-10
```

程序将生成：

```text
output/
├── pages_2-5.pdf
└── pages_8-10.pdf
```

GUI 同样支持直接将 PDF 文件拖入 Split PDF 界面。

成功或失败的 Split 操作都会记录到操作历史中。

## 删除页面

选择：

```text
3. Delete Pages
```

输入需要删除的页面或页面范围：

```text
2, 5-7, 10
```

程序会删除指定页面。

例如，一个包含 10 页的 PDF：

```text
2, 5-7, 10
```

表示删除第 2、5、6、7、10 页。

最终保留：

```text
1, 3-4, 8-9
```

并生成：

```text
output/
└── modified.pdf
```

程序会验证页面范围，并防止删除 PDF 中的全部页面。

如果输出文件已经存在，程序会在覆盖文件前请求用户确认。

## 操作历史

History 界面用于查看之前执行过的 PDF 操作。

每条历史记录可以包含：

* 操作类型
* 操作状态
* 创建时间
* 输入文件
* 输出文件
* 错误信息

### 删除选中记录

选择一条历史记录，然后选择 **Delete Selected**，即可从数据库中删除该记录。

### 清空历史

选择 **Clear History** 可以删除所有保存的操作记录。

清空操作前程序会要求用户确认。

### 操作详情

双击一条历史记录，可以打开操作详情窗口。

详情窗口会显示该操作的完整信息，包括：

* 操作类型
* 状态
* 创建时间
* 输入文件
* 输出文件
* 错误信息（如果存在）

## 测试

运行全部测试：

```bash
pytest
```

项目使用 `pytest` 和 `pytest-qt` 进行自动化测试。

测试覆盖：

* PDF 合并
* PDF 拆分
* 页面删除
* 页面范围验证
* 文件工具
* CLI 行为
* GUI 功能
* 拖放功能
* 多语言 GUI
* 用户设置
* 数据库初始化
* SQLite Schema
* 操作历史 Repository
* HistoryWidget
* History Details
* 输入验证

当前 `v1.2.0` 测试结果：

```text
126 passed
```

## 代码质量

使用 Ruff 检查代码：

```bash
ruff check .
```

## 构建 Windows 可执行程序

Windows 可执行程序使用 PyInstaller 构建。

项目包含 PyInstaller 配置文件：

```text
PDF-Toolkit.spec
```

在本地构建：

```bash
pyinstaller PDF-Toolkit.spec
```

生成的程序位于：

```text
dist/PDF-Toolkit/
```

`build/` 和 `dist/` 目录已被 Git 忽略。

## 持续集成

GitHub Actions 会在代码推送到仓库后自动运行项目测试和代码质量检查。

Windows 构建流程还会：

* 安装所需依赖
* 运行测试
* 使用 PyInstaller 构建 Windows 可执行程序
* 创建可分发的 ZIP 压缩包
* 将 Windows 构建结果作为 GitHub Actions Artifact 上传

这样可以确保 Windows 可执行程序始终基于经过测试的项目版本构建。

## 当前版本

**v1.2.0**

### v1.2.0 更新内容

* 新增基于 SQLite 的持久化操作历史
* 新增操作历史管理
* 新增历史记录刷新功能
* 新增删除选中历史记录功能
* 新增清空历史记录功能
* 新增操作详情窗口
* 新增 Merge 和 Split 操作记录
* 新增成功与失败状态记录
* 新增操作错误信息记录
* 新增数据库和历史功能的自动化测试
* 自动化测试数量扩展至 126 个并全部通过
* 新增 Windows x64 可执行程序发布

## 许可证

本项目使用 MIT License。

详细信息请参阅 `LICENSE` 文件。

## 作者

Senyu Wu

GitHub：Senyu-Lab
