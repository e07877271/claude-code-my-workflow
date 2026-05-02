---
description: 从BIS/IMF/美联储/欧央行/各央行/学术论文/中外投行搜索研报，生成中文资料摘要
---

搜索与以下主题相关的研报和学术论文，主题：$ARGUMENTS

**搜索范围（白名单，逐条执行）：**
- `[主题英文] site:bis.org`
- `[主题英文] site:imf.org`
- `[主题英文] site:federalreserve.gov`
- `[主题英文] site:ecb.europa.eu`
- `[主题英文] site:worldbank.org`
- `[主题英文] NBER working paper`
- `[主题英文] SSRN`
- `[主题英文] "J.P. Morgan" OR "Morgan Stanley" OR "Citi Research" OR "Barclays" OR "HSBC"`
- `[主题中文] 中金 OR 华泰 OR 国泰君安`

同时检查 `sources/` 目录是否有本地PDF文件。

**每份资料生成摘要卡：**
```
来源：[机构] | [日期] | [全文/仅摘要]
核心论点：[1-2句]
关键数据：[数值+时间]
机构表述：[原话引用]
链接：[URL]
```

将全部摘要卡保存至 `topics/YYYY-MM-DD_[主题简称]_lit-search.md`，并告知用户找到了哪些来源及核心结论3条。
