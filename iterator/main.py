from collections import deque


class BTreeNode:
    lt_node = None
    gt_node = None

    def __init__(self, val):
        self.val = val

    def add(self, val):
        if val == self.val:
            return
        elif val < self.val:
            if not self.lt_node:
                self.lt_node = BTreeNode(val)
            else:
                self.lt_node.add(val)
        else:
            if not self.gt_node:
                self.gt_node = BTreeNode(val)
            else:
                self.gt_node.add(val)

    def __iter__(self):
        # return BTreeNodeIter(self)
        return BTreeNode.better_iter(self)

    @staticmethod
    def better_iter(node):
        if node.lt_node:
            yield from BTreeNode.better_iter(node.lt_node)
        yield node.val
        if node.gt_node:
            yield from BTreeNode.better_iter(node.gt_node)


class BTreeNodeIter:
    def __init__(self, node):
        self.stack = deque()
        self.fill_stack(node)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration
        return self.stack.popleft()

    def fill_stack(self, node):
        if node.lt_node:
            self.fill_stack(node.lt_node)
        self.stack.append(node.val)
        if node.gt_node:
            self.fill_stack(node.gt_node)


root = BTreeNode(10)
root.add(15)
root.add(13)
root.add(-3)
root.add(0)
root.add(-20)
