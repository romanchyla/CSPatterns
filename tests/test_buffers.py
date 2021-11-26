from cspatterns.datastructures import buffer

def test_circular_buffer():
    b = buffer.CircularBuffer(2, ['n'])
    assert len(b.next) == 2
    assert b.n is None

    b = buffer.CircularBuffer.create(2, attrs=['n', 'fib'])
    curr = b
    out = [0, 1, ]
  

    curr.prev[-2].n = 0
    curr.prev[-2].fib = 1
    curr.prev[-1].n = 1
    curr.prev[-1].fib = 1
    

    # we are going to calculate fibonacci
    while curr.prev[-1].n < 12:
        curr.n = curr.prev[-1].n + 1
        curr.fib = curr.prev[-1].fib + curr.prev[-2].fib
        out.append(curr.fib)
        curr = curr.next[1]

    assert out == [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]