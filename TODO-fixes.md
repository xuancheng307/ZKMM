# 網站結構 4 份 HTML 報告修正 TODO

Created: 2026-03-11

## 數據來源確認

benchmark_results.md (exp04) 實測數據：
```
G+ORV:  5 gates, 12 lookups, 9 rows,  ~135-138 ms, 4,960 B  ← 多數表格引用
G+RC:   6 gates, 12 lookups, 10 rows, ~132 ms,     4,992 B  ← ExplicitRC 實測
G-ORV:  4 gates, 12 lookups, 8 rows,  ~129 ms,     4,928 B  ← 無檢查 baseline
```

結論：報告已採用 ExplicitRC，但 benchmark 數據大多來自 G+ORV。
**ExplicitRC 與 ORV 的差異：+1 gate, +1 row, +32 B proof, prove time 在雜訊內。**
**ULP 數據不受影響**（Horner 計算邏輯相同，只差範圍檢查方式）。

---

## A. 公式錯誤：d×pp → (d+1)×pp

中間值 bit width 是 (d+1)×pp（例如 d=5, pp=16 → 96 bits）。
但 rem < S^d，所以 rem_bytes = ⌈d×pp/8⌉ 是對的。
問題在：描述「中間值大小」或「BN254 約束」時用了 d×pp。

| # | 文件 | 行 | 現狀 | 修正 |
|---|------|-----|------|------|
| A1 | proposal.html | L920 | "d×pp bits（…96 bits" | → "(d+1)×pp bits（…96 bits" |
| A2 | proposal.html | L934 | "d×pp bits" | → "(d+1)×pp bits" |
| A3 | proposal.html | L936 | "d×pp < 253" | → "(d+1)×pp < 254" |
| A4 | contribution-comparison.html | L205 | "d×pp bit" | → "(d+1)×pp bit" |
| A5 | degree_selection_report.html | L323 | "d·pp < 253" | → "(d+1)×pp < 254" |
| A6 | degree_selection_report.html | L2107 | "d·pp < 253" | → "(d+1)×pp < 254" |
| A7 | degree_selection_report.html | L2199 | "d·pp > 253" | → "(d+1)×pp > 253" |

已正確的位置（不需改）：
- research-background.html L309: "(d+1)×pp" ✓
- contribution-comparison.html L666, L729: "(d+1)×pp" ✓
- proposal.html L1177: "(d+1)×pp < 254" ✓
- degree_selection_report.html L1760: "(d+1)×pp < 254" ✓

---

## B. Gate count：5 → 6（ExplicitRC）

| # | 文件 | 行 | 現狀 | 修正 |
|---|------|-----|------|------|
| B1 | proposal.html | L960 | "Gates = 5（固定）" | → "6（固定）" |
| B2 | proposal.html | L1060 ablation | ExplicitRC rows=9 | → rows=10 |
| B3 | contribution-comparison.html | L672 | "5 gates" | → "6 gates" |
| B4 | degree_selection_report.html | L1629 | "5（固定）" | → "6（固定）" |
| B5 | degree_selection_report.html | L1630 | "1 Horner + 1 truncation + 3 byte-decomp" | → "+1 range check = 6" |
| B6 | degree_selection_report.html | L1786 | "5" | → "6" |

---

## C. Row count：d+4=9 → d+5=10（ExplicitRC 多一行 range check）

benchmark 實測：G+RC = 10 rows，G+ORV = 9 rows。
ExplicitRC 加了一行 r_range_check gate。

| # | 文件 | 行 | 現狀 | 修正 |
|---|------|-----|------|------|
| C1 | proposal.html | L962 | "d + 4" → 9 | → "d + 5" → 10 |
| C2 | proposal.html | L1060 | ExplicitRC rows=9 | → 10 |
| C3 | contribution-comparison.html | L672 | 隱含 d+4 | → d+5 |
| C4 | degree_selection_report.html | L1639 | "d + 4" | → "d + 5" |
| C5 | degree_selection_report.html | L1667 | pp=16,d=5 rows=9 | → 10 |
| C6 | degree_selection_report.html | L1675 | pp=24,d=5 rows=9 | → 10 |
| C7 | degree_selection_report.html | 其他行 | rows 11, 13 等 | 全部 +1 |

