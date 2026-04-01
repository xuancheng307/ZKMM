# 圖表製作任務清單

## 需要製作的圖（按報告出現順序）

### Fig 1: Taylor vs Minimax 誤差分佈圖
- 位置：§3.2
- 內容：兩條曲線，x 軸是 R (輸入)，y 軸是 ULP error
  - Taylor: 誤差在區間邊緣暴增
  - Minimax: 誤差均勻分佈（等振盪）
- 數據來源：`exp01/results/` 的窮舉 ULP 數據
- 工具：Python matplotlib
- 做 exp(x)-1 即可（最直觀的 12x 比較）

### Fig 2: ORV 概念圖
- 位置：§3.1
- 內容：示意圖，展示單調函數 f(R)，標示：
  - 合法區間 [0, R_MAX] → w < S ✓
  - 非法 R > R_MAX → P(R) mod p 是隨機數 → w ≥ S（極高機率）
- 目前 HTML 中用文字+pipeline 圖替代，如果老師需要可補

### Fig 3: Deferred vs Per-step 截斷示意圖
- 位置：§3.3
- 內容：兩個流程圖對比
  - Per-step: 每步都有截斷箭頭，誤差累積
  - Deferred: 只有最後一步截斷
- 目前 HTML 中用 monospace text 替代，可升級為 SVG

### Fig 4: Pipeline 架構圖
- 位置：§5.1
- 內容：已在 HTML 中用 CSS flexbox 實現
- 可選：升級為更精美的 SVG 或 TikZ

### Fig 5: 方法比較雷達圖（optional）
- 位置：§4.2
- 內容：Method A vs B vs G 在 5 個維度的比較
  - 表格大小、prove time、proof size、精度、通用性
- 工具：Python matplotlib radar chart

## 需要的數據表（已在 HTML 中嵌入）

所有表格數據已直接嵌入 index.html，來源對照：

| HTML 表格 | 數據來源檔案 | 已驗證？ |
|-----------|-------------|:--------:|
| §1.4 改善倍率 | exp04 taylor_generalization_results.md | ✅ |
| §3.1 區間 trade-off | exp04 wider_interval_results.md | ✅ |
| §3.1 ORV 結果 | exp02 + exp04 orv_ablation_results.md | ✅ |
| §3.3 截斷比較 | exp04 per_step_results.md | ✅ |
| §3.4 電路指標 | exp04 benchmark_results.md | ✅ |
| §4.1 Ablation 1 | exp04 taylor_generalization_results.md | ✅ |
| §4.1 Ablation 2 | exp04 per_step_results.md | ✅ |
| §4.1 Ablation 3 | exp04 orv_ablation_results.md | ✅ |
| §4.2 方法比較 | exp04 benchmark_results.md + Table 3 | ✅ |
| §4.3 文獻比較 | docs/competitor_analysis.md | ✅ |

## 優先順序

1. **Fig 1 (Taylor vs Minimax)** — 最有視覺衝擊力，建議一定要做
2. Fig 3 (截斷對比) — 幫助理解核心概念
3. Fig 2 (ORV) — 如果老師問「為什麼不用 range check」時有圖可解釋
4. Fig 4, 5 — optional，目前 HTML 版本已夠用
