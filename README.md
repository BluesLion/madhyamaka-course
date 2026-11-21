# madhyamaka-course

佛典思想史每日課程：以中觀（Madhyamaka）為主軸。每天一課、約 15 分鐘，共 174 課。

從阿含的緣起與中道、部派阿毘達磨、般若經，讀到龍樹《中論》與《大智度論》，再順著歷史看中觀如何被漢傳三論、唯識、如來藏、密教、天台華嚴禪與藏傳各宗接續或回應。

線上閱讀（啟用 GitHub Pages 後）：https://blueslion.github.io/madhyamaka-course/

## 每課格式

1. **脈絡**：時代、作者、這段文字在回應什麼問題
2. **原文**：附經論名、卷次與 [CBETA](https://cbetaonline.dila.edu.tw/) 連結（連到行首）
3. **逐句解說**
4. **名詞卡**：中文、梵文、定義、之後在哪一課再出現
5. **回扣與預告**

課後提問會直接展開在課文裡，每一問用一種顏色標示。

## 單元

| 單元 | 主題 | 課次 |
| --- | --- | --- |
| 一 | 阿含的緣起與中道 | 1–10 |
| 二 | 部派與阿毘達磨 | 11–20 |
| 三 | 般若經：空的出現 | 21–32 |
| 四 | 龍樹《中論》 | 33–66 |
| 五 | 龍樹其他論著與提婆 | 67–78 |
| 六 | 《大智度論》 | 79–98 |
| 七 | 中觀在中國 | 99–112 |
| 八 | 瑜伽行派的回應 | 113–126 |
| 九 | 如來藏與佛性 | 127–136 |
| 十 | 後期印度中觀與密教 | 137–152 |
| 十一 | 漢傳宗派的綜合 | 153–164 |
| 十二 | 藏傳中觀 | 165–174 |

## 目錄結構

```
index.html            首頁與課程目錄（由 build.py 產生）
lessons/NNN.html      每課頁面（由 build.py 產生）
src/lessons/NNN.html  每課內文片段（手寫，開頭含 meta）
data/syllabus.json    174 課的課綱
assets/style.css      共用樣式（含深色模式）
build.py              產生網站，只用 Python 標準函式庫
```

新增或修改一課：編輯 `src/lessons/NNN.html`，然後執行

```
python build.py
```

## 啟用 GitHub Pages

Repo 的 Settings → Pages → Source 選 **Deploy from a branch**，Branch 選 `main`、資料夾 `/ (root)`。

## 經文來源

經文引自 [CBETA 線上閱讀](https://cbetaonline.dila.edu.tw/)（中華電子佛典協會）。巴利經典連至 [SuttaCentral](https://suttacentral.net/)。
