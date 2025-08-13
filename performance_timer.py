import time
import csv
import os
from datetime import datetime
from typing import Optional, List, Dict


class PerformanceTimer:
    """
    WindowsネイティブアプリのGUIパフォーマンス計測用タイマー
    
    使用方法:
    timer = PerformanceTimer()
    timer.start(desc="画面の保存")
    # ... 操作実行 ...
    timer.stop()
    """
    
    def __init__(self, csv_filename: str = "performance_log.csv"):
        """
        パフォーマンスタイマーの初期化
        
        Args:
            csv_filename (str): 出力するCSVファイル名（デフォルト: performance_log.csv）
        """
        self.csv_filename = csv_filename
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.operation: Optional[str] = None
        self.iteration: Optional[int] = None
        self.records: List[Dict[str, str]] = []
        
        # CSVファイルが存在しない場合はヘッダーを作成
        if not os.path.exists(csv_filename):
            self._create_csv_header()
    
    def _create_csv_header(self):
        """CSVファイルのヘッダーを作成"""
        with open(self.csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['開始時刻', '終了時刻', '所要時間(秒)', '操作', '回数'])
    
    def _round_to_tenth(self, timestamp: float) -> float:
        """
        タイムスタンプを0.1秒単位に丸める
        
        Args:
            timestamp (float): 元のタイムスタンプ
            
        Returns:
            float: 0.1秒単位に丸められたタイムスタンプ
        """
        return round(timestamp, 1)
    
    def _format_timestamp(self, timestamp: float) -> str:
        """
        タイムスタンプを日時形式に変換（0.1秒単位）
        
        Args:
            timestamp (float): UNIXタイムスタンプ
            
        Returns:
            str: YYYY-MM-DD HH:MM:SS.S 形式の文字列（0.1秒単位）
        """
        dt = datetime.fromtimestamp(timestamp)
        # 0.1秒単位で丸められたミリ秒部分を計算
        milliseconds = int((timestamp % 1) * 10)  # 0.1秒単位
        return dt.strftime('%Y-%m-%d %H:%M:%S') + f'.{milliseconds}'
    
    def start(self, operation: str = "", iteration: Optional[int] = None):
        """
        タイマーを開始
        
        Args:
            operation (str): 操作
            iteration (Optional[int]): 操作の回数（1, 2, 3...）。指定すると説明に含められます
        """
        self.start_time = self._round_to_tenth(time.time())
        self.iteration = iteration
        self.operation = operation
            
        self.end_time = None
        formatted_time = self._format_timestamp(self.start_time)
        print(f"タイマー開始: {self.operation} (時刻: {formatted_time})")
    
    def stop(self) -> Optional[float]:
        """
        タイマーを停止し、所要時間を計算
        
        Returns:
            Optional[float]: 所要時間（秒）、start()が呼ばれていない場合はNone
        """
        if self.start_time is None:
            print("警告: start()が呼ばれていません")
            return None
        
        self.end_time = self._round_to_tenth(time.time())
        duration = self._round_to_tenth(self.end_time - self.start_time)
        
        # 記録を作成
        record = {
            'start_time': self._format_timestamp(self.start_time),
            'end_time': self._format_timestamp(self.end_time),
            'duration': str(duration),
            'operation': self.operation or "",
            'iteration': str(self.iteration) if self.iteration is not None else ""
        }
        self.records.append(record)
        
        print(f"タイマー停止: {self.operation} (所要時間: {duration}秒)")
        
        # CSVに即座に出力
        self._write_to_csv(record)
        
        # リセット
        self.start_time = None
        self.end_time = None
        self.operation = None
        self.iteration = None
        
        return duration
    
    def _write_to_csv(self, record: Dict[str, str]):
        """
        記録をCSVファイルに書き込み
        
        Args:
            record (Dict[str, str]): 記録データ
        """
        with open(self.csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                record['start_time'],
                record['end_time'],
                record['duration'],
                record['operation'],
                record['iteration']
            ])
    
    def get_all_records(self) -> List[Dict[str, str]]:
        """
        すべての記録を取得
        
        Returns:
            List[Dict[str, str]]: 記録のリスト
        """
        return self.records.copy()
    
    def clear_records(self):
        """メモリ上の記録をクリア"""
        self.records.clear()
    
    def export_records(self, filename: str = None):
        """
        記録を別ファイルにエクスポート
        
        Args:
            filename (str): エクスポート先ファイル名（指定しない場合は現在時刻で自動生成）
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"performance_export_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['開始時刻', '終了時刻', '所要時間(秒)', '操作', '回数'])
            
            for record in self.records:
                writer.writerow([
                    record['start_time'],
                    record['end_time'],
                    record['duration'],
                    record['operation'],
                    record['iteration']
                ])
        
        print(f"記録を {filename} にエクスポートしました")


# 使用例
if __name__ == "__main__":
    # 使用例
    timer = PerformanceTimer()
    
    # 基本的なテスト実行
    timer.start(operation="画面の保存")
    time.sleep(1.5)  # 1.5秒待機（実際の操作をシミュレート）
    timer.stop()
    
    timer.start(operation="データの読み込み")
    time.sleep(0.8)  # 0.8秒待機
    timer.stop()
    
    # 複数回の同じ操作を記録する例
    for i in range(1, 4):  # 1回目、2回目、3回目
        timer.start(operation="ファイル処理", iteration=i)
        time.sleep(0.5 + i * 0.2)  # 回数に応じて時間が変わる
        timer.stop()
    
    print("すべての記録:")
    for record in timer.get_all_records():
        print(f"  {record['operation']}: {record['duration']}秒")
