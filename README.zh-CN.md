# Architecture Diagramming Skill

一个用于创建、解释和评审技术架构图/系统架构图的 Codex Skill。

它沉淀了一套实用架构图方法：先判断受众和图的层级，再从业务能力、关键场景、非功能需求、横向分层、纵向复用和生产稳定性模块推导出架构图，而不是把技术组件堆在一起。

## 适用场景

- 你要画整体技术架构图、系统架构图、逻辑架构图。
- 你要把业务架构映射成技术组件。
- 你要说明模块职责、依赖关系、数据流、同步/异步调用。
- 你要用 Mermaid 或 PlantUML 输出架构图。
- 你要评审一张已有架构图，找出粒度混乱、连线语义不清、组件堆叠、缺少稳定性模块等问题。

## 安装

把 Skill 目录复制到 Codex 的全局 skills 目录：

```powershell
Copy-Item -Recurse .\skills\architecture-diagramming "$env:USERPROFILE\.codex\skills\architecture-diagramming"
```

如果目录已存在，可以先手动备份旧版本，再覆盖。

## 使用方式

示例：

```text
Use $architecture-diagramming to design a technical architecture diagram for an e-commerce order system.
```

或者中文直接说：

```text
帮我用 architecture-diagramming 画一个电商订单系统的技术架构图。
```

Codex 默认会输出：

1. 受众和架构图层级假设。
2. 组件清单和职责。
3. 关系清单，包括同步/异步语义。
4. Mermaid 架构图。
5. 简短评审 checklist 和下一步优化建议。

## 自动发布到 GitHub

仓库内置了一个 Python 发布脚本：

```powershell
python .\scripts\publish_skill_to_github.py `
  --skill-path .\skills\architecture-diagramming `
  --repo-name architecture-diagramming-skill `
  --description "Codex skill for creating and reviewing clear technical/system architecture diagrams."
```

脚本会：

1. 读取 `GITHUB_TOKEN` 环境变量。
2. 打包指定 Skill 到标准仓库结构。
3. 创建或复用同名 GitHub 仓库。
4. 初始化 git、提交并 push。

脚本不会把 token 写入文件。可以先加 `--dry-run` 验证本地打包流程，不会访问 GitHub。

## 核心方法

### 1. 先判断架构图层级

- 整体技术架构图：给 CTO、技术负责人、产品经理、新成员看。
- 子领域/子系统架构图：给领域架构师、核心开发、跨团队评审看。
- 应用级架构图：给开发和测试看，展示应用内部模块、层、接口和技术实现。

### 2. 六步画图法

1. 从业务架构推导技术骨架。
2. 从关键用例和非功能需求推导技术模块。
3. 提炼横向分层。
4. 提炼纵向复用模块。
5. 补充稳定性和生产支撑模块。
6. 形成分层、分片的逻辑架构。

### 3. 绘图语义

- 方框：服务、应用、模块、平台、数据库、队列、外部系统。
- 实线箭头：同步调用，例如 HTTP/RPC。
- 虚线箭头：异步消息、事件、任务。
- 双向箭头：双向通信，例如 WebSocket。
- 无箭头虚线：编译期、配置或非运行时依赖。

## 维护建议

这个仓库适合持续补充：

- 不同业务场景的 Mermaid 模板。
- 架构图评审案例。
- 中英文示例提示词。
- 从真实项目中抽象出来的架构图模式。
