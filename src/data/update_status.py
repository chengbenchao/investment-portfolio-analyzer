#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数据更新状态文件工具。"""

from __future__ import annotations
import json
import os
from datetime import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
STATUS_FILE = os.path.join(PROJECT_ROOT, 'logs', 'data_update_status.json')


def _ensure_dir() -> None:
    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)


def load_status() -> dict:
    _ensure_dir()
    if not os.path.exists(STATUS_FILE):
        return {
            'last_attempt_at': None,
            'last_success_at': None,
            'last_error': None,
            'last_mode': None,
            'last_updated_count': 0,
            'data_file': 'src/api/full_realtime_data.json'
        }
    with open(STATUS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_status(patch: dict) -> dict:
    status = load_status()
    status.update(patch)
    _ensure_dir()
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=2)
    return status


def now_str() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
