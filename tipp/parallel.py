# Work around to mimic multiprocessing.Pool.map, which does not support class method
# as the function for Pool.
# See the answer by klaus se at StackOverflow:
# https://stackoverflow.com/questions/3288595/multiprocessing-how-to-use-pool-map-on-a-function-defined-in-a-class

import multiprocessing as mp


def fun(f, q_in, q_out):
  while True:
    i, x, args = q_in.get()
    if i is None:
      break
    q_out.put((i, f(x, *args)))

def parmap(f, X, nprocs, *args):
  q_in = mp.Queue(1)
  q_out = mp.Queue()

  proc = [mp.Process(target=fun, args=(f, q_in, q_out)) for _ in range(nprocs)]
  for p in proc:
    p.daemon = True
    p.start()

  sent = [q_in.put((i, x, args)) for i, x in enumerate(X)]
  [q_in.put((None, None, None)) for _ in range(nprocs)]
  res = [q_out.get() for _ in range(len(sent))]

  [p.join() for p in proc]

  return [x for i, x in sorted(res)]


if __name__ == '__main__':

  def sq_cub(i, plus):
    return i**2+plus, i**3+plus


  rslt = parmap(sq_cub, [1, 2, 3, 4, 6, 7, 8], 2, 4)
  print rslt