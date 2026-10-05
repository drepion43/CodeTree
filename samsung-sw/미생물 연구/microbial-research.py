from collections import deque, defaultdict
N ,Q = map(int, input().split())

board = [[0] * N for _ in range(N)]

# 좌측 하단 : (0, 0), 우측 상단 : (N,N)

# 1. 미생물 투입
# (r1, c1) ~ (rN, cN) 직사각형 영역 미생물 투입
# 새로 투입된 미생물이 기존 미생물 먹음
# 기존 미생물이 먹히면서 영역이 분리될 경우 기존 미생물은 사라짐

# 미생물 개수 세기 + 영역 분리도 확인
def calc_count(board):
    micro_organisms_count = defaultdict()
    for x in range(N):
        for y in range(N):
            val = board[x][y]
            if val > 0:
                if val not in micro_organisms_count:
                    micro_organisms_count[val] = 1
                else:
                    micro_organisms_count[val] += 1
    return micro_organisms_count

dx = [1,-1,0,0]
dy = [0,0,1,-1]
def is_range(x, y):
    return 0 <= x < N and 0 <= y < N

def bfs(board, visited, target, idx, cx, cy):
    
    visited[cx][cy] = True
    q = deque()
    q.append((cx, cy))
    count = 1
    
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if is_range(nx, ny) and not visited[nx][ny] and board[nx][ny] == idx:
                q.append((nx, ny))
                visited[nx][ny] = True
                count += 1
    # print("idx : ", idx, count,  target)

    # 영역이 동일하다면 분리 X, 다르다면 분리
    return count == target

def check_region(board, micro_organisms_count):
    visited = [[False] * N for _ in range(N)]
    delete_organ = set()
    for x in range(N):
        for y in range(N):
            val = board[x][y]
            if val > 0:
                count = micro_organisms_count[val]
                # 사라져야 함
                if not visited[x][y] and not bfs(board, visited, count, val, x, y):
                    delete_organ.add(val)
    return delete_organ

def delete_organisms(board, delete_list, micro_organisms_idx):
    for i in delete_list:
        data = micro_organisms_idx.pop(i)
        for x in range(N):
            for y in range(N):
                val = board[x][y]
                if val == i:
                    board[x][y] = 0
    

# 2. 배양 용기 이동
# 모든 미생물을 새로운 배양 용기로 이동
# 가장 넓은 영역 무리 선택 -> 먼저 투입된 것 우선순위
# x좌표가 작은 위치로 y좌표가 작은 위치로
# 이동할 공간이 없는 미생물은 사라짐

# 미생물 좌표 얻기
def get_organism_coord(board, idx):
    coord = []
    for x in range(N):
        for y in range(N):
            if board[x][y] == idx:
                coord.append((x, y))
    return coord

# 좌표들 중 최소 좌표 얻기
def get_min_coord(coord):
    min_x, min_y = 100, 100
    for x,y in coord:
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
    return min_x, min_y

# 현재 위치에서 보드판에 넣을 수 있는지 검토
def check_size(board, x, y, min_x, min_y, coord):
    is_possible = True
    for cx, cy in coord:
        nx, ny = x + cx - min_x, y + cy - min_y
        if not is_range(nx, ny) or board[nx][ny] != 0:
            is_possible = False
    return is_possible

# 보드판에 넣을 수 있는지 확인 후 이동하여 넣기
def put(new_board, board, idx):
    coord = get_organism_coord(board, idx)
    min_x, min_y = get_min_coord(coord)
    cx, cy = -1, -1
    for x in range(N):
        for y in range(N):
            is_possible = check_size(new_board, x, y, min_x, min_y, coord)
            # 넣을 수 있다면 넣기
            if is_possible:
                cx, cy = x, y
                break
        if is_possible:
            break
    if (cx,cy) != (-1, -1):
        for x, y in coord:
            nx, ny = cx + x - min_x, cy + y - min_y
            new_board[nx][ny] = idx
    return new_board


def re_arrange(board, micro_organisms_count):
    # 새로운 보드판
    new_board = [[0] * N for _ in range(N)]
    # 최대 영역 무리순으로 정렬
    # 영역 크기순 + 먼저 투입된것(idx가 작은것부터)
    max_kinds = [k for k, v in sorted(micro_organisms_count.items(), key=lambda x:(-x[1], x[0]) )]
    for kind in max_kinds:
        new_board = put(new_board, board, kind)

    # print("="*50)
    # for b in  new_board:
    #     print(b)
        
    return new_board


# 3. 실험 결과 기록
# 모든 인접한 무리쌍 확인 -> 두 무리의 맞닪은 면이 둘 이상이더라도 한번만 확인( (A,B)쌍 == (B,A)쌍)
# (A,B)쌍 = A영역 넓이 * B영역 넓이 -> 성과
# 확인한 모든 쌍의 성과를 더한 값
def get_score(board, micro_organisms_count):
    partners = []
    score = 0
    for x in range(N):
        for y in range(N):
            cur_val = board[x][y]
            if cur_val == 0:
                continue
            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]
                if not is_range(nx, ny):
                    continue
                next_val = board[nx][ny]
                if next_val == 0:
                    continue
                if cur_val != next_val:
                    if (cur_val, next_val) not in partners and (next_val, cur_val) not in partners:
                        partners.append((cur_val, next_val))
    for a, b in partners:
        tmp1 = micro_organisms_count.get(a)
        tmp2 = micro_organisms_count.get(b)
        score += tmp1 * tmp2
    return score



micro_organisms_idx = dict()
for i in range(Q):
    # 좌측 하단 , 우측 상단
    data = list(map(int, input().split()))
    x1,y1,x2,y2 = data
    micro_organisms_idx[i+1] = data
    # 1. 미생물 투입
    for x in range(x1, x2):
        for y in range(y1, y2):
            board[x][y] = i+1
    # 미생물 개수 갱신
    micro_organisms_count = calc_count(board)
    # print(micro_organisms_count)
    # 사라져야하는 것들
    delete_list = check_region(board, micro_organisms_count)
    # print("delete list : ", delete_list)
    # 삭제
    delete_organisms(board, delete_list, micro_organisms_idx)
    micro_organisms_count = calc_count(board)
    # print(micro_organisms_idx)
    # print("="*50, "기본", "="*50)
    # for b in  board:
    #     print(b)
    # 2. 배양 용기 이동
    board = re_arrange(board, micro_organisms_count)
    
    # 3. 성과 내기
    result = get_score(board, micro_organisms_count)
    print(result)
