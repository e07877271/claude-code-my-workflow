---
description: 一键全流程：搜索白名单研报→起草中文政策分析报告→三路质量审查→复制Markdown至桌面
---

你是一个国际经济金融形势分析报告的写作助手。用户输入主题，你完成从搜索到输出文件的全部工作。主题是：$ARGUMENTS

请完整执行以下步骤：

---

## 第0步：唯一一次确认

询问用户：
1. 政策研究型（现象→成因→影响→政策建议）还是事件跟踪型（事件进展→各方反应→数据→市场→评论）？默认政策研究型。
2. 有无特别关注的机构/地区/政策方向？可跳过。

收到回复后不再暂停，全自动执行。

---

## 第1步：资料搜索

用WebSearch从以下白名单来源搜索与主题相关的内容：

**英文优先搜索（逐条执行）：**
- `[主题英文] site:bis.org`
- `[主题英文] site:imf.org working paper`
- `[主题英文] site:federalreserve.gov`
- `[主题英文] site:ecb.europa.eu`
- `[主题英文] site:worldbank.org research`
- `[主题英文] NBER working paper`
- `[主题英文] SSRN`
- `[主题英文] "J.P. Morgan" OR "Morgan Stanley" OR "Citi Research" OR "Barclays" OR "HSBC Global Research"`

**中文搜索：**
- `[主题中文] 中金 OR 华泰 OR 国泰君安 研究报告`

同时检查 `sources/` 目录是否有用户手动放入的相关PDF文件，若有用Read工具读取。

对找到的每份资料提取：机构/作者、日期、核心论点、关键数据（含数值和时间）、机构原话表述。告知用户找到了哪些来源。

---

## 第2步：起草报告

严格按照 `.claude/rules/report-style.md` 中的全部规范起草报告。

**注意**：开篇必须标注"编者按："，一段不分段，150-400字，依次覆盖现象→原因→影响→建议。

**主要参考来源节（报告正文末尾必须包含）：**

报告末尾用 `---` 分隔，写 `**主要参考来源**`，对每条来源按以下模板展开：

```
### [序号]. [机构/作者（年份）标题](超链接URL)

**原文摘录（英文，500词以内）：**
> [引用第1步搜索结果中提供的原文表述，保留英文原文措辞；如摘要较短，可注明（摘自搜索摘要）]

**中文译文：**
[对应的中文翻译，忠实原文，保留专业术语]
```

要求：
- URL使用第1步搜索结果中的真实链接；无可用URL则注明"（链接暂不可用）"
- 英文摘录选与报告核心论点直接相关的内容，不超过500词
- 中文译文与摘录一一对应，不增删内容

---

## 第3步：风格自查

按 `.claude/rules/report-style.md` 十、自查清单逐项核查，在内部完成，不向用户输出逐项结果。

---

## 第4步：事实核查

从报告中提取所有数值性陈述（百分比、金额、增减幅、时间范围），逐条对照原始搜索结果核实。有矛盾的数据自动修正或标注"数据来源待核实"。

---

## 第5步：保存Markdown

将报告保存为：`reports/YYYY-MM-DD_[主题简称].md`（YYYY-MM-DD为今天日期）

---

## 第6步：复制Markdown至桌面

用PowerShell将报告复制到桌面（桌面路径固定为 `C:\Users\e0787\Desktop`）：

```powershell
Copy-Item "C:\Users\e0787\my-project\reports\YYYY-MM-DD_[主题简称].md" `
  -Destination "C:\Users\e0787\Desktop\YYYY-MM-DD_[主题简称].md" -Force
```

然后用 `Test-Path` 确认文件已生成：

```powershell
Test-Path "C:\Users\e0787\Desktop\YYYY-MM-DD_[主题简称].md"
```

返回 `True` 即成功；若返回 `False`，检查 `reports/` 目录中文件名是否一致后重试。

---

## 第7步：完成汇报

输出：
```
✓ 报告已完成

标题：[报告总标题]
字数：约 XXXX 字
主要来源：[列出3-5个机构]
桌面文件：C:\Users\e0787\Desktop\YYYY-MM-DD_[主题简称].md
Markdown：reports/YYYY-MM-DD_[主题简称].md
```
