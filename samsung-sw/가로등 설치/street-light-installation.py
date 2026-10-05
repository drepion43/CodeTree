import math
import heapq
# 시간 초과

Q = int(input())
query = list(map(int, input().split()))

# 1. 마을 상태 확인
# N : 거리 크기, M : 초기 가로등 개수
# L_1,L_2... : 초기 가로등 위치, 오름차순
N, M, val_tmp = query[1], query[2], query[3:]
lights = []
# 가로등 번호 관리
locations = []
# 현재 가로등의 좌 우 가로등 위치 파악
left_neighbor = dict()
right_neighbor = dict()
for i, v in enumerate(val_tmp):
    lights.append(v)
    # 가장 왼쪽이면 None, 그게 아니라면 왼쪽 꺼
    left_neighbor[v] = val_tmp[i-1] if i > 0 else None
    # 가장 우측이면 None, 그게 아니라면 우측 꺼
    right_neighbor[v] = val_tmp[i+1] if i < len(val_tmp) - 1 else None

for i in range(1, len(val_tmp)):
    # [간격, 왼쪽, 우측]
    heapq.heappush(locations, (-(val_tmp[i] - val_tmp[i-1]), val_tmp[i-1], val_tmp[i]))

left_head, right_tail = val_tmp[0], val_tmp[-1]

# 2. 가로등 추가

# 가로등 꺼내기 : 가장 넓은 가운데에 설치를 위해
def find_light():
    while locations:
        # 가장 거리가 먼 것부터 확인
        dist, left, right = locations[0]
        # 우측 이웃과 좌측 이웃이 모두 동일하다면 가운데에 설치를 위해 추출
        if right_neighbor.get(left) == right and left_neighbor.get(right) == left:
            return heapq.heappop(locations)
        # 다르다면 다시 찾기
        heapq.heappop(locations)
    return None
    

# 추가 가로등
# 인접 가로등 사이 거리가 가장 먼 곳에 새로운 가로등 설치
# 여러개일시, 좌표 값이 작은 가로등 선택
# 인접 거리 : ceil(L_i + L_j / 2)
def add_light(locations):
    center = find_light()
    if not center:
        return
    dist, left, right = center
    mid = math.ceil((left + right) / 2)
    
    # 이웃에 새로운 거 추가
    left_neighbor[mid] = left
    right_neighbor[mid] = right
    left_neighbor[right] = mid
    right_neighbor[left] = mid

    heapq.heappush(locations, (-(mid - left), left, mid))
    heapq.heappush(locations, (-(right - mid), mid, right))
    lights.append(mid)


# 3. 가로등 제거
# D번 가로등 제거
def del_light(idx, locations, lights):
    global left_head, right_tail
    light = lights[idx-1]
    if light == 0:
        return
    lights[idx-1] = 0
    
    # 삭제할것의 이웃들
    left = left_neighbor[light]
    right = right_neighbor[light]
    
    # 이웃 연결 고리 삭제
    if left is not None:
        right_neighbor[left] = right
    else:
        left_head = right
    if right is not None:
        left_neighbor[right] = left
    else:
        right_tail =  left
        
    # 이웃 자료구조에서 삭제
    right_neighbor.pop(light, None)
    left_neighbor.pop(light, None)
    
    # 추가 삭제된 후 수정하여 재 추가
    if left is not None and right is not None:
        heapq.heappush(locations, (-(right - left), left, right))


# 4. 최소 전력 계산
def min_power(locations):
    # 남아있는 가로등
    left_light = left_head - 1
    right_light = N - right_tail
    # active_lights = [pos for pos in lights if pos != 0]
    # # 가장 좌측 가로등
    # left_light = min(active_lights)
    # # 가장 우측 가로등
    # right_light = max(active_lights)
    # 가운데 있는 가로등 중 제일 큰 것
    mid_req = 0
    # 힙에서 현재 유효한 가장 큰 구간 찾기
    while locations:
        neg_dist, left, right = locations[0]
        if right_neighbor.get(left) == right and left_neighbor.get(right) == left:
            mid_req = (-neg_dist) / 2
            break
        heapq.heappop(locations)  # 무효한 구간 정리
    # print("mid", left_light - 1, N - right_light, mid_req)
    return max(left_light, right_light, mid_req)

# 1,N 전부 밝히기 위한 최소 소비 전력 r 계산
count = M
for _ in range(Q - 1):
    q = list(map(int, input().split()))
    types = q[0]
    # 가로등 추가
    if types == 200:
        add_light(locations)
        count += 1
    elif types == 300:
        del_light(q[1], locations, lights)
    elif types == 400:
        result = min_power(locations)
        print(int(result * 2))
    # print("left neighbor : ", left_neighbor)
    # print("right neighbor : ", right_neighbor)
    # print("light : ", lights)
    # print("locate : ", locations)

