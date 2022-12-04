import itertools

# riddle: _ + _ * _^2 + _^3 - _ = 399
# blue coin: 9 dots
# concave coin: 7 dots
# corroded coin: triangle
# red coin: 2 dots
# shiny coin: pentagon

coins = {
    2: 'red coin',
    3: 'corroded coin',
    5: 'shiny coin',
    7: 'concave coin',
    9: 'blue coin'
}

for p in itertools.permutations(coins.keys()):
    a, b, c, d, e = p
    if a + b * c**2 + d**3 - e == 399:
        print(f'solution: {coins[a]}, {coins[b]}, {coins[c]}, {coins[d]}, {coins[e]}')
