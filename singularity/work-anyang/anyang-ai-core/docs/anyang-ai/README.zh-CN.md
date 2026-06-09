# anyang-ai 学员快速入门（第一期 · Tier A）

> **状态：** 骨架文档 — 导师在 Gitee 模板落地后补充截图与账号链接。  
> **模板导入：** [anyang-ai-gitee-template-import.md](../../anyang-ai-gitee-template-import.md)

## 你要完成什么

第一期「入门完成」= 你有 **自己的 Gitee 仓库** + **本地能改能推** + **在微信群发过证明**。

不要求：GitHub、Claude、Supabase（这些属于进阶轨道 Tier B）。

## 步骤

### 1. 加入微信群

加入 `anyang-ai`，用一句话介绍自己：**姓名 + 你想用 AI 解决的一个小目标**。

### 2. 注册 Gitee

打开 [gitee.com](https://gitee.com) 注册账号。

### 3. 复刻导师模板

1. 打开导师发的模板链接（形如 `https://gitee.com/<导师用户名>/anyang-ai-template`）。
2. 点击 **Fork / 复刻**，在你的账号下创建 **你自己的仓库**。
3. 把 **你的仓库链接** 发到微信群（这是第一份证明）。

### 4. 克隆到电脑

在终端（导师会演示）：

```bash
git clone https://gitee.com/<你的用户名>/<你的仓库名>.git
cd <你的仓库名>
```

用 VS Code 或其他 IDE 打开文件夹。

### 5. 第一个小胜利

1. 新建或编辑 `docs/my-goal.md`，写 3–5 行你的目标。
2. 提交并推送：

```bash
git add docs/my-goal.md
git commit -m "docs: add my goal"
git push
```

3. 在 Gitee 网页上能看到这次提交。
4. 在微信群发：**完成** 或 **卡在：……**（附截图更好）。

### 6. 安全提醒

- **不要** 把 API 密钥、密码发到微信群。
- **不要** 把 `.env` 提交到 Gitee（确认 `.gitignore` 已忽略）。

## 每周线下课

带电脑。课上会有 **45 分钟实操块** — 每个人都要展示仓库进展或明确卡在哪一步。

## 进阶（Tier B）

若你 **本来就能稳定使用** GitHub 和 Claude，可向导师申请国际完整路径；默认全班走 Tier A。

## 相关说明

- [TIER-A-NOTICE.md](./TIER-A-NOTICE.md)