---

## D. Lookup 公式 ✅ FIXED (2026-03-13)

正確公式為 `⌈pp/8⌉ + ⌈d×pp/8⌉`（所有 pp 等級皆透過 selector union 共用 R/w/gap byte 欄位）。
舊公式 `2⌈pp/8⌉ + ⌈d×pp/8⌉` 是錯的——它數的是「被分解的 byte 總數」而非 Halo2 `meta.lookup()` argument 數。

已修正：所有 .tex, .html, .md, .json, .rs 檔案的公式、lookup 值、proof size ratio。

---

## E. Proof size：4,960 → 4,992

| # | 文件 | 行 | 現狀 | 修正 |
|---|------|-----|------|------|
| E1 | contribution-comparison.html | L440 | Ours 4,960 | → 4,992 |
| E2 | contribution-comparison.html | L479 | 4,960 B | → 4,992 B |
| E3 | contribution-comparison.html | L512 | 4,960B | → 4,992B |
| E4 | contribution-comparison.html | L672 | 4,960 B | → 4,992 B |
| E5 | contribution-comparison.html | L725 | 4,960B | → 4,992B |
| E6 | proposal.html | L977-980 | 4,960 B (×4) | → 4,992 B |
| E7 | degree_selection_report.html | L1740 | 4,960 B | → 4,992 B |

注意：
- contribution-comparison.html L430 Taylor+Deferred 行的 4,960 是**不同電路**（無 ExplicitRC），可保留
- proposal.html L1074 已經是 4,992 ✓
- 6.7x 比率 (736 vs 4960) → 變成 6.8x (736 vs 4992)，影響 contribution-comparison L480, L512, L725

---

## F. Prove time

benchmark 實測：G+ORV ~135-138 ms, G+RC ~132 ms（兩者在雜訊內）。

| # | 文件 | 行 | 現狀 | 修正 |
|---|------|-----|------|------|
| F1 | contribution-comparison.html | L438 | 137.8 | 保留（實測值，加腳注配置） |
| F2 | proposal.html | L977-980 | 137.8/135.9/137.0/137.5 | 保留原值，加腳注「G+ORV 基線，ExplicitRC 差異 <2%」 |

proposal.html L1074 的 132 ms 來自 exp05（基於 exp04 初始 131.7 ms 的四捨五入），搭配 4,992 B 是合理的 ExplicitRC 數據。

---

## G. 文獻空白數量

| # | 文件 | 行 | 現狀 | 修正 |
|---|------|-----|------|------|
| G1 | contribution-comparison.html | L186 | "5 個具體的文獻空白" | → "4 個"（表格只有 G1-G4） |

---

## H. 系統數量

| # | 文件 | 行 | 現狀 | 修正 |
|---|------|-----|------|------|
| H1 | proposal.html | L1157 | "30 個 ZK 系統" | → "22 個系統"（與 contribution-comparison 一致） |

---

## I. 52 組配置分類遺漏

33 + 15 + 0 = 48，但總數是 52。缺少 4 組「兩者皆 d*>9」的配置。

| # | 文件 | 行 | 修正 |
|---|------|-----|------|
| I1 | proposal.html | L359-360 | 加入第四類別 "4 組兩者均無法在 d≤9 內達標" |
| I2 | contribution-comparison.html | L627-640 | 同上 |

---

## J. contribution-comparison.html §4 編號

§4.4-4.8 的 "Contribution X" 編號是舊版殘留。核心只有 3 個 contributions。
§4.7 缺失（跳號）。

| # | 修正 |
|---|------|
| J1 | §4.4-4.8 重新命名為 "Finding" 或 "Analysis"，不叫 "Contribution" |
| J2 | 修復跳號 |

---

## K. research-background.html（無數據問題）

這份文件刻意避免具體 benchmark 數字，使用 (d+1)×pp 正確公式，不提 gate count。
唯一需確認：L309 "lookup 數量節省約 40%" 是否有數據支撐。
依據 per-step 約 22 lookups vs deferred 12-14 lookups ≈ 36-45% 節省，OK。

---

## 修正狀態

