from collections import deque

N, M, K = map(int, input().split())
board = []
for _ in range(N):
    board.append(list(map(int, input().split())))

turtles = []
for i in range(1, M+1):
    val = list(map(int, input().split()))
    turtles.append(val)
    
volcano = []
temperature_board = [[0] * N for _ in range(N)]
volcano_values = []
for _ in range(K):
    # 좌표 + 임계치 + 분출여부
    data = list(map(int, input().split())) + [0]
    volcano.append(data)
    volcano_values.append([data[0], data[1], 0])



dead_turtles = []

# 1. 바다거북의 이동
# ID가 작은 순서대로 이동 -> 안식처까지의 최단 경로 탐색
# 방해요소 : 산호초, 바다거북, 화석 -> 장애물
# 이동 규치 : 우하좌상 -> 우선순위, 최단 거리가 없으면 제자리에 대기
# 안식처 도착 : (N-1,N-1) 도착시 지도에서 제외, 해당 턴 도착시간
# 거북이는 해저 화산있는 칸으로 진입 가능

dx = [0,1,0,-1]
dy = [1,0,-1,0]

def is_range(x, y):
    return 0<= x < N and 0 <= y < N

def is_bfs(cx, cy, other_turtles, dead_set):
    # 안식처에 도착시
    if cx == N-1 and cy == N-1:
        return 0
    visited = [[False] * N for _ in range(N)]
    q = deque()
    # 위치와 이동 거리
    q.append([cx, cy, 0])
    visited[cx][cy] = True
    while q:
        x, y, d = q.popleft()
        if x == N-1 and y == N-1:
            return d
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            # 보드판 내부 + 산호초 X
            if is_range(nx, ny) and board[nx][ny] == 0 and not visited[nx][ny]:
                # 다른 거북 X + 죽은 거북 X 
                if (nx, ny) not in other_turtles and (nx, ny) not in dead_set:
                    q.append([nx, ny, d+1])
                    visited[nx][ny] = True
    # 갈 곳이 없을 시
    return float('inf')

def move(idx):
    cx, cy = turtles[idx]
    # 이미 도착했거나 죽은 경우
    if cx == -1 and cy == -1:
        return None
    # 본인 제외 + 죽은 거북이 제외
    other_turtles = {(t[0], t[1]) for i, t in enumerate(turtles) if i != idx and t[0] != -1}
    # 죽은 거북이
    dead_set = {(d[0], d[1]) for d in dead_turtles}
    
    min_dist = float('inf')
    next_pos = (-1, -1)
    # 우 하 좌 상
    for i in range(4):
        nx, ny = cx + dx[i], cy + dy[i]
        # 보드판 내부 + 산호초 X
        if is_range(nx, ny) and board[nx][ny] == 0:
            # 다른 거북 X + 죽은 거북 X 
            if (nx, ny) not in other_turtles and (nx, ny) not in dead_set:
                dist = is_bfs(nx, ny, other_turtles, dead_set)
                
                # 우 하 좌 상 순서로 최단 거리 확인
                if dist < min_dist:
                    min_dist = dist
                    next_pos = (nx, ny)
    if min_dist == float('inf'):
        return None
        
    return next_pos


# 2. 화산 압력 증가
# 모든 해저 화산은 10씩 압력 증가
def charge_volcano(volcano_values):
    for i in range(len(volcano_values)):
        volcano_values[i][2] += 10


# 3. 화산 분출 및 연쇄 반응
# 분출 임게치 P이상인 화산은 열기 분출
# 열기 전파 : P만큼 열기가 발생, 열기는 4방향으로 확산, 이전시 열기/2 로 감소
# 산호초 + 열기가 0일시 확산 중단
# 한칸에 여러 화산 열기가 모일시 그 값 합산

# 연쇄 반응
# 마그마 입력 + 외부 열기 >= P 되면 해당 화산도 분출
# 외부 열기는 분출 조건에만 가담
# 연쇄 분출은 없을때까지 반복

# 바다거북의 위기(화석화)
# 거북이 위치한 칸의 열기 합이 20이상이면 화석으로 변환
# 화석 거북이는 그자리에 고정 + 장애물로 변경

# 열기 전파
def spread_volcano(idx):
    x, y, p, _ = volcano[idx]
    # 본인 칸에 열기 전달
    temperature_board[x][y] += p
    for i in range(4):
        cx, cy = x, y
        current_heat = p
        # 우선 한쪽 방향으로 쭉 확산
        while True:
            current_heat //= 2
            # 열기가 0이면 확산 중단 or 산호초 만날시
            if current_heat <= 0:
                break
            nx, ny = cx + dx[i], cy + dy[i]
            if  not is_range(nx, ny) or board[nx][ny] == 1:
                break
            temperature_board[nx][ny] += current_heat
            cx, cy = nx, ny

# 연쇄 반응
def chain_react():
    q = deque()
    for i in range(len(volcano)):
        x, y, p, is_erupt = volcano[i]
        cur_p = volcano_values[i][2]
        # 분출할적이 없고 임계치 초과시(외부 열기 포함)
        if not is_erupt and (temperature_board[x][y] + cur_p) >= p:
            # 분출 처리
            volcano[i][3] = 1
            q.append(i)
    # 분출한 화산들에 대해
    while q:
        idx = q.popleft()

        # 열기 방출
        spread_volcano(idx)
        
        # 열기 퍼진 후 새로운 분출 가능한 화산 찾기
        for v in range(len(volcano)):
            if volcano[v][3] == 0:
                vx, vy, vp, _ = volcano[v]
                cur_pp = volcano_values[v][2]
                # 열기 + 마그마 압력 > P 화산 분출
                if cur_pp + temperature_board[vx][vy] >= vp:
                    volcano[v][3] = 1
                    q.append(v)

# 거북이 화석 만들기
def turtle_kill():
    for i in range(M):
        tx, ty = turtles[i]
        # 탈출했거나 이미 죽은 거북이는 pass
        if tx == -1 or ty == -1:
            continue
        if temperature_board[tx][ty] >= 20:
            dead_turtles.append((tx, ty))
            turtles[i] = [-1,-1]

# 4. 환경 초기화
# 바다 위의 모든 열기 정보 제거
# 이번 턴에 분출을 일으킨 모든 화산의 마그마 입력은 0으로 초기화, 분출하지 않은 화산의 압력은 유지

def reset_env():
    global temperature_board
    temperature_board = [[0] * N for _ in range(N)]
    for i in range(K):
        if volcano[i][3] == 1:
            volcano_values[i][2] = 0
            volcano[i][3] = 0

answer = [-1] * M
# 시뮬레이션
for t in range(100):
    # print("="*20, t, "="*20)
    # 1. 거북이 이동
    for i in range(M):
        # 죽은 거북이는 이동 pass
        if turtles[i][0] == -1 and turtles[i][1] == -1:
            continue
        next_pos = move(i)
        if next_pos is not None:
            turtles[i] = [next_pos[0], next_pos[1]]
            # 안식처 도착시 즉시 퇴장
            if turtles[i][0] == N-1 and turtles[i][1] == N-1:
                answer[i] = t + 1
                turtles[i] = [-1, -1]
    # print("거북이: ", turtles)
    # 2. 마그마 추가
    charge_volcano(volcano_values)

    # 3. 마그마 분출
    chain_react()
    turtle_kill()
    # print("마그마: ", volcano)
    # print("마그마 값: ", volcano_values)
    # print("열기: ", temperature_board)

    # 4. 환경 초기화
    reset_env()

for ans in answer:
    print(ans)
