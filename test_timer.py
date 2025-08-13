#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
パフォーマンスタイマーモジュールのテストスクリプト
"""

from performance_timer import PerformanceTimer
import time


def test_basic_functionality():
    """基本的な機能のテスト"""
    print("=== 基本的な機能テスト ===")
    
    timer = PerformanceTimer("test_basic.csv")
    
    # テスト1: 基本的なstart/stop
    timer.start(desc="テスト操作1")
    time.sleep(1.0)
    duration = timer.stop()
    print(f"テスト操作1の所要時間: {duration}秒")
    
    # テスト2: 短い操作
    timer.start(desc="テスト操作2")
    time.sleep(0.3)
    duration = timer.stop()
    print(f"テスト操作2の所要時間: {duration}秒")
    
    # テスト3: 長い操作
    timer.start(desc="テスト操作3")
    time.sleep(2.5)
    duration = timer.stop()
    print(f"テスト操作3の所要時間: {duration}秒")


def test_multiple_operations():
    """複数操作の連続テスト"""
    print("\n=== 複数操作の連続テスト ===")
    
    timer = PerformanceTimer("test_multiple.csv")
    
    operations = [
        ("画面の保存", 1.2),
        ("データの読み込み", 0.8),
        ("ファイルのエクスポート", 1.8),
        ("設定の変更", 0.5)
    ]
    
    for desc, sleep_time in operations:
        timer.start(desc=desc)
        time.sleep(sleep_time)
        duration = timer.stop()
        print(f"{desc}: {duration}秒")
    
    # すべての記録を表示
    print("\nすべての記録:")
    records = timer.get_all_records()
    for record in records:
        print(f"  {record['description']}: {record['duration']}秒")


def test_error_handling():
    """エラーハンドリングのテスト"""
    print("\n=== エラーハンドリングテスト ===")
    
    timer = PerformanceTimer("test_error.csv")
    
    # stop()をstart()なしで呼び出すテスト
    print("start()なしでstop()を呼び出し:")
    result = timer.stop()
    print(f"結果: {result}")


def test_csv_output():
    """CSV出力のテスト"""
    print("\n=== CSV出力テスト ===")
    
    timer = PerformanceTimer("test_csv_output.csv")
    
    # いくつかの操作を実行
    timer.start(desc="CSVテスト操作1")
    time.sleep(0.7)
    timer.stop()
    
    timer.start(desc="CSVテスト操作2")
    time.sleep(1.3)
    timer.stop()
    
    # エクスポート機能のテスト
    timer.export_records("test_export.csv")
    
    print("CSVファイルが正常に作成されました")


def main():
    """メイン関数"""
    print("パフォーマンスタイマーモジュールのテストを開始します\n")
    
    try:
        test_basic_functionality()
        test_multiple_operations()
        test_error_handling()
        test_csv_output()
        
        print("\n=== すべてのテストが完了しました ===")
        print("生成されたCSVファイルを確認してください:")
        print("- test_basic.csv")
        print("- test_multiple.csv")
        print("- test_error.csv")
        print("- test_csv_output.csv")
        print("- test_export.csv")
        
    except Exception as e:
        print(f"テスト中にエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
