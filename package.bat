@echo off

REM 检查是否安装了PyInstaller
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo 正在安装PyInstaller...
    pip install pyinstaller -i https://pypi.org/simple/
    if %errorlevel% neq 0 (
        echo 安装PyInstaller失败，请手动安装后重试。
        pause
        exit /b 1
    )
)

REM 使用PyInstaller进行打包
pyinstaller --clean pack.spec

if %errorlevel% equ 0 (
    echo 打包成功！可执行文件位于dist目录下。
    pause
) else (
    echo 打包失败，请查看错误信息。
    pause
    exit /b 1
)