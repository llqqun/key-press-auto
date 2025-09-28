#!/usr/bin/env python3
"""
测试SendInput实现的脚本
"""
import time
from game_input_sendinput import GameSendInput

def test_keyboard():
    """测试键盘输入"""
    print("测试键盘输入...")
    game_input = GameSendInput()
    
    # 测试基本按键
    print("按下 'a' 键")
    game_input.press_key('a')
    time.sleep(1)
    
    print("按下 'enter' 键")
    game_input.press_key('enter')
    time.sleep(1)
    
    # 测试组合键（先按住shift，再按a，然后释放）
    print("测试组合键：Shift + A")
    game_input.hold_key('shift')
    time.sleep(0.1)
    game_input.press_key('a')
    time.sleep(0.1)
    game_input.release_key('shift')
    time.sleep(1)

def test_mouse():
    """测试鼠标输入"""
    print("测试鼠标输入...")
    game_input = GameSendInput()
    
    # 测试鼠标点击（在屏幕中央）
    print("在屏幕中央点击")
    screen_width = 1920  # 假设屏幕宽度
    screen_height = 1080  # 假设屏幕高度
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    game_input.click(center_x, center_y)
    time.sleep(1)
    
    # 测试右键点击
    print("右键点击")
    game_input.click(center_x + 100, center_y, button='right')
    time.sleep(1)

if __name__ == "__main__":
    print("SendInput 测试开始")
    print("请在3秒内切换到目标窗口...")
    time.sleep(3)
    
    try:
        test_keyboard()
        test_mouse()
        print("测试完成！")
    except Exception as e:
        print(f"测试出错: {e}")
        import traceback
        traceback.print_exc()