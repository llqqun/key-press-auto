#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成PyInstaller打包配置文件的脚本
可以根据需要自定义配置参数
"""
import os
import argparse

def generate_spec_file(output_path='pack.spec', app_name='按键精灵', entry_point='main.py', 
                       include_files=None, hidden_imports=None, console=False):
    """
    生成PyInstaller的spec配置文件
    
    参数:
    output_path: 输出的spec文件路径
    app_name: 应用程序名称
    entry_point: 程序入口文件
    include_files: 要包含的额外文件列表，格式为[(源路径, 目标路径), ...]
    hidden_imports: 隐藏的导入模块列表
    console: 是否显示控制台窗口
    """
    # 默认包含的文件
    if include_files is None:
        include_files = [
            ('shortcuts.json', '.'),
            ('demo.json', '.')
        ]
    
    # 默认隐藏的导入模块
    if hidden_imports is None:
        hidden_imports = ['keyboard', 'PyQt6', 'PyAutoGUI']
    
    # 当前目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 生成文件内容
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

    block_cipher = None

    # 要包含的额外文件
    added_files = [
    {',\n'.join([f"    ('{src}', '{dest}')" for src, dest in include_files])}
    ]

    # 分析代码和依赖项
    a = Analysis(['{entry_point}'],
                pathex=['{current_dir}'],
                binaries=[],
                datas=added_files,
                hiddenimports={hidden_imports},
                hookspath=[],
                hooksconfig={{}},
                runtime_hooks=[],
                excludes=[],
                win_no_prefer_redirects=False,
                win_private_assemblies=False,
                cipher=block_cipher,
                noarchive=False)

    # 创建Python Zipped Archive
    pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

    # 创建可执行文件
    exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            [],
            name='{app_name}',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            upx_exclude=[],
            runtime_tmpdir=None,
            console={console},
            disable_windowed_traceback=False,
            target_arch=None,
            codesign_identity=None,
            entitlements_file=None)
    """
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"配置文件已生成: {os.path.abspath(output_path)}")
    print(f"应用名称: {app_name}")
    print(f"入口文件: {entry_point}")
    print(f"包含文件: {include_files}")
    print(f"隐藏导入: {hidden_imports}")
    print(f"显示控制台: {console}")


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='生成PyInstaller打包配置文件')
    parser.add_argument('--output', '-o', default='pack.spec', help='输出的spec文件路径')
    parser.add_argument('--name', '-n', default='按键精灵', help='应用程序名称')
    parser.add_argument('--entry', '-e', default='main.py', help='程序入口文件')
    parser.add_argument('--console', '-c', action='store_true', help='显示控制台窗口')
    
    args = parser.parse_args()
    
    # 生成配置文件
    generate_spec_file(
        output_path=args.output,
        app_name=args.name,
        entry_point=args.entry,
        console=args.console
    )


if __name__ == '__main__':
    main()