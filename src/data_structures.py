import random


class SkipList:
    class Node:
        def __init__(self, key: int, level: int):
            self._key = key
            self.forward = [None] * (level + 1)

        @property
        def key(self) -> int:
            return self._key

    def __init__(self, max_level, p):
        self._max_level = max_level
        self._p = p
        self._sentinel = SkipList.Node(-1, self._max_level)

        self.level = 0

    def _random_level(self) -> int:
        level = 0
        while random.random() < self._p and level < self._max_level:
            level += 1
        return level

    def insert(self, key) -> None:
        update = [None] * (self._max_level + 1)
        current = self._sentinel

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]
        if current is None or current.key != key:
            random_level = self._random_level()
            if random_level > self.level:
                for i in range(self.level + 1, random_level + 1):
                    update[i] = self._sentinel
                self.level = random_level

            node = SkipList.Node(key, random_level)
            for i in range(random_level + 1):
                node.forward[i] = update[i].forward[i]
                update[i].forward[i] = node

    def search(self, key, current=None) -> "SkipList.Node":
        """Go to the previous key of the possible next key

        :param key: Value to find
        :type key: int
        :param current: Starting node, defaults to None
        :type current: SkipList.Node, optional
        :return: Node to be left of the target node
        :rtype: Optional[SkipList.Node]
        """
        current = current
        if current is None:
            current = self._sentinel
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]

        return current

    def __contains__(self, key: int) -> bool:
        """Check membership for key

        :param key: Item to be checked
        :type key: int
        :return: True if list contains key False otherwise
        :rtype: bool
        """
        current = self._sentinel
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]

        current = current.forward[0]
        return current and current.key == key

    def __str__(self) -> str:
        head = self._sentinel
        res = ""
        for lvl in range(self.level + 1):
            res += f"Level {lvl}: "
            node = head.forward[lvl]
            while node != None:
                res += f"{node.key} "
                node = node.forward[lvl]
            res += "\n"
        return res


if __name__ == "__main__":
    lst = SkipList(3, 0.5)
    lst.insert(3)
    lst.insert(6)
    lst.insert(7)
    lst.insert(9)
    lst.insert(12)
    lst.insert(19)
    lst.insert(17)
    lst.insert(26)
    lst.insert(21)
    lst.insert(25)
    print(lst)
    print(17 in lst)
    print(lst.search(17).key)
