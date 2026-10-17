# 个人学术主页：发布与维护

正式网址：**https://ningyuanxu0.github.io/**。

GitHub 仓库：https://github.com/NingyuanXu0/ningyuanxu0.github.io 。

## 页面内容

首页集中展示个人简介、两个主要研究方向、三篇论文、三项第一发明人专利申请、教育与研究经历、导师及联系方式。详细研究经历、助教经历、技能和奖项保留在 `cv.html`。

正文采用 Arial／Helvetica，标题采用 Georgia。桌面正文为 18px，手机正文为 17px，导航为 16px，主要辅助文字为 15–17px。

三位导师均提供邮箱、课题组主页和 Google Scholar 链接。专利部分区分已受理申请与已公布申请，两项公开记录提供查询链接。

## 修改内容

内容源文件为 `data/profile.json`。

| 想修改的内容 | 对应字段 |
| --- | --- |
| 姓名、身份和研究简介 | `name`、`role`、`affiliation`、`intro`、`tagline` |
| 研究方向和详细研究经历 | `research` |
| 论文及 DOI | `publications` |
| 专利名称、发明人、申请号和公开记录 | `patents` |
| 导师姓名、邮箱、课题组及 Google Scholar | `supervisors` |
| 教育及研究／教学经历 | `education`、`appointments` |
| CV 中的技能和奖项 | `skills`、`honours` |
| 个人及学术邮箱 | `primary_email`、`secondary_email`、`academic_emails` |
| 学术平台 | `profiles` |
| 更新日期 | `updated`，格式为 `YYYY-MM-DD` |

`research` 和 `appointments` 中的 `show_on_homepage` 决定条目是否显示在首页；完整内容仍会进入 CV。研究条目的 `homepage_title` 和 `homepage_description` 用于精简首页展示，`details` 用于完整 CV。

修改后在项目文件夹运行：

```bash
python3 scripts/build.py
python3 scripts/check.py
```

需要 Python 3.9 或以上版本，无需额外 Python 包。请把 JSON 和重新生成的 HTML 等文件一起提交到 `main`，GitHub Pages 会自动更新。单独修改 JSON 不会改变已生成的网页。

## GitHub Pages 设置

当前发布设置为 **Settings → Pages → Deploy from a branch → main → /(root)**，已启用 HTTPS。

`index.html` 位于仓库根目录，`.nojekyll` 已包含在源码中。可在仓库 Actions 中查看 `pages build and deployment` 的结果。

## 专利与导师信息核对

三项专利以你提供的原始文件核对：

- 无透析液血液净化器：`202610812573.7`，2026-06-07 申请，受理通知书确认已受理。
- 超双疏高反射涂料：`202510541383.1`，公开号 `CN120248697A`。已按原件将旧 CV 的申请号和共同发明人修正为徐宁远、杨金龙。
- 流媒体后视镜防雨水：`202410272423.2`，公开号 `CN118455041A`。

导师邮箱和 Google Scholar 链接按课题组及学校官方页面核实。相关来源见 `docs/REFERENCES.md`。

## 联系方式和 CV

首页保留 Gmail、Outlook 两个个人邮箱。原有四个教育邮箱位于 Contact → Academic email addresses，点击即可展开。

打开 `cv.html`，点击 **Print / Save as PDF** 可打印或保存 CV。深浅主题和手机菜单为可选增强功能，页面内容与普通链接均可在禁用 JavaScript 时使用。
