import heapq
from collections import deque, defaultdict

N, T = map(int, input().split())
# F_ij : (i, j) 학생의 초기 음식
# T : 민트, C : 초코, M : 우유
# B_ij : (i, j) 학생의 신앙심

# 비트 마스킹으로 표현 -> 약한 전파시 1 | 2 = 3, 1|4 = 5
# 3: 민트초코, 5: 민트우유 등 표현이 가능
ch = {
    "T": 1, "C": 2, "M": 4,
    
}
board = []
for _ in range(N):
    tmp = input().strip()
    data = []
    for t in tmp:
        data.append(ch[t])
    board.append(data)

# 산앙심
trusts = []
for _ in range(N):
    data = list(map(int, input().split()))
    trusts.append(data)

dx = [-1,1,0,0]
dy = [0,0,-1,1]

def is_range(x, y):
    return 0 <= x < N and 0 <= y < N

# 1. 아침시간
# 신앙심 1씩 추가
def morning(trusts):
    for x in range(N):
        for y in range(N):
            trusts[x][y] += 1

# 2. 점심시간
# 인접한 4방향 상하좌우에 같은 신봉 음식끼리 그룹 생성
# 그룹 대표는 1. 신앙심 크기 2. 행이 작은 순서 3. 열이 작은 순선
# 그룹 대표는 그룹원수 -1 신앙심 추가, 나머지 그룹원들은 1 신앙심 감소

# 그룹 찾기
def bfs(visited, cx, cy, board, trusts):
    result = []
    q = deque()
    visited[cx][cy] = True
    q.append((cx, cy))
    target = board[cx][cy]
    heapq.heappush(result, (-trusts[cx][cy], cx, cy))
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            # 격자 범위 + 방문한적 X + 같은 그룹 값(같은 신봉 음식)
            if is_range(nx, ny) and not visited[nx][ny] and target == board[nx][ny]:
                q.append((nx, ny))
                visited[nx][ny] = True
                heapq.heappush(result, (-trusts[nx][ny], nx, ny))
    return result

# 대표자 선출
def choice_represent(tmp, trusts, groups):
    if not tmp:
        return None
    _, rep_x, rep_y = heapq.heappop(tmp)
    n = len(tmp)
    # 그룹 대표 선정
    groups[(rep_x, rep_y)]
    # 대표 신앙심 증가(그룹원들 수만큼)
    trusts[rep_x][rep_y] += n
    # 각 그룹 조합원들 신앙심 갑소
    for _,x,y in tmp:
        trusts[x][y] -= 1
        # 그룹 대표에 그룹원들 추가
        groups[(rep_x, rep_y)].append((x, y))
    