A-K 完成 ✓（2026-03-11）
L 完成 ✓（2026-03-12）

- A（公式 d×pp → (d+1)×pp）：✓ proposal / contribution-comparison / degree_selection_report
- B（Gates 5 → 6）：✓ proposal / contribution-comparison / degree_selection_report
- C（Rows d+4 → d+5）：✓ proposal / contribution-comparison / degree_selection_report
- D（Lookup 公式 pp=16 sharing 備註）：✓ proposal L964 / contribution-comparison L677
- E（Proof size 4,960 → 4,992）：✓ proposal / contribution-comparison / degree_selection_report
- F（Prove time 腳注）：✓ proposal L983
- G（文獻空白 5 → 4）：✓ contribution-comparison L186
- H（系統數量 30 → 22）：✓ proposal L1157
- I（52 組分類加第四類）：✓ proposal L360 / contribution-comparison L640
- J（§4 編號修復）：✓ contribution-comparison §4.8 → §4.7，移除 "Contribution 8"
- K（research-background）：✓ 確認無需修改

---

## L. BN254 累積值約束修正（2026-03-12）

### 問題
§9 BN254 約束使用 `d×pp < 253`（僅檢查係數大小），正確約束應為 `(d+1)×pp < 254`（Horner 累積值 P(R) 需 fit in field）。

### 影響
- d_max 全部下降 1：pp=12:20, pp=16:14, pp=20:11, pp=24:9, pp=28:8, pp=32:6, pp=36:6, pp=40:5
- pp=28 最受影響：d=9 不可用 → ln, arcsin, GELU 在 pp=28 無法達 ULP=1
- 可行配置點：585 → 546（溢出 52 → 91）
- 52 組統計：33/15/0/4 → 30/15/0/7

### Python 實驗說明
- ULP 計算使用 Python 無限精度整數，數學上正確
- 但 BN254 可行性檢查只看 max(|D_i|) < 2^253，未檢查累積值
- pp=28 d=9 的 ULP=1 結果在數學上正確，但無法部署到 BN254 電路
- Rust/Halo2 測試只跑過 d=5（pp=16 和 pp=24），未觸發此問題

### 待辦
- [ ] 全部實驗數據改為 Rust/Halo2 版本（用戶確認）
- [ ] 圖表更新（pp* vs d 圖的 BN254 紅線位置）

---

## M. EXP07 E2E Results Integration（2026-03-14）

### 問題
Range reduction 原為「未來工作」，所有成本為估計值。EXP07 已完成全部 13 個函數的 E2E 電路 + KZG benchmark。

### 修正
- [x] M1: proposal.html S5.1 — pipeline scope: 灰色虛框不再是「未來工作」，13 函數 E2E 已完成
- [x] M2: proposal.html S5.2 — limitation: ULP scope 降為「低」，附 E2E 實測數據
- [x] M3: proposal.html S6 — 新增 E2E summary table（13 函數, 7 欄）
- [x] M4: contribution-comparison.html S5 — limitation #1: 附 E2E 實測數據 + 剩餘限制
- [x] M5: degree_selection_report.html S11 — 全部估計值替換為 KZG 實測值
- [x] M6: research-background.html — 掃描完畢，無需修改（無 RR/E2E 相關內容）
- [x] M7: TODO-fixes.md — 此區段

### 數據來源
`benchmark_results.json` (post-Bug-B-fix + Issue-06-fix, 2026-03-14)
所有值為 KZG mode, BN254 + SHPLONK, release build, median of 5 runs.

### 新增 Issue 06: arcsin integer division
Python E2E verification 發現 arcsin.rs `((S-a)/2)*S` → `(S-a)*S/2`。
- 影響：x=S-1 時 Z=0（正確應為 32768），ULP 362→3
- 修正：僅 witness computation，不影響 constraints、proof size
- 驗證：39 tests + KZG benchmark 全部通過

### Python E2E Math Verification
`python/verify_e2e_math.py`：獨立驗證全部 13 函數的數學正確性
- Phase 1: 14 kernel CoeffSets, 98 checks, all ≤4 ULP at w level
- Phase 2: 13 E2E pipelines, 105 checks, all pass
