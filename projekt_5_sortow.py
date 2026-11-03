import random
import time
import sys


sys.setrecursionlimit(20000)
random.seed(42)

# --- 0. Insertion sort (pozniej do hybryd) ---
def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# --- 1. Quicksort ---
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


# --- 2. Sortowanie rekurencyjne (Merge Sort) ---
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# --- 3. Dowolny (Heap Sort) ---
def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr


#wygenerowane
# --- 4. Hybryda 1: Quicksort + Insertion Sort dla małych podtablic ---
def hybrid_quicksort_in_place(arr, low, high, threshold=16):
    while low < high:
        if high - low + 1 < threshold:
            insertion_sort(arr, low, high)
            break
        else:
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            p = i + 1

            if p - low < high - p:
                hybrid_quicksort_in_place(arr, low, p - 1, threshold)
                low = p + 1
            else:
                hybrid_quicksort_in_place(arr, p + 1, high, threshold)
                high = p - 1


def hybrid_quicksort(arr):
    a = arr.copy()
    hybrid_quicksort_in_place(a, 0, len(a) - 1)
    return a


#wygenerowane
# --- 5. Hybryda 2: Merge Sort + Insertion Sort dla małych podtablic ---
def hybrid_merge_sort_rec(arr, temp, left, right, threshold=16):
    if right - left + 1 <= threshold:
        insertion_sort(arr, left, right)
        return
    mid = (left + right) // 2
    hybrid_merge_sort_rec(arr, temp, left, mid, threshold)
    hybrid_merge_sort_rec(arr, temp, mid + 1, right, threshold)

    # Scalanie
    i = left
    j = mid + 1
    for k in range(left, right + 1):
        if i > mid:
            temp[k] = arr[j]
            j += 1
        elif j > right:
            temp[k] = arr[i]
            i += 1
        elif arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            j += 1
    for k in range(left, right + 1):
        arr[k] = temp[k]


def hybrid_merge_sort(arr):
    a = arr.copy()
    temp = [0] * len(a)
    hybrid_merge_sort_rec(a, temp, 0, len(a) - 1)
    return a



def generate_datasets(n=10000):
    datasets = {}
    #podpowiedz od ai google, nie wiem czy sie zalicza pod wygenerowanie
    # 1. Dane losowe
    datasets["Losowe"] = [random.randint(0, 1000000) for _ in range(n)]

    # 2. 9000 posortowanych + 1000 nieposortowanych na końcu
    sorted_part = sorted([random.randint(0, 1000000) for _ in range(9000)])
    unsorted_part = [random.randint(0, 1000000) for _ in range(1000)]
    datasets["90% posortowane + 10% losowe"] = sorted_part + unsorted_part

    # 3. Dane z powtórzeniami (mały zakres wartości)
    datasets["Z powtórzeniami"] = [random.randint(0, 10) for _ in range(n)]

    # 4. Dane z powtórzeniami w kolejności odwrotnej
    dup_sorted = sorted([random.randint(0, 10) for _ in range(n)])
    datasets["Z powtórzeniami (odwrotne)"] = list(reversed(dup_sorted))

    return datasets



def run_benchmark():
    algorithms = {
        "Quicksort (klasyczny)": quicksort,
        "Merge Sort (rekurencyjny)": merge_sort,
        "Heap Sort (dowolny)": heap_sort,
        "Hybryda 1 (Quick + Insertion)": hybrid_quicksort,
        "Hybryda 2 (Merge + Insertion)": hybrid_merge_sort
    }

    datasets = generate_datasets(10000)

    print(f"{'Algorytm':<30} | {'Typ danych':<30} | {'Czas (s)':<10}")
    print("-" * 76)

    for data_name, data in datasets.items():
        for algo_name, algo_func in algorithms.items():
            test_data = data.copy()

            start_time = time.perf_counter()
            _ = algo_func(test_data)
            end_time = time.perf_counter()

            elapsed = end_time - start_time
            print(f"{algo_name:<30} | {data_name:<30} | {elapsed:.5f}s")
        print("-" * 76)


if __name__ == "__main__":
    print("Uruchamianie testów wydajnościowych algorytmów sortowania (N = 10 000)...\n")
    run_benchmark()