# 점심시간
def afternoon(board, trusts, groups):
    visited = [[False] * N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if not visited[x][y]:
                tmp = bfs(visited, x, y, board, trusts)
                choice_represent(tmp, trusts, groups)


# 3. 저녁 시간
# 그룹 대표들이 신앙을 전파
# 1. 단일음식(민트, 초코, 우유) 2. 이중 조합(초코우유, 민트우유, 민트초코) 3.삼중조합(민트초코우유)
# 같은그룹내에서는 전파 기준 : 1. 대표자 신앙심 높은 순 2.행번호 작은 순 3. 열 번호 작은 순서
# 간절함 : 신앙심(B) - 1
# 간절함 % 4의 값으로 방향 선택 : 0(상), 1(하), 2(좌), 3(우)
# 전파자 한칸씩 이동하며 전파, 간절함이 0이되면 전파 종료
# 전파 대상과 전파자의 신봉 음식이 동일시 다음으로 진행

# 전파 대상이 전파자와 음식이 다른 경우(x: 간절함, y: 전파 대상자 신앙심)
# 1. x > y : 강한 전파 성공 -> 전파자의 신봉 음식과 동일해짐, 전파자는 간절함 y+1만큼 감소, 전파 대상의 신앙심은 1 증가
# 2. x <= y : 약한 전파 성공 -> 기존 관심 기본 음식과 전파자 기본 음식을 합친 음식을 신봉, 전파자 간절함 0이 되고, 전파 대상의 신앙심은 x만큼 증가

# 어떤 학생이 다른 음식 대표자에게 전파 당했다면, 해당 학생은 전파 그날 불가, 전파 받는 것은 가능

# 민트초코우유, 민트초코, 민트우유, 초코우유, 우유, 초코, 민트 순서대로 신앙심 총합 출력

# 기본 음식 조합 개수
def extract_food_priory(val):
    n = val
    cnt = 0
    while n > 0:
        if n & 1:
            cnt += 1
        n >>= 1
    return cnt

# 대표자 전파 순서 정렬
def sort_represent(board, trusts, groups):
    # 전파할 대표자들 순서 정렬
    result = []
    for x, y in groups.keys():
        val = board[x][y]
        trust = trusts[x][y]
        n = extract_food_priory(val)
        heapq.heappush(result, (n, -trust, x, y))
    return result

# 전파시키기
def spread(board, trusts, groups):
    # 전파할 대표자 정렬된 리스트
    represents = sort_represent(board, trusts, groups)
    # 전파 당한 대표자는 그 날에 전파 X
    impossible_spread = {k:True for k in groups.keys()}
    while represents:        
        _, trust, x, y = heapq.heappop(represents)
        trust = -trust
        # print("="*20, x,y, "="*20)
        if not impossible_spread[(x,y)]:
            continue
        # 간절함
        earnest = trust - 1
        # 방향 설정
        dirs = trust % 4
        # 신앙심 1로 변경
        trusts[x][y] = 1
        nx, ny = x, y
        while earnest > 0:
            nx, ny = nx + dx[dirs], ny + dy[dirs]
            # 격자 범위 내인지 확인 
            if not is_range(nx, ny):
                break
            oppose = trusts[nx][ny] # 대상자 신앙심
            # 전파와 대상자 음식이 동일시 간절함 소모 X
            if board[x][y] == board[nx][ny]:
                continue
            # print(nx, ny, earnest, oppose)
            # x > y 인경우 : 강한 전파
            if earnest > oppose:
                earnest -= (oppose+1) # 간절함 y+1 만큼 감소
                trusts[nx][ny] += 1 # 대상자 신앙심 증가
                board[nx][ny] = board[x][y] # 전파자와 동일한 음식으로 변경
            # x <= y 인경우 : 약한 전파
            elif earnest <= oppose:
                board[nx][ny] |= board[x][y] # 음식 or 연산으로 추가
                trusts[nx][ny] += earnest # 대상자들 신앙심 x만큼 증가
                earnest = 0 # 간절함 0으로 변경
            if (nx, ny) in impossible_spread.keys():
                impossible_spread[(nx,ny)] = False
        # print(trusts)
        # print(board)

def get_score(board, trusts):
    result = {k:0 for k in range(1,8)}
    # 민트초코우유(7),초코우유(6),민트우유(5),우유(4),초코민트(3),초코(2),민트(1) -> 7,3,5,6,4,2,1
    sort_key = [7,3,5,6,4,2,1]
    for x in range(N):
        for y in range(N):
            result[board[x][y]] += trusts[x][y]
    answer = [result[k] for k in sort_key]
    return answer

for _ in range(T):
    groups = defaultdict(list)
    # print("="*40)
    morning(trusts)
    # print("morning: ", trusts)
    # print("morning: ", board)
    afternoon(board, trusts, groups)
    # print("오후 : ", trusts)
    # print("오후: ", board)
    # print("오후 대표 : ", groups)
    spread(board, trusts, groups)
    answer = get_score(board, trusts)
    # print("저녁 : ", trusts)
    # print("저녁 : ", board)
    print(*answer)
