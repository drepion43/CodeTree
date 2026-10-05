# 시간초과로 인한 heapq로 변경
import heapq
T = int(input())

query = list(map(int, input().split()))

_, N = query.pop(0), query.pop(0)
reload_boats = {}
boats_wait = {}
# 사격 대기
wait_attack = []

for i in range(N):
    idx, p, r = query[i*3:(i+1)*3]
    boats_wait[idx] = [True, p, r]
    heapq.heappush(wait_attack, (-p, idx))


# print(boats_wait)
# 1. 공격 준비
# N척의 선박에 사격 준비
# 초기 상태는 모두 사격 대기
# 번호: i, 공격력: p, 재장전 시간: r

# 2. 지원 요청
# 추가 병력 요청
# 새로 합류한 선박도 사격대기 상태
def add_boat(boats_wait, wait_attack, idx, p, r):
    boats_wait[idx] = [True, p, r]
    # 상위 5개 추출을 위한 사격 대기 힙에 추가
    heapq.heappush(wait_attack, (-p, idx))

# 3. 함포 교체
# i번 선박의 함포를 교체
# 교체후 선박의 공격력 pw
def change_boat(boats_wait, wait_attack, idx, pw):
    is_possible, p, r = boats_wait[idx]
    boats_wait[idx] = [is_possible, pw, r]
    if is_possible:
        heapq.heappush(wait_attack, (-pw, idx))

# 4. 공격 명령
# 사격 대기 상태 선박 중 공격력이 가장 높은 선박 최대 5척에 사격 명령 -> 공격력이 같다면 i번이 작은 값 우선순위 -> 총 피해가 최대가 되도록 선박 선택
# 대형 함선에 공격력 합만큼 피해
# r시간 이후 다시 사격 대기 상태
def attack(boats_wait, reload_boats, wait_attack):
    attack_list = []
    damage = 0
    # 사격 대기 힙에서 상위 5개 추출
    while wait_attack and len(attack_list) < 5:
        neg_p, idx = heapq.heappop(wait_attack)
        
        # 현재 사격 대기 상태 + 변경된 공격력이 아닌지 검사
        if boats_wait[idx][0] and boats_wait[idx][1] == -neg_p:
            p, r = boats_wait[idx][1], boats_wait[idx][2]
            # 사격하니 상태 변경
            boats_wait[idx][0] = False
            damage += p
            reload_boats[idx] = r
            attack_list.append(idx)
    return damage, attack_list

# 재장전
def reload_time(reload_boats, boats_wait, wait_attack):
    delete_boats = []
    if len(reload_boats) > 0:
        # 재장전 시간 감소
        for k, v in reload_boats.items():
            if v > 0:
                reload_boats[k] -= 1
            # 만약 재장전 시간이 다 됬다면, 다시 사격 대기 상태로도 변경
            if reload_boats[k] == 0:
                delete_boats.append(k)
                boats_wait[k][0] = True
                # 사격이 가능하니 힙에 다시 추가
                heapq.heappush(wait_attack, (-boats_wait[k][1], k))
    for i in delete_boats:
        reload_boats.pop(i)

# 1시간 단위로 수행
for _ in range(T-1):
    data = list(map(int, input().split()))
    types = data[0]
    if types == 200:
        i, p, r = data[1], data[2], data[3]
        add_boat(boats_wait, wait_attack, i, p, r)
    elif types == 300:
        i, pw = data[1], data[2]
        change_boat(boats_wait, wait_attack, i, pw)
    elif types == 400:
        damage, boats = attack(boats_wait, reload_boats, wait_attack)
        print(damage, len(boats), *boats)
    reload_time(reload_boats, boats_wait, wait_attack)


