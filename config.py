import random
from dataclasses import dataclass, asdict

@dataclass
class Step:
    key: str           # 按键
    delay: float       # 基础延迟（秒）
    random_offset: float = 0.1  # 随机波动（秒）

    def get_wait_time(self):
        if self.random_offset > 0:
            return self.delay + random.uniform(-self.random_offset, self.random_offset)
        return self.delay
    
    def to_dict(self):
        # 将Step对象转换为字典，用于JSON序列化
        return asdict(self)
