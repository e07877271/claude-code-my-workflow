---
paths:
  - "reports/**"
  - "topics/**"
---

# 任务完成验证协议

**每次生成或修改报告后，必须在汇报前完成以下验证。**

## 对于报告文件（reports/*.md）

1. 确认文件已写入磁盘（PowerShell）：
   ```powershell
   Test-Path "reports/YYYY-MM-DD_[主题简称].md"
   ```
2. 读取文件前 30 行，确认开篇摘要和第一节标题已正确生成
3. 检查文件字数是否符合预期（2000 字以上）
4. 若已运行 `/review-report`，确认审查报告已保存至 `quality_reports/`

## 对于桌面 Markdown 文件（C:\Users\e0787\Desktop\*.md）

1. 确认文件存在（PowerShell）：
   ```powershell
   Test-Path "C:\Users\e0787\Desktop\YYYY-MM-DD_[主题简称].md"
   ```
2. 若文件不存在，重新运行：
   ```powershell
   Copy-Item "reports/YYYY-MM-DD_[主题简称].md" -Destination "C:\Users\e0787\Desktop\YYYY-MM-DD_[主题简称].md" -Force
   ```

## 对于资料摘要（topics/*.md）

1. 确认文件已写入 `topics/` 目录
2. 确认每条来源都有机构名称、日期和核心论点

## 禁止假设成功

- 不要在未验证文件存在的情况下汇报"已完成"
- 若验证失败，报告失败原因并重试，而不是忽略错误
