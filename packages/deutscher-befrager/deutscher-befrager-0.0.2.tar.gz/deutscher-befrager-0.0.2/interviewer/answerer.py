import functools as fun
from random import shuffle, uniform

def next_question(questions):
    """Determin the next question"""
    # len(dictview)
    bump_pairs = list(
        map( 
            lambda k: (k, _inital_bump(questions[k])), 
            questions.keys()
        )
    )        
    bump_pairs = sorted(bump_pairs, key=lambda p: p[0]) # sort by key

    age_acc = 0
    aged_bump_pairs = []
    for pair in bump_pairs:
        key, bump = pair
        new_bump = bump + age_acc
        aged_bump_pairs.append((key, new_bump))
        age_acc = age_acc + 0.1

    bump_pairs = aged_bump_pairs
        
    # click.echo(bump_pairs)

    bump_min = fun.reduce(_min, bump_pairs, 0)
    bump_max = fun.reduce(_max, bump_pairs, 0)

    def remap_pair(pair):
        key, bump = pair
        return (key, _remap(bump, bump_max, bump_min, 1, 0))

    final_pairs = list(map(remap_pair, bump_pairs))
    shuffle(final_pairs)
    random_bump = uniform(0, 1.0)
    final_key = final_pairs[0][0] 
    for pair in final_pairs:
        key, bump = pair
        if bump < random_bump:
            final_key = key
            break

    # click.echo(f'bump_pairs: {bump_pairs}')
    # click.echo(f'final_pairs: {final_pairs}')
    # click.echo(random_bump)
    # click.echo(final_key)
    return final_key

def _min(acc, pair):
    key, bump = pair
    if bump < acc: 
        return bump
    return acc

def _max(acc, pair):
    key, bump = pair
    if bump > acc: 
        return bump
    return acc

def _remap(old_value, old_max, old_min, new_max, new_min):
    old_range = (old_max - old_min)
    new_value = new_min
    if (old_range != 0):
        new_range = (new_max - new_min)  
        new_value = (((old_value - old_min) * new_range) / old_range) + new_min
    return new_value

def _inital_bump(q):
    bump = 0
    if 'A' in q:
        bump += len(q['A'])
    if 'Grade' in q:
        bump += q['Grade']
    return bump
