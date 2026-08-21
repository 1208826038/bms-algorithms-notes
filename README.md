# bms-algorithms-notes

BMS（电池管理系统）核心算法与 Simulink 建模**深度笔记**，从底层嵌入式工程师视角讲透原理、建模、代码生成与实测。

> 这是一份**独立仓库**，内容比 `embedded-skill-notes` 里面试神器.html 的 BMS 速记章深数倍：公式推导、拓扑对比、控制伪代码、Simulink→Embedded Coder 代码生成链路、MIL/SIL/PIL/HIL 验证、ISO 26262 落地都铺开讲。

## 内容地图（bms-deep.md，23 节，约 1.7 万字）

- **系统全景**：从电芯到算法的数据流、为什么只能估算不能测量、算法在 AUTOSAR 软件栈的位置、量产视角（和你「单季度万级出货」简历挂钩）
- **电池模型地基**：LFP/NMC 差异、Rint/1RC/2RC/PNGV 谱系、1RC/2RC 方程与离散化、OCV 滞回与温度、HPPC/RLS 参数辨识
- **SOC 估算**：安时积分、OCV 查表、**EKF 完整推导（雅可比/五步递推/噪声整定/数值算例）**、**UKF sigma 点公式**、PF、温/倍率/老化补偿、校准策略
- **SOH 估算**：容量法/内阻法、SEI 老化机理、ICA(dQ/dV) 增量容量分析、在线/离线
- **均衡 BAL**：被动 vs 主动（电容/电感/flyback/Buck-Boost 拓扑对比）、判据与策略、控制伪代码、发热与时间估算
- **SOP/SOE**：含极化的精确功率公式与时域
- **故障诊断与功能安全**：故障-DTC 衔接、绝缘监测、ISO 26262 ASIL 分配与 FMEA、接触器预充状态机
- **热管理**：产热模型、冷却方式、温差控制
- **Simulink→代码生成（重点）**：工具链、建模四步法、生成代码结构、与 AUTOSAR Runnable/NvM 映射、MIL/SIL/PIL/HIL、S32K144 最小可练链路、代码生成配置速查 + MCAL 衔接
- **量产与架构**：标定/OTA、集中式 vs 分布式 BMS、MCU 资源预算
- **工程坑与面试 20 题速查**、与简历亮点衔接

## 怎么看

- **直接读源码**：`bms-deep.md`（GitHub 原生渲染，含代码块与表格）。
- **离线浏览器看**：双击打开 `index.html`（内嵌同一份 markdown，自带渲染器，深色主题，无需联网）。
- 修改 markdown 后重新生成 `index.html`：运行 `python build_index.py`。

## 与实战衔接

本仓库内容与 `S32K144_上手指南.md`、MATLAB R2024b 配合，可在家把「安时积分 SOC → RTE → CAN 发出」的最小链路在 S32K144 上跑通，把本章每个算法落到真板子。

## License

学习笔记，转载请注明出处。
