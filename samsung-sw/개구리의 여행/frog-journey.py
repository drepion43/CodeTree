import heapq

N = int(input())
# 0: 안전한 돌, 1: 미끄러운 돌, 2: 천적 돌
ch ={'.':0, 'S':1, '#':2}

board = []
for _ in range(N):
    tmp = input().strip()
    data = []
    for t in tmp:
        data.append(ch[t])
    board.append(data)
# print(board)

dx = [1,-1,0,0]
dy = [0,0,1,-1]
INF = float('inf')

# (1,1): 좌측 상단, (N,N) : 우측 하단
# 돌 종류 : 안전한 돌(.), 미끄러운 돌(S), 천적이 사는 돌(#)
# 개구리의 점프력: 1

# 1. 점프
# 점프력 k :  (x-k,y),(x+k,y), (x,y-k), (x,y+k) 이동
# 이동하려는 위치에 돌이 없거나, 미끄러운 돌은 이동 X, 점프해서 지나치는 위치에 천적이 사는 돌이라면 이동 X
# 점프시 1만큼 시간 소요

# 2. 점프력
# 점프력 1 증가
# 점프력이 1,2,3,4인 경우에만 가능, 최대 점플력은 5
# 점프력 증가 후 점프력 k일시, k^2 만큼 시간 소요

# 3. 점프력 감소
# 기존 점프력 k일시, 1,2,3,k-1 중 점프력을 갖음
# 1만큼 시간 소요

# 경로마다 가중치가 다르니 BFS X

def is_range(x, y):
    return 0 <= x < N and 0 <= y < N

# 최단 경로 탐색
def dijkstra(board, x1, y1, x2, y2):
    # 거리 : (x,y,k) -> dist[k][x][y]
    dist = [[[INF] * N for _ in range(N)] for _ in range(6)]
    
    q = []
    # (시간, 좌표, 점프력)
    heapq.heappush(q, (0, x1, y1, 1))
    dist[1][x1][y1] = 0
    while q:
        t, x, y, k = heapq.heappop(q)
        # print(t, x, y, k)
        
        # 현재 상태가 이미 처리된것보다 작다면 skip
        if dist[k][x][y] < t:
            continue
        
        # 목적지 도착
        if (x, y) == (x2, y2):
            return t
        
        # 4방향 확인
        for i in range(4):
            nx, ny = x + dx[i]*k, y+dy[i]*k
            if not is_range(nx, ny):
                continue
            # 착지 지점은 "안전한 돌"
            if board[nx][ny] == 0:
                # 해당 경로로 이동시 "천적 돌"을 지나치는지 확인
                enemy = False
                for s in range(1, k+1):
                    if board[x + dx[i]*s][y + dy[i]*s] == 2:
                        enemy = True
                        break
                # 천적이 없다면 해당 경로로 이동
                if not enemy:
                    cost = t + 1
                    if cost < dist[k][nx][ny]:
                        dist[k][nx][ny] = cost
                        heapq.heappush(q, (cost, nx, ny, k))
        
        # 2. 점프력 증가도 수행
        if k < 5:
            # 점프력 1 상승
            upgrade_k = k + 1
            # 시간은 제곱으로 늘어남
            cost = t + (upgrade_k ** 2)
            # 현재 지점 보다 작다면 이동
            if cost < dist[upgrade_k][x][y]:
                dist[upgrade_k][x][y] = cost
                heapq.heappush(q, (cost, x, y, upgrade_k))
            
        # 3. 점프력 감소도 수행
        for i in range(1, k):
            cost = t + 1
            if cost < dist[i][x][y]:
                dist[i][x][y] = cost
                heapq.heappush(q, (cost, x, y, i))
    # print(dist)
    return -1

Q = int(input())
frogs = []
# 개구리 여행 정보
for _ in range(Q):
    # 개구리 점프력
    
    x1, y1, x2, y2 = map(int, input().split())
    # 출발점, 목적지
    result = dijkstra(board, x1-1, y1-1, x2-1, y2-1)
    print(result)
