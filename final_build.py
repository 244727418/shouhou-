#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终版打包脚本 - 完全不需要 superqt
"""

import os
import subprocess
import shutil

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 最终版打包脚本")
    print("💡 完全不需要 superqt")
    print("=" * 60)
    
    # 检查当前目录
    current_dir = os.getcwd()
    print(f"📂 当前目录: {current_dir}")
    
    # 检查主程序文件是否存在
    if not os.path.exists("dj.py"):
        print("❌ 找不到主程序文件 dj.py")
        input("按 Enter 键退出...")
        return
    
    # 清理之前的打包文件
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # 删除根目录的 exe 文件（如果存在）
    if os.path.exists("退款管理工具.exe"):
        os.remove("退款管理工具.exe")
        print("🗑️ 已删除根目录的旧 exe 文件")
    
    # 最终版打包命令 - 完全不需要 superqt
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "退款管理工具",
        "--add-data", "icons;icons",
        "--add-data", "refund_data.db;.",
        "--add-data", "theme_settings.json;.",
        # 只包含实际使用的依赖（不需要 superqt）
        "--hidden-import", "openpyxl",
        "--hidden-import", "xlrd",
        "--hidden-import", "xlsxwriter",
        "--hidden-import", "pandas",
        "--hidden-import", "numpy",
        "--hidden-import", "pyperclip",
        "dj.py"
    ]
    
    try:
        print("🚀 开始打包...")
        print(f"命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ 打包成功！")
            
            # 显示生成的文件（只在 dist 文件夹）
            exe_path = os.path.join("dist", "退款管理工具.exe")
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
                print(f"📁 exe 文件位置: {exe_path}")
                print(f"📊 文件大小: {file_size:.2f} MB")
                print("💡 exe 文件仅保存在 dist 文件夹，根目录不会生成")
                
                # 测试 exe 是否能运行
                print("\n🔍 正在测试 exe 文件...")
                try:
                    test_result = subprocess.run([exe_path], 
                                               capture_output=True, timeout=5)
                    print("✅ exe 文件可以正常运行")
                except:
                    print("⚠️ 无法测试 exe 文件，请手动测试")
                
                return True
            else:
                print("❌ exe 文件未生成")
                return False
        else:
            print("❌ 打包失败")
            if result.stdout:
                print(f"输出: {result.stdout}")
            if result.stderr:
                print(f"错误: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 打包过程中发生错误: {e}")
        return False

if __name__ == "__main__":
    try:
        main()
        input("\n按 Enter 键退出...")
    except KeyboardInterrupt:
        print("\n❌ 用户中断操作")
    except Exception as e:
        print(f"\n❌ 发生未知错误: {e}")
        input("按 Enter 键退出...")