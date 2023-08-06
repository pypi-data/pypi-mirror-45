from typing import Union, List


class ListNode:
    def __init__(self, val: int = None) -> None:
        self.val = val
        self.next = None


class LinkedList:
    def __init__(self, val: Union[int, List] = None) -> None:
        self.head = self.tail = None
        if val:
            self.add(val)

    def add(self, val):
        if self.head is None:
            self.head = self.tail = ListNode(val)
        else:
            self.tail.next = ListNode(val)

    def add1(self, val):
        lst = []
        lst.append(val)
        if lst:
            for i in range(len(lst)):
                self.tail.next = ListNode(lst[i])
                if self.tail.next is None:
                    break
                self.tail = self.tail.next

    def _traversal(self, list_node: ListNode = None) -> List:
        res = []
        if list_node is None:
            return res
        while list_node:
            if list_node:
                res.append(list_node.val)
            list_node = list_node.next
        return res

    def print(self) -> None:
        list_nodes = self._traversal(self.head)
        for list_node in list_nodes[:-1]:
            print(list_node, end='->')
        print(list_nodes[-1])

    def print1(self, list_node: ListNode = None) -> None:
        if list_node is None:
            list_node = self.head
        while list_node:
            if list_node.next:
                print(list_node.val, end='->')
            else:
                print(list_node.val)
            list_node = list_node.next
