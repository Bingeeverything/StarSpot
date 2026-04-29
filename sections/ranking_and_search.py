import heapq

def add_to_queue(heap_list, mountain_name, stargazing_score):
    sort_value = stargazing_score * -1

    mountain_data = (sort_value, mountain_name)
    heapq.heappush(heap_list, mountain_data)

    return heap_list

def get_top_spots(heap_list, top_n=3):
    best_spots = heapq.nsmallest(top_n, heap_list)

    results = []
    for spot in best_spots:
        sort_value, mountain_name = spot
        actual_score = sort_value * -1
        results.append((mountain_name, actual_score))

    return results