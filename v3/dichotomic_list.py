class PreferenceNode:
    def __init__(self, preference, data):
        self.preference = preference
        self.data = data

    def __str__(self):
        return str(self.data.name)

class DichotomicList:
    def __init__(self, max_capacity):
        self._list = []
        self._max_capacity = max_capacity

    def insert(self, preference, data):
        # Creating a new node
        node = PreferenceNode(preference, data)

        # Search the index where inserting the node in order to keep the list sorted
        low = 0
        high = len(self._list) - 1
        while low < high:
            mid = (low + high) // 2
            if node.preference > self._list[mid].preference:
                high = mid
            else:
                low = mid + 1

        # Insert the node at best index
        self._list.insert(low, node)

    def insert_and_pop(self, preference, data):
        # If the maximum accepted preference is lower than the preference of the insertion candidate, we don't try to insert
        if preference > self._list[-1].preference:
            return data

        self.insert(preference, data)

        # Pop the least preferred from the list and returns it
        return self._list.pop(-1).data

    def is_full(self):
        return len(self._list) == self._max_capacity

    def __str__(self):
        return str([str(node) for node in self._list])
