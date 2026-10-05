Q = int(input())
query = list(map(int, input().split()))
_, N, ants_house = query[0], query[1], query[2:]

ants = dict()
# # 여왕 추가
# ants_house.insert(0, 0)
# ants[0] = 0
for i, v in enumerate(ants_house):
    ants[i+1] = v

# 수직선 땅
# 1. 마을 건설
# 여왕 개미 집 x = 0, 개미집은 오름차순

# 2. 개미집 건설
# 새로운 개미집 건설
# 개미집 위치 x=p
# p는 이전까지 개미집의 좌표보다 큰 값으로 주어짐
# 개미집 번호 : N+k
def build_house(ants, ants_house, cnt, p):
    ants_house.append(p)
    ants[cnt] = p

# 3. 개미집 철거
# q번호의 개미집 철거
def delete_house(ants, ants_house, idx):
    val = ants.pop(idx)
    ants_house.remove(val)


# 4. 개미집 정찰
# 모든 개미집 확인
# 개미의 수 r마리가 서로 다른 개미집을 선택하여 확인 -> x값 증가하는 방향으로 1초에 1만큼 이동 -> 여왕개미집은 항상 안전한 개미집
# 처음 개미집이 안전한 개미집이면 이동 중지 : 모든 개미집이 안전한 개미집이면 이동 종료
# 정찰 시간 최소화를 위한 개미집을 선택
# 여왕개미에게 정찰 시간 보고

# 그리디 탐색
def greedy_cover(ants_house, T, r):
    # 몇 마리 개미로 커버할 수 있는지 검사
    count = 0
    # 주어진 T 시간동안 어느 범위까지 커버할 수 있는 검사
    max_cover = -1
    for x in ants_house:
        if x > max_cover:
            # 현재 위치 에서 커버할 수 있는 범위
            max_cover = T + x
            count += 1
    return count <= r

def binary_search(ants_house, r):
    if not ants_house:
        return 0
    ans = 0
    # 좌측 끝 -> 여왕 집도 가능
    left = 0
    # 우측 끝
    right = ants_house[-1] - ants_house[0]
    while left <= right:
        mid = (left + right) // 2
        if greedy_cover(ants_house, mid, r):
            ans = mid
            right = mid - 1
        else:
            left = mid + 1

    return ans

cnt = N + 1

for i in range(Q-1):
    query = list(map(int, input().split()))
    types = query[0]
    if types == 200:
        p = query[1]
        build_house(ants, ants_house, cnt, p)
        cnt += 1
    elif types == 300:
        q = query[1]
        delete_house(ants, ants_house, q)
    elif types == 400:
        r = query[1]
        result = binary_search(ants_house, r)
        print(result)

