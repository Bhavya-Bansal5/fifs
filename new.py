from collections import defaultdict
     
def solution(numbers):
    counts = defaultdict(int)
    answer = 0
    for element in numbers:
        counts[element] += 1
        for two_power in range(21):
            second_element = (1 << two_power) - element
            answer += counts[second_element]
            print(element, second_element, counts[second_element])
    return answer 
print(solution([-2, -1, 0, 1, 2]))