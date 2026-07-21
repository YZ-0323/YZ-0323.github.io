"""
Inspired by the classic eggdrop problem: 100 floors, 2 eggs.
Use the least steps needed to find where the egg breaks.
Goal:
Find minimum attempts needed in worst case.
"""
# 1. Linear Search
def linear_search(floors, breaking_floor):
    """
    Test floors one by one from bottom.
    Requires no assumption about egg number.
    """
    attempts = 0
    for floor in range(1, floors + 1):
        attempts += 1
        if floor >= breaking_floor:
            return attempts
    return attempts
# 2. Binary Search
def binary_search(floors, breaking_floor):
    """
    Binary search.
    Assumes failed tests do not consume resources.
    """
    low = 1
    high = floors
    attempts = 0
    while low <= high:
        attempts += 1
        mid = (low + high) // 2
        if mid == breaking_floor:
            return attempts
        elif mid < breaking_floor:
            low = mid + 1
        else:
            high = mid - 1
    return attempts
# 3. Two Egg Optimal Strategy
def two_egg_optimal(floors):
    """
    Optimal solution when only 2 eggs exist.
    Find smallest m such that:
        1 + 2 + ... + m >= floors
    """
    attempts = 0
    covered = 0
    while covered < floors:
        attempts += 1
        covered += attempts
    return attempts
# 4. General Dynamic Programming
def egg_drop_dp(eggs, floors):
    """
    Dynamic programming solution.
    dp[k][n]:
    minimum attempts needed with k eggs and n floors
    """
    dp = [[0] * (floors + 1) for _ in range(eggs + 1)]
    for i in range(floors + 1):
        dp[1][i] = i
    for k in range(1, eggs + 1):
        dp[k][0] = 0
    for k in range(2, eggs + 1):
        for n in range(1, floors + 1):
            dp[k][n] = float("inf")
            for x in range(1, n + 1):
                worst_case = 1 + max(
                    dp[k-1][x-1],
                    dp[k][n-x]
                )
                dp[k][n] = min(
                    dp[k][n],
                    worst_case
                )
    return dp[eggs][floors]
# Experiment
if __name__ == "__main__":
    floors = 100
    breaking_floor = 73
    print("Floors:", floors)
    print("Breaking floor:", breaking_floor)
    print("---------------------------")
    print(
        "Linear Search:",
        linear_search(floors, breaking_floor),
        "attempts"
    )
    print(
        "Binary Search:",
        binary_search(floors, breaking_floor),
        "attempts"
    )
    print(
        "Two Egg Optimal:",
        two_egg_optimal(floors),
        "attempts"
    )
    print(
        "DP (2 eggs):",
        egg_drop_dp(2, floors),
        "attempts"
    )
    print(
        "DP (3 eggs):",
        egg_drop_dp(3, floors),
        "attempts"
    )