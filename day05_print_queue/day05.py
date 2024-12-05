#!/usr/bin/env python3

import sys

def correctly_ordered(pages, rules):
    for index, page in enumerate(pages):
        if any((page, earlier_page) in rules for earlier_page in pages[:index]):
            return False
        if any((later_page, page) in rules for later_page in pages[index+1:]):
            return False
    return True

def middle_page(pages):
    return pages[len(pages) // 2]

def do_part1(updates, rules):
    return sum(middle_page(pages) for pages in updates if correctly_ordered(pages, rules))

def order_correctly(pages, rules):
    ordered_pages = []
    for page in pages:
        for index, ordered_page in enumerate(ordered_pages):
            if (page, ordered_page) in rules:
                ordered_pages.insert(index, page)
                break
        else:
            ordered_pages.append(page)
    return ordered_pages

def do_part2(updates, rules):
    return sum(middle_page(order_correctly(pages, rules)) for pages in updates if not correctly_ordered(pages, rules))

if __name__ == '__main__':
    rules = set()
    updates = None
    for line in sys.stdin:
        line = line.strip()
        if updates is None:
            if line:
                before, after = map(int, line.split('|'))
                rules.add((before, after))
            else:
                updates = []
        else:
            pages = list(map(int, line.split(',')))
            updates.append(pages)
    part1 = do_part1(updates, rules)
    print(f"Part 1: {part1}")
    part2 = do_part2(updates, rules)
    print(f"Part 2: {part2}")
