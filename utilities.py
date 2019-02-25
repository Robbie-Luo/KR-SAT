# test if a predicate [p] holds for all elements of [l]
def forall(l,p):
  return len([x for x in l if p(x)]) == len(l)

# test if a predicate [p] holds for some element of [l]
def exists(l,p):
  return len([x for x in l if p(x)]) > 0

# flatten list of lists
def flatten(l):
  return [x for xs in l for x in xs]

# remove duplicates from [l]
# nb: does not guarantee order
def uniquify(l):
  return list(set(l))


def symbols_of(f):
  return uniquify([ abs(l) for l in flatten(f) ])

# c is satisfied by v
# if c contains at least one literal which is true
def clause_satisfied(c,v):
  return exists(c, lambda l: l in v)

# f is satisfied by v
# if every clause of f is satisfied by v
def satisfied(f,v):
  return forall(f, lambda c: clause_satisfied(c,v))

# f is unsatisfiable
# if there exists a clause of f that is false (all literals are false)
def unsatisfiable(f,v):
  return exists(f, lambda c: forall(c, lambda l: -l in v))

def solve_dfs(f):
  def dfs(sym,v):
    if satisfied(f,v): return v
    elif unsatisfiable(f,v): return False
    else:
      l, s = sym[0], sym[1:]
      return dfs(s, v+[l]) or dfs(s, v+[-l])
  return dfs(symbols_of(f), [])