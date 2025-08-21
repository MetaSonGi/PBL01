import json
import time
import random
import platform
import psutil
from typing import Dict, Any


class DummySensor:
    def __init__(self) -> None:
        self.env_values: Dict[str, Any] = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None
        }

    def set_env(self) -> None:
        self.env_values["mars_base_internal_temperature"] = round(random.uniform(18, 30), 2)
        self.env_values["mars_base_external_temperature"] = round(random.uniform(0, 21), 2)
        self.env_values["mars_base_internal_humidity"] = round(random.uniform(50, 60), 2)
        self.env_values["mars_base_external_illuminance"] = round(random.uniform(500, 715), 2)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 4)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    def get_env(self) -> Dict[str, Any]:
        return dict(self.env_values)


class MissionComputer:
    def __init__(self) -> None:
        self.env_values: Dict[str, Any] = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None,
        }
        self.ds = DummySensor()

    def get_sensor_data(self) -> None:
        while True:
            self.ds.set_env()
            self.env_values.update(self.ds.get_env())
            print(json.dumps(self.env_values, ensure_ascii=False))
            time.sleep(5)

    def get_mission_computer_info(self) -> None:
        """운영체제, 버전, CPU 타입, CPU 코어수, 메모리 크기 정보를 JSON으로 출력"""
        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "cpu_type": platform.processor(),
            "cpu_cores": psutil.cpu_count(logical=True),
            "memory_total_MB": round(psutil.virtual_memory().total / (1024*1024), 2)
        }
        print(json.dumps(info, ensure_ascii=False))

    def get_mission_computer_load(self) -> None:
        """CPU 및 메모리 실시간 사용량 정보를 JSON으로 출력"""
        load = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent
        }
        print(json.dumps(load, ensure_ascii=False))


if __name__ == "__main__":
    runComputer = MissionComputer()
    print("=== Mission Computer Info ===")
    runComputer.get_mission_computer_info()
    print("=== Mission Computer Load ===")
    runComputer.get_mission_computer_load()
    # 센서 데이터 출력은 무한루프라 기본 실행에서는 생략
    # runComputer.get_sensor_data()
