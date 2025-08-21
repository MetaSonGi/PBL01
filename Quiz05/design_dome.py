import numpy as np
import pandas as pd

def main():
    # 파일 경로
    file1 = r"C:\Users\52649\Documents\GitHub\python_codyseey\Step01\01\PBL01\Quiz05\mars_base_main_parts-001.csv"
    file2 = r"C:\Users\52649\Documents\GitHub\python_codyseey\Step01\01\PBL01\Quiz05\mars_base_main_parts-002.csv"
    file3 = r"C:\Users\52649\Documents\GitHub\python_codyseey\Step01\01\PBL01\Quiz05\mars_base_main_parts-003.csv"


    # CSV 읽기 (숫자 데이터만 추출)
    df1 = pd.read_csv(file1).select_dtypes(include=[np.number])
    df2 = pd.read_csv(file2).select_dtypes(include=[np.number])
    df3 = pd.read_csv(file3).select_dtypes(include=[np.number])

    # ndarray 변환
    arr1 = df1.to_numpy()
    arr2 = df2.to_numpy()
    arr3 = df3.to_numpy()

    # 병합 (merge)
    parts = np.vstack((arr1, arr2, arr3))

    # 열 단위 평균값 계산
    means = np.mean(parts, axis=0)

    # 평균값이 50보다 작은 값만 추출
    below_50 = means[means < 50]

    # CSV로 저장
    pd.DataFrame(below_50, columns=["mean_value"]).to_csv("parts_to_work_on.csv", index=False)

    print("✅ 작업 완료: parts_to_work_on.csv 저장됨")

if __name__ == "__main__":
    main()
