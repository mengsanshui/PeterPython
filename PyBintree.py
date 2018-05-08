
class binaryTree:
    def __init__(self, nodeData, left=None, right=None):
        self.nodeData = nodeData
        self.left = left
        self.right = right
def __str__(self):
    return str(self.nodeData)

def traverse(tree):
    if tree.left != None:
        traverse(tree.left)
    if tree.right != None:
        traverse(tree.right)
    print(tree.nodeData)

tree = binaryTree("Root")
BranchA = binaryTree("Branch A")
BranchB = binaryTree("Branch B")
tree.left = BranchA
tree.right = BranchB
LeafC = binaryTree("Leaf C")
LeafD = binaryTree("Leaf D")
LeafE = binaryTree("Leaf E")
LeafF = binaryTree("Leaf F")
BranchA.left = LeafC
BranchA.right = LeafD
BranchB.left = LeafE
BranchB.right = LeafF

graph = {'A': ['B', 'F'],
        'B': ['A', 'C'],
        'C': ['B', 'D'],
        'D': ['C', 'E'],
        'E': ['D', 'F'],
        'F': ['E', 'A']}

def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        print("Ending")
        return path
    for node in graph[start]:
        print("Checking Node ", node)
        if node not in path:
            print("Path so far ", path)
        newp = find_path(graph, node, end, path)
        if newp:
            return newp

def snort(data):
    for sindex in range(0, len(data)):
        minindex = sindex
        for neindex in range(sindex+1, len(data)):
            if data[neindex] < data[minindex]:
                minindex = neindex
        if minindex != sindex:
            data[sindex], data[minindex] = data[minindex], data[sindex]
        print(data)

def inort(data):
    for scanIndex in range(1, len(data)):
        temp = data[scanIndex]
        minIndex = scanIndex
        while minIndex > 0 and temp < data[minIndex - 1]:
            data[minIndex] = data[minIndex - 1]
            minIndex -= 1
        data[minIndex] = temp
        print(data)

def mergeSort(list):
    # Determine whether the list is broken into individual pieces.
    if len(list) < 2:
        return list
    # Find the middle of the list.
    middle = len(list)//2
    # Break the list into two pieces.
    left = mergeSort(list[:middle])
    right = mergeSort(list[middle:])
    # Merge the two sorted pieces into a larger piece.
    print("Left side: ", left)
    print("Right side: ", right)
    merged = merge(left, right)
    print("Merged ", merged)
    return merged

def merge(left, right):
# When the left side or the right side is empty,
# it means that this is an individual item and is already sorted.
    if not len(left):
        return left
    if not len(right):
        return right
    # Define variables used to merge the two pieces.
    result = []
    leftIndex = 0
    rightIndex = 0
    totalLen = len(left) + len(right)
    # Keep working until all of the items are merged.
    while (len(result) < totalLen):
        # Perform the required comparisons and merge the pieces according to value.
        if left[leftIndex] < right[rightIndex]:
            result.append(left[leftIndex])
            leftIndex += 1
        else:
            result.append(right[rightIndex])
            rightIndex += 1
        # When the left side or the right side is longer,
        # add the remaining elements to the result.
        if leftIndex == len(left) or rightIndex == len(right):
            result.extend(left[leftIndex:] or right[rightIndex:])
            break
    return result


def partition(data, left, right):
    pivot = data[left]
    lIndex = left + 1
    rIndex = right
    while True:
        while lIndex <= rIndex and data[lIndex] <= pivot:
            lIndex += 1
        while rIndex >= lIndex and data[rIndex] >= pivot:
            rIndex -= 1
        if rIndex <= lIndex:
            break
        data[lIndex], data[rIndex] = data[rIndex], data[lIndex]
        print(data)
    data[left], data[rIndex] = data[rIndex], data[left]
    print(data)
    return rIndex

def quickSort(data, left, right):
    if right <= left:
        return
    else:
        pivot = partition(data, left, right)
        quickSort(data, left, pivot-1)
        quickSort(data, pivot+1, right)
    return data


