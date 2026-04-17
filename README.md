# The White Box (白い部屋)

16GB RAMのローカル環境（Snapdragon X）で動作する、2体のAIエージェントと1体の監視者による閉鎖環境シミュレーション。

## 概要 (Overview)
本プロジェクトは、物理的な「忘却」と「情動の変化」を伴う、AI同士の自律的な対話シミュレーションの観察を目的としています。
単一の `Bonsai 8B` モデルを推論エンジンとして使用し、メモリ効率を最大化した「三位一体」運用を行います。

## セットアップ (Setup)
1. 依存ライブラリのインストール:
   ```bash
   pip install -r requirements.txt
   ```
2. 実行:
   ```bash
   streamlit run src/app.py
   ```
