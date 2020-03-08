from collections import Counter


class ChangeProblem():
  def __init__(self, amount, coins, change, goal):
    self.amount = amount
    self.coins = coins
    self.change = change
    self.goal = goal


# Read in our input
FILE = 'wedstrijd.invoer'
with open(FILE, 'r') as ifp:
  lines = ifp.readlines()

# Parse the content
n_test_cases = int(lines[0])
lines = lines[1:]
test_cases = []
for i in range(n_test_cases):
  amount = int(lines[i*4])
  coins = list(map(int, lines[i*4 + 1].strip().split()[1:]))
  change = list(map(int, lines[i*4 + 2].strip().split()[1:]))
  goal = list(map(int, lines[i*4 + 3].strip().split()[1:]))
  
  test_cases.append(ChangeProblem(amount, coins, change, goal))

def coin_available(munt, coins, solution):
  """Check if the provided coin is still available"""
  coins_cntr = Counter(coins)
  solution_cntr = Counter(solution)
  return solution_cntr[munt] < coins_cntr[munt]

def exceed_amount(munt, solution, amount):
  """Check if we exceed a provided amount"""
  largest_coin = max(solution + [munt])
  curr_amount = sum(solution + [munt])
  return (curr_amount - largest_coin) >= test_case.amount

def valid(munt, coins, solution, amount):
  """Checks if a candidate solution is valid"""
  return (
    coin_available(munt, coins, solution) and 
    not exceed_amount(munt, solution, amount)
  )

def solve(coins, amount, solutions):
  """Return minimal amount of coins required to form the provided amount"""
  best_sol, min_coins = None, float('inf')
  for munt in set(coins):
    solution = solutions[amount - munt]
    if solution is not None:
      n_coins = len(solution) + 1
      if valid(munt, coins, solution, amount) and n_coins < min_coins:
        min_coins = n_coins
        best_sol = solution + [munt]
  return best_sol

# Solve test cases
with open('wedstrijd.oplossing', 'w+') as ofp:
  for t, test_case in enumerate(test_cases):
    # We need to insert the price (amount) and the sum of coins
    # we want to have returned. Only exceeding this total with our
    # final (largest) coin.
    total = test_case.amount + sum(test_case.goal)

    # If the coins we want to get returned are not being returned
    # by the machine, then impossible.
    if len(set(test_case.goal) - set(test_case.change) ) != 0:
      ofp.write('{} {}\n'.format(t + 1, 'ONMOGELIJK'))
      continue

    # Solve the minimal amount of coins needed by dynamic programming.
    # We solve this by iteratively solving solutions[i] with i
    # the total we want to achieve. 
    # Start of with initialization.
    solutions = [None] * (max(test_case.coins) + 1)
    for munt in set(test_case.coins):
      solutions[munt] = [munt]

    # Solve iteratively.
    for i in range(max(test_case.coins) + 1, total + 1):
      solutions.append(solve(test_case.coins, i, solutions))

    # Check if solution is possible & write away
    if solutions[total] is not None: 
      ofp.write('{} {}\n'.format(t + 1, len(solutions[total])))
    else:
      ofp.write('{} {}\n'.format(t + 1, 'ONMOGELIJK'))
