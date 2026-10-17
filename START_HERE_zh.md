# 宁远的个人学术主页：发布与维护

本源码为英文个人学术主页，适合向潜在博士导师和研究合作者介绍你的研究。页面已包含你的 NTU、UESTC 和 Glasgow 教育与研究经历、三篇已发表论文、学术平台链接及六个邮箱。

目标地址为 **https://ningyuanxu0.github.io/**。只有 GitHub Pages 部署成功后，这一地址才表示本次网站已经上线；源码文件本身不代表部署成功。

## 1. 先查看本地页面

解压源码包后，进入 `ningyuanxu0.github.io` 文件夹，双击 `index.html` 即可在浏览器中查看。保留 `assets` 文件夹与 `index.html` 的相对位置。

点击 **CV ↗** 可打开 `cv.html`，使用 **Print / Save as PDF** 或浏览器打印功能保存 PDF。网站的内容和链接不依赖 JavaScript；主题切换、手机菜单、论文筛选和复制按钮属于额外功能。

## 2. 通过 GitHub 网页发布，无需命令行

1. 登录 **NingyuanXu0** 对应的 GitHub 账户。
2. 新建仓库，名称填写 **`ningyuanxu0.github.io`**，选择 **Public**。这是用户主页的仓库命名方式，名称全部使用小写。
3. 在仓库选择 **Add file → Upload files**。
4. 将解压后 `ningyuanxu0.github.io` 文件夹中的**内容**上传到仓库根目录。仓库首页应直接看到 `index.html`、`cv.html`、`assets`、`data` 等，而不是在外面再嵌套一层同名文件夹。
5. 点击 **Commit changes**。默认分支使用 `main`。
6. 进入仓库 **Settings → Pages**。
7. 在 **Build and deployment → Source** 选择 **Deploy from a branch**。
8. 在 Branch 选择 **main**，目录选择 **/(root)**，点击 **Save**。
9. 等待 Pages 部署完成。可以在仓库 **Actions** 查看 `pages build and deployment` 的执行结果。
10. 成功后打开 **https://ningyuanxu0.github.io/**。这是供他人访问的主页，GitHub 仓库地址则是源码页面。

源码包包含空的 `.nojekyll` 文件。若文件管理器隐藏了它，可在 GitHub 仓库中通过 **Add file → Create new file** 新建名为 `.nojekyll` 的空文件并提交。

如果你已经有同名主页仓库，应先查看现有内容，再决定将新页面放到其中；本源码未对你的远程仓库执行覆盖操作。

## 3. 以后如何修改

内容集中在 `data/profile.json`，一般不需要改 CSS 或 JavaScript。

| 想修改的内容 | 对应字段 |
| --- | --- |
| 姓名、身份和单位 | `name`、`role`、`affiliation` |
| 首页介绍和详细简介 | `intro`、`about` |
| 研究方向和项目描述 | `interests`、`research` |
| 论文与 DOI | `publications` |
| 教育背景 | `education` |
| 研究和助教经历 | `appointments` |
| 奖项 | `honours` |
| 技能 | `skills` |
| 个人邮箱 | `primary_email`、`secondary_email` |
| 教育邮箱 | `academic_emails`，数组顺序就是网页展示顺序 |
| 学术平台 | `profiles` |
| 页面更新日期 | `updated`，格式为 `YYYY-MM-DD` |

修改 JSON 后，在项目文件夹运行：

```bash
python3 scripts/build.py
python3 scripts/check.py
```

需要 Python 3.9 或以上版本，不需要安装 npm、Ruby 或其他 Python 包。第一条命令同步生成主页、CV、BibTeX 和搜索元数据；第二条检查邮箱、平台链接、本地资源、锚点和元数据。

之后把修改的 JSON 和重新生成的文件一起提交到 GitHub，Pages 会按分支设置更新。**只编辑 JSON 而不重新生成 HTML，已部署页面不会变化。**

如果只是临时调整页面文字，也可以直接修改 `index.html`；但下次运行生成脚本会按 JSON 覆盖它，因此建议以 JSON 为长期维护入口。

## 4. 邮箱安排

网站将 Gmail 作为默认联系邮箱，Outlook 作为另一联系邮箱。教育邮箱按你要求的学校就读顺序排列：

1. UESTC（2022–2026）：`2022190906016@std.uestc.edu.cn`、`nyxu@std.uestc.edu.cn`。
2. University of Glasgow（2022–2026，联合培养）：`2840141x@student.gla.ac.uk`。
3. NTU（2026–present）：`NINGYUAN004@e.ntu.edu.sg`。

页面显示全部六个地址，并保留对应的 `mailto:` 链接。学校邮箱是否在毕业后继续接收邮件由学校决定。

## 5. 图片和论文

首页和研究项目使用原创概念示意图，并标明 **Conceptual illustration**；它们不是实验数据。以后可以将相应 SVG 替换为你准备公开的研究图，并在 `research` 中同步修改图片路径和替代文本。

当前论文列表包括已发表的 ACIS 2026 综述、Small 2025 研究论文和 ACS Nano 2025 综述。DOI 和 BibTeX 已放入源码；网页不托管出版社 PDF。

## 6. 常见问题

- **看到的是代码或 README：**你打开的是仓库地址。部署完成后应打开 `https://ningyuanxu0.github.io/`。
- **主页 404：**检查仓库名、Public 设置、`main / (root)` 和 Actions 的 Pages 部署结果。
- **页面没有样式：**检查 `assets/css/style.css` 是否已上传，以及 `index.html` 是否位于仓库根目录。
- **网页没有更新：**确认新的 HTML 已提交并且最新 Pages 工作流已成功，再刷新页面。
- **复制按钮不可用：**浏览器可能限制本地文件的剪贴板访问；可以直接选中文本复制，或者下载 `.bib` 文件。在 HTTPS 页面上按浏览器提示使用复制功能。

参考项目与官方发布文档见 `docs/REFERENCES.md`。检查范围见 `docs/VALIDATION.md`。
