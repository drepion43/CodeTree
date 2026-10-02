from bisect import bisect_left, bisect_right
from collections import deque
Q = int(input())
query = list(map(int, input().split()))
_, _, mountains = query[0], query[1], query[2:]

# 1.등산가 이동
# 우측으로 이동
# 현재 산보다 더 높은 산으로만 이동

# 2. 케이블카
# 특정 산에서만 탑승
# 현재 위치포함 임의의 산으로 이동(높낮이 X)
# 케이블카 탄 후 등산가 이동 이어짐

# 3. 등산 시뮬레이션
# 1. 시작 산 선택
# 2. 오른쪽 위치한 산으로 이동 성공 : 100만점 획득
# 3. 케이블카 이용시 : 100만점 획득
# 4. 케이블카 이용 후 다시 등산 성공 : 100만점 획득
# 5. 위치한 산의 높이만큼 점수 획득

mountain_buckets = []
depth_history = []
# 우공이산 : 우측끝에 산 추가
# LIS에 필요한 산들 추가
# 예시 시뮬레이션
# 5 3 6 8 4 9 2 이 입력이 들어왔을 때
# step1 : height=5, tails = [], idx = 0, mountain_buckets=[[5]], depth_history=[0]
# step2 : height=3, tails = [5], idx = 0, mountain_buckets=[[5, 3]], depth_history=[0, 0]
# step3 : height=6, tails = [3], idx = 1, mountain_buckets=[[5, 3], [6]], depth_history=[0, 0, 1]
# step4 : height=8, tails = [3, 6], idx = 2, mountain_buckets=[[5, 3], [6], [8]], depth_history=[0, 0, 1, 2]
# step5 : height=4, tails = [3, 6, 8], idx = 1, mountain_buckets=[[5, 3], [6, 4], [8]], depth_history=[0, 0, 1, 2, 1]
# step6 : height=9, tails = [3, 4, 8], idx = 3, mountain_buckets=[[5, 3], [6, 4], [8], [9]], depth_history=[0, 0, 1, 2, 1, 3]
# step7 : height=2, tails = [3, 4, 8, 9], idx = 0, mountain_buckets=[[5, 3, 2], [6, 4], [8], [9]], depth_history=[0, 0, 1, 2, 1, 3, 0]
def add_mountain(mountain_buckets, depth_history, height):
    bucket = [data[-1] for data in mountain_buckets]
    idx = bisect_left(bucket, height)
    depth_history.append(idx)
    if len(mountain_buckets) <= idx:
        mountain_buckets.append([])
    mountain_buckets[idx].append(height)

# 지진 : 가장 우측 산 제거
def delete_mountain(mountain_buckets, depth_history):
    # 가장 우측 삭제
    idx = depth_history.pop()
    mountain_buckets[idx].pop()
    if len(mountain_buckets[idx]) == 0:
        mountain_buckets.pop()

# 등산 시뮬레이션
# LIS -> 산 리스트, 케이블카 위치
def climbing(mountain_buckets, depth_history, cidx):
    # mountain_buckets에서의 케이블카 위치 : 케이블카 산까지 등산
    idx = depth_history[cidx]
    # 케이블까 산까지 등산 + 케이블카 탑승
    score = (idx + 1) * 1_000_000
    # 케이블카를 타고 다시 처음으로 와서 등산 시작
    score += (len(mountain_buckets) - 1) * 1_000_000
    # 가장 높은 산
    max_height = mountain_buckets[-1][0]
    score += max_height
    return score

# 산 추가(초기화)
for m in mountains:
    add_mountain(mountain_buckets, depth_history, m)

for _ in range(Q-1):
    query = list(map(int, input().split()))
    types = query[0]
    if types == 200:
        val = query[1]
        add_mountain(mountain_buckets, depth_history, val)
    elif types == 300:
        delete_mountain(mountain_buckets, depth_history)
    elif types == 400:
        val = query[1]
        score = climbing(mountain_buckets, depth_history, val-1)
        print(score)