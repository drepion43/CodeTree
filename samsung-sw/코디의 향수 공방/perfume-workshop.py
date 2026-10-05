import bisect
from collections import Counter

Q = int(input())
line = list(map(int, input().split()))
# 1: 향료 준비
# 2: 향료 추가 : N+1,N+2,.로 추가 향로 번호 부여
# 3: 향료 폐기 : idx번 향료 폐기, 없다면 -1
# 4; 블렌딩 : 향도 합이 K가 되도록 향로를 선택시 최소 개수를 출력
# 5: 향수 구성 : 
types1 = line[0]
N = line[1]
difuse = {i+1:line[2+i] for i in range(N)}
discarded = set()
cnt = N

def blending(available, k):
    available = list(set(available))
    dp = [float('inf')] * (k+1)
    # 0을 만들기 위해서는 0개가 필요
    dp[0] = 0
    for i in range(1, k+1):
        # i 값을 만들기 위해 가지고 있는 것들로 표현 가능 개수 구하기
        for v in available:
            if i - v >= 0 and dp[i-v] != float('inf'):
                # 더 작은 것이 있다면 개수
                dp[i] = min(dp[i], dp[i-v] + 1)
    return dp[k] if dp[k] != float('inf') else -1


def difuse_composition(available, K):
    freq = Counter(available)
    if not freq:
        return 0
    
    # 고유 향도 오름차순 정렬
    unique_vals = sorted(freq.keys())
    U = len(unique_vals)
    
    # Suffix Sum (특정 인덱스 이후의 향료 총 개수)
    suffix_sum = [0] * (U + 1)
    for i in range(U - 1, -1, -1):
        suffix_sum[i] = suffix_sum[i + 1] + freq[unique_vals[i]]
        
    count = 0
    for i in range(U):
        top = unique_vals[i]
        top_count = freq[top]
        
        for j in range(U):
            middle = unique_vals[j]
            middle_count = freq[middle]
            # 필요한 최소 베이스 향도
            target_base = K - (top + middle)
            
            # target_base 이상인 첫 번째 위치를 이진 탐색으로 찾음
            idx = bisect.bisect_left(unique_vals, target_base)
            
            # 만족하는 베이스 향료들의 총 개수
            valid_base_count = suffix_sum[idx]
            
            count += top_count * middle_count * valid_base_count
            
    return count

for i in range(Q-1):
    # 입력
    types, val = map(int, input().split())
    # 향료 추가
    if types == 2:
        cnt += 1
        difuse[cnt] = val
    # 향료 폐기
    elif types == 3:
        if val not in difuse or val in discarded:
            print(-1)
        else:
            result = difuse[val]
            discarded.add(val)
            print(result)
    # 블랜딩
    elif types == 4:
        available = [difuse[i] for i in difuse if i not in discarded]
        result = blending(available, val)
        print(result)
    elif types == 5:
        available = [difuse[i] for i in difuse if i not in discarded]
        result = difuse_composition(available, val)
        print(result)
