N, M = map(int, input().split())

board = [[0] * N for _ in range(N)]

boxes = dict()
for _ in range(M):
    k, h, w, y = map(int, input().split())
    # y위치, 가로크기, 세로크기, 번호
    boxes[k]= [h, w, y-1]
# 박스좌표 담기 -> (left_up, left_down, right_up, right_down)
boxes_coord = dict()

# 1. 택배 투입
# 왼쪽열 위치 : c, 가로 크기 : w , 세로 크기 : h, 번호: k
# 투입후 하단으로 낙하 -> 다른 짐을 만나면 멈춤
# 택배 아래로 하강
def input_package(board, boxes, boxes_coord):
    for idx, v in boxes.items():
        h, w, y = v
        start_x = -1
        # 상자의 높이를 확인 후 가장 아래로 내려갈 수 있는 곳 찾기
        for bottom in range(h-1, N):
            is_possible = True
            # 상자 길이만큼 다 들어갈 수 있는지 검토
            for x in range(bottom - h +1, bottom+1):
                new_array = board[x][y:y+w]
                # 모두 0인지 판별(블록이 없는지 검사) -> 모두 0이 아니라면 : 못 넣는 곳
                if any(new_array):
                    is_possible = False
                    break
            # 넣을 수 있다면 그 곳을 갱신 -> 아래로 확인하니 제일 마지막에 갱신되 곳이 가장 하단 부분
            if is_possible:
                start_x = bottom
            else:
                break
        if start_x != -1:
            # (left_up, left_down, right_up, right_down)
            boxes_coord[idx] = [(start_x-h+1, y), (start_x, y), (start_x-h+1, y+w-1), (start_x, y+w-1)]
            for i in range(h):
                board[start_x-i][y:y+w] = [idx for _ in range(w)]

# 위의 박스들 내리기
def re_arrange(board, boxes, boxes_coord):
    # 남아 있는 박스만 추출 -> 하단 밑 x좌표가 가장 큰것부터 내림차순 정렬
    active_boxes = sorted(boxes_coord.keys(), key=lambda idx:-boxes_coord[idx][1][0])
    for idx in active_boxes:
        h, w, y = boxes[idx]
        bottom, top = boxes_coord[idx][1][0], boxes_coord[idx][0][0]
        for x in range(top, bottom+1):
            # 이동 가능을 확인하기 위해 잠시 비워두기
            board[x][y:y+w] = [0] * w
        
        # 한칸씩 내려가며 블록이 있는지 검사
        next_bottom = bottom
        for x in range(bottom+1, N):
            new_array = board[x][y:y+w]
            # 다른 블록이 존재한다면
            if any(new_array):
                break
            # 존재하지 않다면
            next_bottom = x
        # 새로운 위치로 갱신 -> (left_up, left_down, right_up, right_down)
        boxes_coord[idx] = [(next_bottom-h+1, y), (next_bottom, y), (next_bottom-h+1, y+w-1), (next_bottom,y+w-1)]
        
        # 보드판에 다시 기록
        for x in range(next_bottom-h+1, next_bottom+1):
            board[x][y:y+w] = [idx for _ in range(w)]
    
# 2. 택배 하차(좌)
# 좌로 이동시 택배와 부딪히지 않고 뺄 수 있는 택배부터 하차 -> 여러개일 시 k작은것이 우선순위
# 하차 후 떨어질 수 있는 것들은 떨어짐
def remove_left(board, boxes, boxes_coord):
    remove_list = []
    for idx in boxes_coord.keys():
        h, w, y = boxes[idx]
        left_top_x, left_bottom_x = boxes_coord[idx][0][0], boxes_coord[idx][1][0]
        is_possible = True
        for x in range(left_top_x, left_bottom_x+1):
            new_array = board[x][:y]
            # 좌측으로 뺄 수 없는 것
            if any(new_array):
                is_possible = False
                break
        # 제거 가능한 것
        if is_possible:
            remove_list.append(idx)
    remove_list.sort()
    # 번호가 가장 작은 것 제거
    num = remove_list[0]
    # print(num)
    h, w, y = boxes[num]
    bottom, top = boxes_coord[num][1][0], boxes_coord[num][0][0]
    for x in range(top, bottom+1):
        # 보드판에서 제거
        board[x][y:y+w] = [0] * w
    boxes_coord.pop(num)
    boxes.pop(num)
    return num

# 3. 택배 하차(우)
# 우로 이동시 택배와 부딪히지 않고 뺄 수 있는 택배부터 하차 -> 여러개일 시 k작은것이 우선순위
# 하차 후 떨어질 수 있는 것들은 떨어짐
def remove_right(board, boxes, boxes_coord):
    remove_list = []
    for idx in boxes_coord.keys():
        h, w, y = boxes[idx]
        right_top_x, right_bottom_x = boxes_coord[idx][2][0], boxes_coord[idx][3][0]
        is_possible = True
        for x in range(right_top_x, right_bottom_x+1):
            new_array = board[x][y+w:]
            # 좌측으로 뺄 수 없는 것
            if any(new_array):
                is_possible = False
                break
        # 제거 가능한 것
        if is_possible:
            remove_list.append(idx)
    remove_list.sort()
    # 번호가 가장 작은 것 제거
    num = remove_list[0]
    # print(num)
    h, w, y = boxes[num]
    bottom, top = boxes_coord[num][1][0], boxes_coord[num][0][0]
    for x in range(top, bottom+1):
        # 보드판에서 제거
        board[x][y:y+w] = [0] * w
    boxes_coord.pop(num)
    boxes.pop(num)
    return num
# 모든 택배 하차시까지 2,3번 반복

    
input_package(board, boxes, boxes_coord)
# for b in board:
#     print(b)
# print(boxes_coord)
while boxes_coord:
    left = remove_left(board, boxes, boxes_coord)
    re_arrange(board, boxes, boxes_coord)
    print(left)
    right = remove_right(board, boxes, boxes_coord)
    re_arrange(board, boxes, boxes_coord)
    print(right)
# for b in board:
#     print(b)
# print(boxes_coord)
