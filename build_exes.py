#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
编译脚本，将所有Python文件编译为单独的exe文件
"""

import os
import subprocess
import sys
from pathlib import Path


def compile_python_to_exe(script_path, output_dir="dist"):
    """
    将单个Python脚本编译为exe文件
    
    Args:
        script_path (str): Python脚本路径
        output_dir (str): 输出目录
    
    Returns:
        bool: 编译是否成功
    """
    try:
        # 获取脚本名称（不含扩展名）
        script_name = Path(script_path).stem
        
        print(f"正在编译 {script_path}...")
        
        # 构建PyInstaller命令
        # --onefile: 生成单个exe文件
        # --windowed: 对于GUI应用，不显示控制台窗口
        # --name: 指定生成的exe文件名
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            f"--name={script_name}",
            f"--distpath={output_dir}",
            script_path
        ]
        
        # 执行编译命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"成功编译 {script_path} -> {output_dir}/{script_name}.exe")
            return True
        else:
            print(f"编译 {script_path} 失败:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"编译 {script_path} 时发生异常: {str(e)}")
        return False


def clean_build_artifacts():
    """
    清理编译过程中产生的临时文件和目录
    """
    # 删除build目录
    build_dir = "build"
    if os.path.exists(build_dir):
        try:
            import shutil
            shutil.rmtree(build_dir)
            print(f"已删除 {build_dir} 目录")
        except Exception as e:
            print(f"删除 {build_dir} 目录时出错: {str(e)}")
    
    # 删除spec文件
    for spec_file in Path(".").glob("*.spec"):
        try:
            spec_file.unlink()
            print(f"已删除 {spec_file} 文件")
        except Exception as e:
            print(f"删除 {spec_file} 文件时出错: {str(e)}")


def main():
    """
    主函数：编译所有Python文件为exe
    """
    print("开始编译Python文件为exe...")
    
    # 确保已安装PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("错误: 未找到PyInstaller，请先安装:")
        print("pip install pyinstaller")
        sys.exit(1)
    
    # 查找所有Python文件（除了当前脚本）
    current_script = Path(__file__).name
    python_files = []
    
    for py_file in Path(".").glob("*.py"):
        if py_file.name != current_script:
            python_files.append(str(py_file))
    
    if not python_files:
        print("未找到需要编译的Python文件")
        return
    
    print(f"找到 {len(python_files)} 个Python文件需要编译:")
    for py_file in python_files:
        print(f"  - {py_file}")
    
    # 编译每个Python文件
    success_count = 0
    for py_file in python_files:
        if compile_python_to_exe(py_file):
            success_count += 1
    
    # 清理临时文件
    print("\n正在清理临时文件...")
    clean_build_artifacts()
    
    # 输出总结
    print(f"\n编译完成: {success_count}/{len(python_files)} 个文件编译成功")
    
    if success_count == len(python_files):
        print("所有文件均已成功编译!")
    else:
        print("部分文件编译失败，请查看上面的错误信息")


if __name__ == "__main__":
    main()