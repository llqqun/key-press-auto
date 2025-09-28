# key-press-auto
自动按键脚本配置

python版本：3.12

## 更新说明
- 已将底层输入库从 `pydirectinput` 替换为 Windows 原生 `SendInput` API
- 新的实现使用 `game_input_sendinput.py`，提供更好的游戏兼容性
- 保留原有的 `pydirectinput` 实现作为备份方案


## 安装依赖
```
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

## 运行
```
python main.py
```
