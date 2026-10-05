from collections import deque
N, r, c, d = map(int, input().split())

r -= 1
c -= 1
d -= 1

# 입력 방향을 내부 표현으로 변환합니다.
# 입력(0-indexed): 0=상, 1=하, 2=좌, 3=우
# 내부(반시계):    0=상, 1=좌, 2=하, 3=우
dir_map = [0, 2, 1, 3]
d = dir_map[d]

# 이동 순서 : 상좌하우
dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]

## 1단계
# 1. 현재 방향 직진, 2.좌회줜, 3.우회줜, 4. 180도 회전

## 2단계
# 인접한칸이 모두 방문이라면, 가장 가까운 칸을 찾아 이동
# 1. 최소 이동횟수(상하좌우순), 암초는 패스X
# 2. 행번호, 열번호 작은 순
# 3. 좌하우상 순으로 선택
visited = [[False] * N for _ in range(N)]
board = []
for _ in range(N):
    board.append(list(map(int, input().split())))

def is_range(r, c):
    if 0 <= r < N and 0 <= c < N:
        return True
    else:
        return False

# 1단계 이동
def move1(r, c, d):
    # 현재 방향 직진, 좌회전, 우회전, 180도 회전
    for dir in [0, 1, -1, 2]:
        nd = (d + dir + 4) % 4
        nr, nc = r + dx[nd], c + dy[nd]
        if is_range(nr, nc) and board[nr][nc] == 0 and not visited[nr][nc]:
            return nr, nc, nd
    # 이동이 불가한 경우
    return -1, -1, -1

# 2단계 : 최단거리
def bfs(r, c):
    # 최단 거리
    dist = [[-1] * N for _ in range(N)]
    dist[r][c] = 0
    q = deque()
    q.append([r, c])
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx, ny = x+dx[i], y+dy[i]
            if is_range(nx, ny) and board[nx][ny] == 0 and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                q.append([nx, ny])
    # 못가는 곳은 -1
    return dist
            

# 전체 바다 크기
total = sum(board[i][j] == 0 for i in range(N) for j in range(N))
print(r+1, c+1)


def simulation(r, c, d):
    # 이동
    visited[r][c] = True
    cnt = 1

    # 어항 채우기
    while cnt < total:

        # 1단계 이동
        while True:
            nr, nc, nd = move1(r, c, d)
            # 1단계 불가한 경우
            if nr == -1:
                break
            visited[nr][nc] = True
            r, c, d = nr, nc, nd
            cnt += 1
            print(r+1,c+1)

        
        # 갈 수 있는 곳 모두 갔을 때
        if cnt >= total:
            break

        # 2단계 : 1단계가 불가한 현재 위치에서 가장 짧은 거리로 이동 -> 이동할 좌표 선택
        dist = bfs(r, c)
        min_x, min_y, min_dist = -1, -1, float('inf')
        for x in range(N):
            for y in range(N):
                # 암초 or 방문했던 적 or 갈 수 없는 곳일 경우 -> 검사 통과
                if board[x][y] != 0 or visited[x][y] or dist[x][y] == -1:
                    continue
                if dist[x][y] < min_dist or (dist[x][y] == min_dist and (x, y) < (min_x, min_y)):
                    min_x, min_y, min_dist = x, y, dist[x][y]
        # 2단계 : 이동할 목표 지점에서 현재 위치까지의 최소 거리로 이동(이동시 거리1씩 줄어드는 방향이며 좌하우상 순서로 선택)
        dist2 = bfs(min_x, min_y)
        # 2단계 이동
        while min_x != r or min_y != c:
            # 좌하우상
            for i in [1,2,3,0]:
                nx, ny = r + dx[i], c + dy[i]
                # 거리가 1줄어드는 방향으로 이동해야함
                if is_range(nx, ny) and board[nx][ny] == 0 and dist2[nx][ny] == dist2[r][c] - 1:
                    r, c, d = nx, ny, i
                    break
        # 2단계로 이동 후 방문 처리
        visited[r][c] = True
        cnt += 1
        print(r+1,c+1)
        
        
simulation(r, c, d)
