import json
import time
import random
import platform
import psutil
import threading
from multiprocessing import Process
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
    def __init__(self, name: str = "MissionComputer") -> None:
        self.name = name
        self.env_values: Dict[str, Any] = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None,
        }
        self.ds = DummySensor()

    def get_sensor_data(self, interval: int = 5) -> None:
        """5초(기본)마다 센서 값을 수집/출력"""
        while True:
            self.ds.set_env()
            self.env_values.update(self.ds.get_env())
            payload = {
                "source": f"{self.name}.get_sensor_data",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                **self.env_values
            }
            print(json.dumps(payload, ensure_ascii=False))
            time.sleep(interval)

    def get_mission_computer_info(self, interval: int = 20) -> None:
        """20초마다 시스템 정적 정보 출력"""
        while True:
            info = {
                "source": f"{self.name}.get_mission_computer_info",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "os": platform.system(),
                "os_version": platform.version(),
                "cpu_type": platform.processor(),
                "cpu_cores": psutil.cpu_count(logical=True),
                "memory_total_MB": round(psutil.virtual_memory().total / (1024*1024), 2)
            }
            print(json.dumps(info, ensure_ascii=False))
            time.sleep(interval)

    def get_mission_computer_load(self, interval: int = 20) -> None:
        """20초마다 시스템 부하(실시간) 출력"""
        while True:
            load = {
                "source": f"{self.name}.get_mission_computer_load",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent
            }
            print(json.dumps(load, ensure_ascii=False))
            # interval은 psutil.cpu_percent의 내부 1초 대기 포함 이후로 계산
            time.sleep(max(0, interval - 1))


def run_threads() -> None:
    """하나의 MissionComputer 인스턴스에서 3개 메소드를 멀티 스레드로 실행"""
    runComputer = MissionComputer(name="runComputer(Thread)")
    t1 = threading.Thread(target=runComputer.get_mission_computer_info, args=(20,), daemon=True)
    t2 = threading.Thread(target=runComputer.get_mission_computer_load, args=(20,), daemon=True)
    t3 = threading.Thread(target=runComputer.get_sensor_data, args=(5,), daemon=True)
    for t in (t1, t2, t3):
        t.start()
    return (t1, t2, t3)


def proc_info(name: str) -> None:
    mc = MissionComputer(name=name)
    mc.get_mission_computer_info(20)


def proc_load(name: str) -> None:
    mc = MissionComputer(name=name)
    mc.get_mission_computer_load(20)


def proc_sensor(name: str) -> None:
    mc = MissionComputer(name=name)
    mc.get_sensor_data(5)


def run_processes() -> tuple[Process, Process, Process]:
    """3개의 MissionComputer 인스턴스를 멀티 프로세스로 실행"""
    p1 = Process(target=proc_info, args=("runComputer1(Process)",))
    p2 = Process(target=proc_load, args=("runComputer2(Process)",))
    p3 = Process(target=proc_sensor, args=("runComputer3(Process)",))
    for p in (p1, p2, p3):
        p.start()
    return (p1, p2, p3)


if __name__ == "__main__":
    print("[Main] 멀티 스레드 + 멀티 프로세스 실행 시작 (Ctrl+C로 종료)")
    # 1) 스레드 실행
    threads = run_threads()
    # 2) 프로세스 실행
    processes = run_processes()

    try:
        # 스레드는 데몬으로 돌고, 프로세스는 join 대기
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("\n[Main] 종료 신호 감지, 정리 중...")
        for p in processes:
            if p.is_alive():
                p.terminate()
        for p in processes:
            p.join()
        print("[Main] 종료 완료.")
