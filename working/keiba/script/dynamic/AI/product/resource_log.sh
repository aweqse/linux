#!/bin/bash

# 保存先ディレクトリを指定
LOG_DIR="/home/aweqse/keiba/log"

# ディレクトリがなければ作成
mkdir -p "$LOG_DIR"

# 永続ループ
while true
do
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_DIR/top.log"
  top -b -n 1 >> "$LOG_DIR/top.log"

  echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_DIR/iostat.log"
  iostat -xz 1 1 >> "$LOG_DIR/iostat.log"

  sleep 5
done
