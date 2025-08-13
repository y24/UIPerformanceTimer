# UIPerformanceTimer

WindowsネイティブアプリのGUIパフォーマンス計測用のシンプルなPythonモジュールです。

## 機能

- 操作の開始・終了時刻を0.1秒単位で記録
- 所要時間の自動計算
- CSVファイルへの自動出力
- 操作説明（operation）による識別
- 操作回数（iteration）の記録

## インストール

特別なインストールは不要です。Pythonの標準ライブラリのみを使用しています。

## 基本的な使用方法

```python
from performance_timer import PerformanceTimer

# タイマーのインスタンス作成
timer = PerformanceTimer()

# タイマー開始
timer.start(operation="画面の保存")

# ... 実際のUI操作 ...

# タイマー停止
duration = timer.stop()
print(f"所要時間: {duration}秒")
```

## 詳細な使用例

```python
from performance_timer import PerformanceTimer
import time

# タイマーのインスタンス作成（CSVファイル名を指定可能）
timer = PerformanceTimer("my_performance_log.csv")

# 複数の操作を計測
timer.start(operation="画面の保存")
time.sleep(1.5)  # 実際の操作をシミュレート
timer.stop()

timer.start(operation="データの読み込み")
time.sleep(0.8)  # 実際の操作をシミュレート
timer.stop()

timer.start(operation="ファイルのエクスポート")
time.sleep(2.3)  # 実際の操作をシミュレート
timer.stop()

# 複数回の同じ操作を記録
for i in range(1, 4):
    timer.start(operation="ファイル処理", iteration=i)
    time.sleep(0.5 + i * 0.2)
    timer.stop()

# すべての記録を取得
records = timer.get_all_records()
for record in records:
    print(f"{record['operation']}: {record['duration']}秒")

# 記録を別ファイルにエクスポート
timer.export_records("detailed_report.csv")
```

## CSVファイルの出力形式

以下の列を含むCSVファイルが自動生成されます：

| 列名 | 説明 |
|------|------|
| 開始時刻 | 操作開始時のタイムスタンプ（0.1秒単位） |
| 終了時刻 | 操作終了時のタイムスタンプ（0.1秒単位） |
| 所要時間(秒) | 操作にかかった時間 |
| 操作 | start()で指定したoperation |
| 回数 | start()で指定したiteration（指定しない場合は空） |

## メソッド一覧

### `__init__(csv_filename="performance_log.csv")`
- タイマーの初期化
- CSVファイル名を指定可能

### `start(operation="", iteration=None)`
- タイマー開始
- `operation`: 操作の説明文字列
- `iteration`: 操作の回数（1, 2, 3...）。指定すると説明に含められます

### `stop()`
- タイマー停止
- 所要時間を計算してCSVに出力
- 所要時間を返す

### `get_all_records()`
- メモリ上のすべての記録を取得

### `clear_records()`
- メモリ上の記録をクリア

### `export_records(filename=None)`
- 記録を別ファイルにエクスポート
- ファイル名を指定しない場合は自動生成

## 注意事項

- タイムスタンプは0.1秒単位に丸められます
- CSVファイルはUTF-8エンコーディングで出力されます
- 各操作の記録は`stop()`時に即座にCSVファイルに書き込まれます
- `start()`を呼ばずに`stop()`を呼ぶと警告が表示されます

## 実際のUI操作での使用例

```python
from performance_timer import PerformanceTimer
import pyautogui  # 例としてpyautoguiを使用

timer = PerformanceTimer()

# ボタンクリックの計測
timer.start(operation="保存ボタンクリック")
pyautogui.click(x=100, y=200)  # 実際のUI操作
timer.stop()

# メニュー選択の計測
timer.start(operation="ファイルメニュー選択")
pyautogui.click(x=50, y=50)
pyautogui.click(x=50, y=100)
timer.stop()

# 複数回の同じ操作を計測
for i in range(1, 6):
    timer.start(operation="ボタンクリック", iteration=i)
    pyautogui.click(x=200, y=300)
    timer.stop()
```
