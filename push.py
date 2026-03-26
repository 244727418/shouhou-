#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动 Git 推送脚本
功能：自动执行 git add、commit、push 操作
作者：自动生成
"""

import subprocess
import sys
import os
from datetime import datetime
import time

def run_command(command, description):
    """
    执行命令并处理结果
    """
    print(f"\n【正在执行】{description}")
    print(f"命令: {command}")
    
    try:
        # 执行命令
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        
        # 输出命令执行结果
        if result.stdout:
            print(f"输出: {result.stdout.strip()}")
        
        if result.stderr:
            print(f"错误: {result.stderr.strip()}")
        
        # 检查命令是否成功执行
        if result.returncode == 0:
            print(f"✅ {description} 成功")
            return True
        else:
            print(f"❌ {description} 失败")
            return False
            
    except Exception as e:
        print(f"❌ 执行 {description} 时发生异常: {str(e)}")
        return False

def check_git_installed():
    """
    检查 Git 是否已安装
    """
    print("🔍 检查 Git 是否已安装...")
    try:
        result = subprocess.run("git --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git 已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git 未安装或未添加到系统 PATH")
            return False
    except Exception as e:
        print(f"❌ 检查 Git 时发生异常: {str(e)}")
        return False

def check_git_repository():
    """
    检查当前目录是否为 Git 仓库
    """
    print("🔍 检查当前目录是否为 Git 仓库...")
    
    # 检查是否存在 .git 文件夹
    if not os.path.exists(".git"):
        print("❌ 当前目录不是 Git 仓库")
        print("💡 请先运行: git init")
        return False
    
    # 检查远程仓库配置
    try:
        result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout:
            print("✅ 已配置远程仓库:")
            print(result.stdout)
            return True
        else:
            print("❌ 未配置远程仓库")
            print("💡 请先运行: git remote add origin https://github.com/244727418/shouhou-.git")
            return False
    except Exception as e:
        print(f"❌ 检查远程仓库时发生异常: {str(e)}")
        return False

def main():
    """
    主函数 - 执行 Git 推送流程
    """
    print("=" * 60)
    print("🚀 Git 自动推送脚本")
    print("=" * 60)
    
    # 获取当前日期时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"更新：{current_time}"
    
    print(f"📅 当前时间: {current_time}")
    print(f"💬 提交信息: {commit_message}")
    
    # 检查前置条件
    if not check_git_installed():
        print("\n❌ 请先安装 Git 并确保已添加到系统 PATH")
        print("💡 下载地址: https://git-scm.com/downloads")
        input("按 Enter 键退出...")
        return
    
    if not check_git_repository():
        print("\n❌ 请先初始化 Git 仓库并配置远程仓库")
        input("按 Enter 键退出...")
        return
    
    print("\n" + "=" * 60)
    print("开始执行 Git 推送流程...")
    print("=" * 60)
    
    # 步骤1: git add .
    if not run_command("git add .", "添加所有文件到暂存区"):
        print("\n❌ 添加文件失败，请检查文件状态")
        input("按 Enter 键退出...")
        return
    
    # 步骤2: git commit
    if not run_command(f'git commit -m "{commit_message}"', "提交更改"):
        print("\n❌ 提交失败，可能没有需要提交的更改")
        
        # 检查是否有未暂存的更改
        result = subprocess.run("git status", shell=True, capture_output=True, text=True)
        print("\n当前 Git 状态:")
        print(result.stdout)
        
        input("按 Enter 键退出...")
        return
    
    # 步骤3: git push
    print("\n" + "=" * 60)
    print("开始推送到远程仓库...")
    print("=" * 60)
    
    if run_command("git push origin main", "推送到远程仓库"):
        print("\n🎉 Git 推送流程完成！")
        print(f"✅ 所有更改已成功推送到远程仓库")
    else:
        print("\n❌ 推送失败，请检查网络连接和权限")
        print("💡 如果这是第一次推送，请尝试: git push -u origin main")
    
    # 显示最终状态
    print("\n" + "=" * 60)
    print("最终 Git 状态:")
    subprocess.run("git status", shell=True)
    print("=" * 60)
    
    # 暂停以便查看结果
    input("\n按 Enter 键退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断操作")
        input("按 Enter 键退出...")
    except Exception as e:
        print(f"\n❌ 发生未知错误: {str(e)}")
        input("按 Enter 键退出...")