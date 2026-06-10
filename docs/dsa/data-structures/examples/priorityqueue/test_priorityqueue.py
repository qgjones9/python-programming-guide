import pytest
from priorityqueue import IndexedMinPQ, PriorityQueue


def test_empty_priority_queue_raises():
    pq = PriorityQueue()
    assert pq.is_empty()
    assert len(pq) == 0
    with pytest.raises(IndexError):
        pq.peek()
    with pytest.raises(IndexError):
        pq.pop()
    with pytest.raises(IndexError):
        pq.peek_priority()


def test_push_and_peek_max_priority():
    pq = PriorityQueue()
    pq.push("low", priority=3)
    pq.push("high", priority=10)
    pq.push("mid", priority=5)
    assert pq.peek() == "high"
    assert pq.peek_priority() == 10


def test_pop_returns_descending_max_priority():
    pq = PriorityQueue()
    pairs = [(4, "d"), (1, "a"), (7, "g"), (3, "c"), (9, "i")]
    for prio, item in pairs:
        pq.push(item, priority=prio)
    popped = []
    while not pq.is_empty():
        popped.append((pq.peek_priority(), pq.pop()))
    assert popped == [(9, "i"), (7, "g"), (4, "d"), (3, "c"), (1, "a")]


def test_equal_priority_fifo_tie_break():
    pq = PriorityQueue()
    pq.push("first", priority=5)
    pq.push("second", priority=5)
    pq.push("third", priority=5)
    assert pq.pop() == "first"
    assert pq.pop() == "second"
    assert pq.pop() == "third"
    assert pq.is_empty()


def test_from_pairs_max_queue():
    tasks = [(8.0, "urgent"), (3.0, "low"), (5.0, "mid")]
    pq = PriorityQueue.from_pairs(tasks, max_queue=True)
    assert pq.pop() == "urgent"
    assert pq.pop() == "mid"
    assert pq.pop() == "low"
    assert pq.is_empty()


def test_min_priority_queue():
    pq = PriorityQueue(max_queue=False)
    pq.push("far", priority=10)
    pq.push("near", priority=2)
    pq.push("mid", priority=5)
    assert pq.peek_priority() == 2
    assert pq.pop() == "near"
    assert pq.pop() == "mid"
    assert pq.pop() == "far"
    assert pq.is_empty()


def test_merge_combines_queues():
    left = PriorityQueue.from_pairs([(5, "a"), (2, "b")])
    right = PriorityQueue.from_pairs([(8, "c"), (1, "d")])
    left.merge(right)
    assert right.is_empty()
    assert left.pop() == "c"
    assert left.pop() == "a"
    assert left.pop() == "b"
    assert left.pop() == "d"
    assert left.is_empty()


def test_clear_resets_queue():
    pq = PriorityQueue.from_pairs([(1, "a"), (2, "b")])
    pq.clear()
    assert pq.is_empty()
    assert len(pq) == 0
    with pytest.raises(IndexError):
        pq.peek()


def test_iter_yields_items_in_heap_order():
    pq = PriorityQueue.from_pairs([(3, "a"), (1, "b"), (2, "c")])
    assert set(pq) == {"a", "b", "c"}


def test_negative_priorities():
    pq = PriorityQueue()
    pq.push("neg", priority=-3)
    pq.push("zero", priority=0)
    pq.push("pos", priority=2)
    assert pq.pop() == "pos"
    assert pq.pop() == "zero"
    assert pq.pop() == "neg"


def test_empty_indexed_min_pq_raises():
    ipq = IndexedMinPQ(4)
    with pytest.raises(IndexError):
        ipq.pop_min()


def test_indexed_min_pq_insert_and_pop_order():
    ipq = IndexedMinPQ(5)
    ipq.insert(2, 8.0)
    ipq.insert(0, 3.0)
    ipq.insert(4, 5.0)
    assert ipq.pop_min() == (0, 3.0)
    assert ipq.pop_min() == (4, 5.0)
    assert ipq.pop_min() == (2, 8.0)
    with pytest.raises(IndexError):
        ipq.pop_min()


def test_indexed_min_pq_decrease_key():
    ipq = IndexedMinPQ(4)
    ipq.insert(1, 10.0)
    ipq.insert(2, 4.0)
    ipq.insert(3, 7.0)
    ipq.decrease_key(1, 2.0)
    assert ipq.pop_min() == (1, 2.0)
    assert ipq.pop_min() == (2, 4.0)
    assert ipq.pop_min() == (3, 7.0)


def test_indexed_min_pq_decrease_key_no_op_when_not_smaller():
    ipq = IndexedMinPQ(3)
    ipq.insert(0, 5.0)
    ipq.decrease_key(0, 6.0)
    ipq.decrease_key(0, 5.0)
    assert ipq.pop_min() == (0, 5.0)


def test_indexed_min_pq_dijkstra_style():
    adj = {
        0: [(1, 4.0), (2, 1.0)],
        1: [(3, 1.0)],
        2: [(1, 2.0), (3, 5.0)],
    }
    n = 4
    start = 0

    dist = [float("inf")] * n
    dist[start] = 0.0
    pq = IndexedMinPQ(n)
    pq.insert(start, 0.0)
    while True:
        try:
            u, du = pq.pop_min()
        except IndexError:
            break
        if du > dist[u]:
            continue
        for v, w in adj.get(u, []):
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if pq._qp[v] < 0:
                    pq.insert(v, nd)
                else:
                    pq.decrease_key(v, nd)

    assert dist == [0.0, 3.0, 1.0, 4.0]
