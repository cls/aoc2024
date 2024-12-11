use nom::{
    character::complete::{newline, space1, u64},
    combinator::all_consuming,
    error::Error,
    multi::separated_list1,
    sequence::terminated,
    Err,
};
use std::collections::HashMap;

fn parse_stones(input: &str) -> Result<HashMap<u64, u64>, Err<Error<&str>>> {
    let (_eof, stones) = all_consuming(terminated(separated_list1(space1, u64), newline))(input)?;
    let mut quantities = HashMap::new();
    for stone in stones {
        quantities.entry(stone).and_modify(|quantity| *quantity += 1).or_insert(1);
    }
    Ok(quantities)
}

fn blink(quantities: HashMap<u64, u64>) -> HashMap<u64, u64> {
    let mut new_quantities = HashMap::new();
    for (stone, quantity) in quantities {
        if stone == 0 {
            new_quantities.entry(1).and_modify(|new_quantity| *new_quantity += quantity).or_insert(quantity);
        } else {
            let digits = stone.ilog10() + 1;
            if digits % 2 == 0 {
                let split = 10_u64.pow(digits / 2);
                new_quantities.entry(stone / split).and_modify(|new_quantity| *new_quantity += quantity).or_insert(quantity);
                new_quantities.entry(stone % split).and_modify(|new_quantity| *new_quantity += quantity).or_insert(quantity);
            } else {
                new_quantities.entry(stone * 2024).and_modify(|new_quantity| *new_quantity += quantity).or_insert(quantity);
            }
        }
    }
    new_quantities
}

#[test]
fn blinks_example() {
    let mut stones = parse_stones(include_str!("../example.txt")).unwrap();
    for _n in 0..25 {
        stones = blink(stones);
    }
    assert_eq!(stones.values().sum::<u64>(), 55312);
}

fn main() {
    let mut stones = parse_stones(include_str!("../input.txt")).unwrap();
    for _n in 0..25 {
        stones = blink(stones);
    }
    let part1 = stones.values().sum::<u64>();
    println!("Part 1: {part1}");
    for _n in 25..75 {
        stones = blink(stones);
    }
    let part2 = stones.values().sum::<u64>();
    println!("Part 2: {part2}");
}
