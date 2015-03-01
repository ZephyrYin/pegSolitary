# try:
#     import Queue as Q  # ver. < 3.0
# except ImportError:
#     import queue as Q
#
# class Skill(object):
#     def __init__(self, priority, description):
#         self.priority = priority
#         self.description = description
#         print('New Level:', description)
#         return
#     def __cmp__(self, other):
#         return self.priority > other.priority
#
# q = Q.PriorityQueue()
#
# q.put(Skill(5, 'Proficient'))
# q.put(Skill(10, 'Expert'))
# q.put(Skill(1, 'Novice'))
#
# while not q.empty():
#     next_level = q.get()
#     print('Processing level:', next_level.description)
import queue

class Node(object):
    def __init__(self, name, gCost, hCost):
        self.name = name
        self.gCost = gCost
        self.hCost = hCost

    def printNode(self):
        print(self.name)
        print('gCost: ', self.gCost)
        print('hCost: ', self.hCost)

    def __lt__(self, other):
        return self.gCost + self.hCost < other.gCost + other.hCost

a = Node('tom', 1, 9)
b = Node('lucy', 5, 8)
c = Node('jack', 1, 9)


l = queue.PriorityQueue()
l.put((1,a))
l.put((1,b))
l.put((13,c))
#
# l.put((a.gCost+a.hCost, a))
# l.put((b.gCost+b.hCost, b))
# l.put((c.gCost+c.hCost, c))
# while not l.empty():
#     n = l.get()
#     #print(n)
#     n[1].printNode()

import heapq
heap = []
heapq.heapify(heap)
heapq.heappush(heap, a)
heapq.heappush(heap, b)
heapq.heappush(heap, c)

while len(heap) > 0:
    top = heapq.heappop(heap)
    top.printNode()
    #print(l.get()[0])
    # n = l.get()[1]
    # n.printNode()
# l.put(6)
# l.put(7)
# l.put(8)
# while not l.empty():
#     n = l.get()
#     n.printNode()

# list = []
# list.append(a)
# list.append(b)
# list.append(c)
# list.sort(key=lambda Node: Node.hCost+Node.gCost, reverse=False)
# for l in list:
#     l.printNode()
#
# d = list.pop(0)
#
# d.printNode()
# names = ['Adam', 'Donald', 'John']
# names.sort(key=lambda x: x[3], reverse=True)
# print(names)