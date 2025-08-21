import json
import time
import random
from typing import Dict, Any


class DummySensor:
    """
    테스트용 더미 센서.
    호출할 때마다 지정된 범위 내에서 난수를 생성해 환경 값을 반환한다.
    """
    def __init__(self) -> None:
        self.env_values: Dict[str, Any] = {
            "mars_base_internal_temperature": None,   # 내부 온도 (18~30 °C)
            "mars_base_external_temperature": None,   # 외부 온도 (0~21 °C)
            "mars_base_internal_humidity": None,      # 내부 습도 (50~60 %)
            "mars_base_external_illuminance": None,   # 외부 광량 (500~715 W/m2)
            "mars_base_internal_co2": None,           # 내부 CO2 농도 (0.02~0.1 %)
            "mars_base_internal_oxygen": None         # 내부 산소 농도 (4~7 %)
        }

    def set_env(self) -> None:
        """범위 내 난수로 센서 값을 갱신한다."""
        self.env_values["mars_base_internal_temperature"] = round(random.uniform(18, 30), 2)
        self.env_values["mars_base_external_temperature"] = round(random.uniform(0, 21), 2)
        self.env_values["mars_base_internal_humidity"] = round(random.uniform(50, 60), 2)
        self.env_values["mars_base_external_illuminance"] = round(random.uniform(500, 715), 2)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 4)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    def get_env(self) -> Dict[str, Any]:
        """현재 센서 값을 반환한다."""
        return dict(self.env_values)


class MissionComputer:
    """
    화성 기지 미션 컴퓨터.
    센서로부터 값을 읽어 env_values에 저장하고 5초 주기로 출력한다.
    """
    def __init__(self) -> None:
        self.env_values: Dict[str, Any] = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None,
        }
        # 문제 3의 더미 센서 인스턴스
        self.ds = DummySensor()

    def get_sensor_data(self) -> None:
        """
        1) 센서 값을 읽어 env_values에 저장
        2) env_values를 JSON으로 출력
        3) 위 과정을 5초마다 반복
        """
        while True:
            # 1) 센서 업데이트 및 수집
            self.ds.set_env()
            self.env_values.update(self.ds.get_env())

            # 2) JSON 출력 (한국어 환경에서도 보이도록 ensure_ascii=False)
            print(json.dumps(self.env_values, ensure_ascii=False))

            # 3) 5초 대기
            time.sleep(5)


if __name__ == "__main__":
    # MissionComputer를 RunComputer라는 이름으로 인스턴스화
    RunComputer = MissionComputer()
    try:
        # 지속적으로 환경 값을 출력
        RunComputer.get_sensor_data()
    except KeyboardInterrupt:
        # Ctrl+C로 종료 시 깔끔하게 마무리
        print("\n[MissionComputer] 종료합니다.")
