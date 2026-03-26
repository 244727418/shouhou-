#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库修复脚本 - 修复缺失的 global_settings 表
"""

import sqlite3
import os
import shutil
from datetime import datetime

def backup_database():
    """备份数据库文件"""
    if os.path.exists("refund_data.db"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"refund_data_backup_{timestamp}.db"
        shutil.copy("refund_data.db", backup_name)
        print(f"✅ 数据库已备份为: {backup_name}")
        return backup_name
    return None

def check_database_tables():
    """检查数据库表结构"""
    print("🔍 检查数据库表结构...")
    
    conn = sqlite3.connect("refund_data.db")
    cursor = conn.cursor()
    
    # 检查所有表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("📊 现有表:", [table[0] for table in tables])
    
    # 检查 global_settings 表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='global_settings'")
    if cursor.fetchone():
        print("✅ global_settings 表存在")
        # 检查表结构
        cursor.execute("PRAGMA table_info(global_settings)")
        columns = cursor.fetchall()
        print("📋 global_settings 表结构:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        conn.close()
        return True
    else:
        print("❌ global_settings 表不存在")
        conn.close()
        return False

def create_global_settings_table():
    """创建 global_settings 表"""
    print("🔨 创建 global_settings 表...")
    
    conn = sqlite3.connect("refund_data.db")
    cursor = conn.cursor()
    
    # 创建 global_settings 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS global_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT UNIQUE NOT NULL,
            setting_value TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 插入默认设置
    default_settings = [
        ("daily_orders", "100", "日单量"),
        ("daily_sales", "5000", "日销售金额"),
        ("refund_rate", "0.05", "退款率"),
        ("store_name", "我的店铺", "店铺名称"),
        ("theme", "light", "界面主题"),
        ("language", "zh", "界面语言")
    ]
    
    for key, value, desc in default_settings:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO global_settings (setting_key, setting_value, description)
                VALUES (?, ?, ?)
            """, (key, value, desc))
        except:
            pass
    
    conn.commit()
    conn.close()
    print("✅ global_settings 表创建完成")

def check_other_tables():
    """检查其他可能缺失的表"""
    print("\n🔍 检查其他表结构...")
    
    conn = sqlite3.connect("refund_data.db")
    cursor = conn.cursor()
    
    # 检查 refund_records 表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='refund_records'")
    if not cursor.fetchone():
        print("❌ refund_records 表不存在，需要创建")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS refund_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                customer_name TEXT,
                product_name TEXT,
                refund_amount REAL,
                refund_reason TEXT,
                refund_date TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ refund_records 表已创建")
    else:
        print("✅ refund_records 表存在")
    
    conn.commit()
    conn.close()

def main():
    """主函数"""
    print("=" * 60)
    print("🔧 数据库修复脚本")
    print("💡 修复缺失的 global_settings 表")
    print("=" * 60)
    
    # 检查数据库文件是否存在
    if not os.path.exists("refund_data.db"):
        print("❌ 找不到数据库文件 refund_data.db")
        print("💡 将创建新的数据库文件")
        # 创建空的数据库文件
        open("refund_data.db", "w").close()
    
    # 备份数据库
    backup_file = backup_database()
    
    # 检查表结构
    if check_database_tables():
        print("\n✅ 数据库表结构正常")
    else:
        print("\n🔨 开始修复数据库...")
        create_global_settings_table()
        check_other_tables()
        
        # 验证修复结果
        if check_database_tables():
            print("\n🎉 数据库修复完成！")
        else:
            print("\n❌ 数据库修复失败")
    
    print("\n💡 现在可以重新运行程序了")
    input("按 Enter 键退出...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        input("按 Enter 键退出...")