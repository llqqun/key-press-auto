import json
import os
from dataclasses import dataclass, asdict

CONFIG_FILE = "shortcuts.json"

@dataclass
class Config:
    keys: list           # 快捷键配置

    def __init__(self):
        self.keys = self._get_default_keys()
        self._load_config()
    
    def _load_config(self):
        """从配置文件加载快捷键设置"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.keys = data.get('keys', self._get_default_keys())
            except:
                # 如果加载失败，返回默认配置
                return self._get_default_keys()
        else:
            return self._get_default_keys()
    
    def _get_default_keys(self):
        """获取默认快捷键配置"""
        return [
            {
                "key": "alt+f10",
                "title": "启动/暂停",
            },
            {
                "key": "alt+f11",
                "title": "停止",
            }
        ]
    
    def save_config(self):
        """保存配置到文件"""
        config_data = {
            'keys': self.keys
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
    
    def to_dict(self):
        # 将对象转换为字典，用于JSON序列化
        return asdict(self)
    
    def get_key_by_title(self, title):
        """根据标题获取快捷键"""
        for key_config in self.keys:
            if key_config['title'] == title:
                return key_config['key']
        return None

config = Config()
