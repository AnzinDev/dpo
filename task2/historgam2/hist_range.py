import random
import time

hist = [0] * 10
times = [0] * 100 
new_hist_name = "hist0.txt"


def GetRandomNums():
    arr = [0] * 1000000
    for i in range(1000000):
        arr[i] = random.randint(0, 999)
    return arr


def CalcHist(histogram):
    for i in histogram:
        hist[(i // 100)] += 1


def HistDistance(a, b):
    if(len(a) != len(b)):
        return "Error: lists of different lengths."
    length = 0
    for i in range(len(a)):
        length += (a[i] - b[i]) ** 2
    return length ** 0.5


def ReadHistFromFile(path):
    with open(path, "r") as file_obj:
        a = [int(item) for item in (file_obj.read().split(","))]
        print(a)
        return a


def SaveHistToFile(histogram, path):
    string_to_save = ""
    for i in histogram:
        string_to_save += f"{i},"
    string_to_save[:-1]
    with open(path, "w") as file_obj:
            file_obj.write(string_to_save)


def main():
    list1 = ReadHistFromFile("hist1.txt")
    list2 = ReadHistFromFile("hist2.txt")
    print(f"Cartesian distance between historgams: {round(HistDistance(list1, list2), 5)}")
    buffer = GetRandomNums()
    CalcHist(buffer)
    SaveHistToFile(hist, new_hist_name)
    print(f"File {new_hist_name} saved. \nSaved hist: ", end = "")
    for i in hist:
        print(f"{i} ", end = "")
    print()


main()