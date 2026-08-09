from typing import Dict, Any, Callable


class SmartDevice:
    def __init__(self, name: str):
        self.name = name
        self.actions: Dict[str, Callable[[Dict[str, Any]], str]] = {}

    @property
    def aciton_list(self):
        return list(self.actions.keys())

    def execute_action(self, action: str, parameters: Dict[str, Any]) -> str:
        """
        根据字典映射执行操作。
        """
        if action in self.actions:
            return self.actions[action](parameters)
        else:
            return f"{self.name} 不支持操作 {action}"


class SmartLight(SmartDevice):
    def __init__(self, name: str):
        super().__init__(name)
        self.actions = {
            "turn_on": self.turn_on,
            "turn_off": self.turn_off,
            "adjust_brightness": self.adjust_brightness,
            "change_color": self.change_color,
        }

    def turn_on(self, parameters: Dict[str, Any]) -> str:
        return f"{self.name} 已开启"

    def turn_off(self, parameters: Dict[str, Any]) -> str:
        return f"{self.name} 已关闭"

    def adjust_brightness(self, parameters: Dict[str, Any]) -> str:
        level = parameters.get("level", "default")
        return f"{self.name} 的亮度已调整到 {level}"

    def change_color(self, parameters: Dict[str, Any]) -> str:
        color = parameters.get("color", "white")
        return f"{self.name} 的颜色已更改为 {color}"


class SmartAirConditioner(SmartDevice):
    def __init__(self, name: str):
        super().__init__(name)
        self.actions = {
            "turn_on": self.turn_on,
            "turn_off": self.turn_off,
            "set_temperature": self.set_temperature,
            "adjust_fan_speed": self.adjust_fan_speed,
            "change_mode": self.change_mode,
        }

    def turn_on(self, parameters: Dict[str, Any]) -> str:
        return f"{self.name} 已开启"

    def turn_off(self, parameters: Dict[str, Any]) -> str:
        return f"{self.name} 已关闭"

    def set_temperature(self, parameters: Dict[str, Any]) -> str:
        temperature = parameters.get("temperature", 24)
        return f"{self.name} 的温度已设置为 {temperature} 度"

    def adjust_fan_speed(self, parameters: Dict[str, Any]) -> str:
        speed = parameters.get("speed_level", "medium")
        return f"{self.name} 的风速已调整到 {speed}"

    def change_mode(self, parameters: Dict[str, Any]) -> str:
        mode = parameters.get("mode", "cooling")
        return f"{self.name} 的模式已切换到 {mode}"


class SmartCurtain(SmartDevice):
    def __init__(self, name: str):
        super().__init__(name)
        self.actions = {
            "open": self.open,
            "close": self.close,
            "adjust_position": self.adjust_position,
        }

    def open(self, parameters: Dict[str, Any]) -> str:
        return f"{self.name} 窗帘已打开"

    def close(self, parameters: Dict[str, Any]) -> str:
        return f"{self.name} 窗帘已关闭"

    def adjust_position(self, parameters: Dict[str, Any]) -> str:
        position = parameters.get("percentage", 100)
        return f"{self.name} 窗帘开合度调整到 {position}%"


# 定义设备实例
light = SmartLight("客厅灯")
air_conditioner = SmartAirConditioner("卧室空调")
curtain = SmartCurtain("厨房窗帘")

function_list = [
    {
        "name": "控制灯光",
        "description": "该函数用于控制家中的灯光，可以实现开灯、关灯、调节亮度或更改灯光颜色。",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "灯光所在的房间或区域，比如客厅、卧室。未说明则为[默认]"
                },
                "action": {
                    "type": "string",
                    "description": "具体操作，比如 'turn_on'（开灯）、'turn_off'（关灯）、'adjust_brightness'（调整亮度）、'change_color'（改变颜色）。"
                },
                "brightness": {
                    "type": "string",
                    "description": "亮度水平，比如 '50%'、'maximum'（仅在调整亮度时需要）。"
                },
                "color": {
                    "type": "string",
                    "description": "灯光颜色，比如 'blue'、'warm white'（仅在改变颜色时需要）。"
                }
            },
            "required": ["location", "action"]
        }
    },
    {
        "name": "控制空调",
        "description": "该函数用于控制空调，可以实现开关、调节温度、风速或切换模式。",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "空调所在的房间，比如客厅、卧室。未说明则为[默认]"
                },
                "action": {
                    "type": "string",
                    "description": "具体操作，比如 'turn_on'（开启）、'turn_off'（关闭）、'set_temperature'（设置温度）、'adjust_fan_speed'（调整风速）、'change_mode'（改变模式）。"
                },
                "temperature": {
                    "type": "number",
                    "description": "目标温度（仅在设置温度时需要）。"
                },
                "fan_speed": {
                    "type": "string",
                    "description": "风速等级，比如 'low'、'medium'、'high'（仅在调整风速时需要）。"
                },
                "mode": {
                    "type": "string",
                    "description": "空调模式，比如 'cooling'、'heating'、'fan_only'（仅在改变模式时需要）。"
                }
            },
            "required": ["location", "action"]
        }
    },
    {
        "name": "控制窗帘",
        "description": "该函数用于控制窗帘的开合，可以实现打开、关闭或调整开合程度。",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "窗帘所在的房间或区域，比如客厅、卧室。未说明则为[默认]"
                },
                "action": {
                    "type": "string",
                    "description": "具体操作，比如 'open'（打开）、'close'（关闭）、'adjust_position'（调整开合程度）。"
                },
                "percentage": {
                    "type": "number",
                    "description": "窗帘开合百分比（仅在调整开合程度时需要），值范围为 0-100。"
                }
            },
            "required": ["location", "action"]
        }
    },
    {
        "name": "查询温湿度",
        "description": "该函数用于查询房间的温度或湿度信息。",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "需要查询温湿度的房间或区域，比如客厅、厨房。未说明则为[默认]"
                },
                "query_type": {
                    "type": "string",
                    "description": "查询类型，比如 'temperature'（温度）或 'humidity'（湿度）。"
                }
            },
            "required": ["location", "query_type"]
        }
    },
    {
        "name": "控制门锁",
        "description": "该函数用于控制智能门锁的开锁或上锁操作。",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "门锁所在的位置，比如前门、后门。未说明则为[默认]"
                },
                "action": {
                    "type": "string",
                    "description": "具体操作，比如 'lock'（上锁）或 'unlock'（开锁）。"
                }
            },
            "required": ["location", "action"]
        }
    },
    {
        "name": "控制音响",
        "description": "该函数用于控制智能音响，可以实现播放、暂停、调节音量等操作。",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "音响所在的房间，比如客厅、卧室。未说明则为[默认]"
                },
                "action": {
                    "type": "string",
                    "description": "具体操作，比如 'play_music'（播放音乐）、'pause'（暂停）、'adjust_volume'（调整音量）。"
                },
                "volume_level": {
                    "type": "string",
                    "description": "音量大小，比如 'low'、'medium'、'high'（仅在调整音量时需要）。"
                },
                "track_name": {
                    "type": "string",
                    "description": "播放的曲目名称（仅在播放音乐时需要）。"
                }
            },
            "required": ["location", "action"]
        }
    }
]
