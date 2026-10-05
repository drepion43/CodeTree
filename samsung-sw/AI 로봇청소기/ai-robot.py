from collections import deque
import copy

N, K, L = map(int, input().split())

board = []
dusts = []
obstacles = []
no_dusts = []
for x in range(N):
    # -1은 물건 위치
    data = list(map(int, input().split()))
    board.append(data)
    for y, d in enumerate(data):
        if d > 0:
            dusts.append((x, y))
        elif d == -1:
            obstacles.append((x, y))
        elif d == 0:
            no_dusts.append((x, y))

robot = []
for _ in range(K):
    x, y = map(int, input().split())
    robot.append((x-1, y-1))
    
# print(board)
# print(robot)
# print(dusts)

# 로봇 청소기
# 1. 먼지O 2. 먼지X 3. 물건
# 먼지 값 1 ~ 100, 로봇 청소기 초기 위치는 먼지 X

# 1. 청소기 이동
# 순서대로 이동 거리가 가장 가까운 오염된 격자로 이동
# 물건/청소기 위치는 통과 X
# 이동거리 상하좌우, 행/열 작은 격자 우선순위
dx1 = [-1,0,0,1]
dy1 = [0,-1,1,0]
def is_range(x, y):
    return 0 <= x < N and 0 <= y < N

# 현재 로봇 위치에서 먼지가 있는 곳 최단 거리 위치 파악
def is_bfs(cx, cy, other_robots):
    # 만약 현재 위치에 이미 먼지가 있다면 이동하지 않고 제자리 유지
    if board[cx][cy] > 0:
        return cx, cy
    visited = [[False] * N for _ in range(N)]
    q = deque()
    # 좌표, 거리
    q.append((cx, cy, 0))
    visited[cx][cy] = True
    
    candidates = []
    min_dist = float('inf')
    while q:
        x, y, dist = q.popleft()
        # 이미 찾은 최단 거리보다 멀어지면 탐색 중단
        if dist > min_dist:
            break
        # 처음 위치와 다르며 먼지가 있는 곳을 가장 먼저 만난다면
        if board[x][y] > 0 and (x, y) != (cx, cy):
            candidates.append((x, y))
            min_dist = dist
            continue
        for i in range(4):
            nx, ny = x + dx1[i], y + dy1[i]
            if is_range(nx, ny) and board[nx][ny] >= 0 and not visited[nx][ny]:
                if (nx, ny) not in other_robots:
                    visited[nx][ny] = True
                    q.append((nx, ny, dist + 1))
                    
    # 최단 거리 후보가 있다면 (행 번호 작은 순 -> 열 번호 작은 순) 정렬 후 선택
    if candidates:
        candidates.sort(key=lambda x: (x[0], x[1]))
        return candidates[0]
    # 갈 수 있는 곳이 없으면 제자리
    return cx, cy

def move(idx, robot):
    cx, cy = robot[idx]
    # 본인 제외 로봇들
    other_robots = {(r[0], r[1]) for i, r in enumerate(robot) if i != idx}
    x, y = is_bfs(cx, cy, other_robots)
    # 로봇 이동
    robot[idx] = (x, y)


# 2. 청소
# 청소는 본인 위치, 좌/상/우 청소 가능
# 먼지량이 가장 큰 방향에서 청소 시작
# 최대 청소 먼지량 : 20
# 합이 같은 방향이 여러개라면, 우하좌상 순
# 청소기마다 순서대로

# 우 하 좌 상 : 우선순위
clean_pattern = {
    0:[(0, 0), (-1, 0), (1, 0), (0, 1)], # ㅏ,
    1:[(0, 0), (0, 1), (0, -1), (1, 0)], # ㅜ
    2:[(0, 0), (0, -1), (1, 0), (-1, 0)], # ㅓ
    3:[(0, 0), (-1, 0), (0, -1), (0, 1)], # ㅗ
}
def cleaning(idx, board):
    cx, cy = robot[idx]
    max_dust = -1
    dirs = -1
    # ㅏ, ㅜ, ㅓ, ㅗ 방향 탐색
    for i in range(4):
        dust_total = 0
        for dx, dy in clean_pattern[i]:
            nx, ny = cx + dx, cy + dy
            if is_range(nx, ny) and board[nx][ny] > 0:
                # 격자 마다 청소할 수 있는 최대 먼지량
                dust_total += min(20, board[nx][ny])
        
        # dust 최대 값 찾기 : 어느 방향을 청소할지 선택
        if dust_total > max_dust:
            max_dust = dust_total
            dirs = i

    if dirs != -1:
        # 선택 후 실제 청소 시작
        for dx, dy in clean_pattern[dirs]:
            nx, ny = cx + dx, cy + dy
            if is_range(nx, ny) and board[nx][ny] > 0:
                board[nx][ny] -= min(20, board[nx][ny])

# 3. 먼지 축적
# 먼지 있는 칸에 5씩 증가
def stack_dust(board):
    for x in range(N):
        for y in range(N):
            if board[x][y] > 0:
                board[x][y] += 5

# 4. 먼지 확산
# 깨끗한 격자 주변 4방향 격자의 먼지량 합 / 10만큼 먼지 확산
# 소숫점 아래 버림
# 동시에 확산
def spread_dust(board):
    # 장애물만 추가한 새로운 판때기 생성
    new_board = [[0]* N for _ in range(N)]

    for x in range(N):
        for y in range(N):
            if board[x][y] == 0:
                count = 0
                for i in range(4):
                    nx, ny = x + dx1[i], y + dy1[i]
                    if is_range(nx, ny) and board[nx][ny] > 0:
                        count += board[nx][ny]
                spread_val = count // 10
                new_board[x][y] = spread_val

    for x in range(N):
        for y in range(N):
            if new_board[x][y] > 0:
                board[x][y] += new_board[x][y]



# 5. 출력
# 전체 공간 총 먼지량 출력
# 먼지가 모두없다면 0 출력
def print_dust(board):
    return sum(val for row in board for val in row if val > 0)


for _ in range(L):
    # 1. 로봇 이동
    for i in range(K):
        move(i, robot)

    for i in range(K):
        # 2. 청소 시작
        cleaning(i, board)
    
    # 3. 먼지 축적
    stack_dust(board)
    
    # 4. 먼지 확산
    spread_dust(board)
    
    # 5. 출력
    # print(board)
    result = print_dust(board)
    print(result)
