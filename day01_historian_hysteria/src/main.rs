use nom::{
    character::complete::{newline, space1, u32},
    combinator::all_consuming,
    error::Error,
    multi::many1,
    sequence::{separated_pair, terminated},
    Err,
};
use std::collections::HashMap;

fn parse_lists(input: &str) -> Result<(Vec<u32>, Vec<u32>), Err<Error<&str>>> {
    let (_eof, pairs) = all_consuming(many1(terminated(separated_pair(u32, space1, u32), newline)))(input)?;
    Ok(pairs.into_iter().unzip())
}

#[test]
fn parse_example() {
    let (lhs, rhs) = parse_lists(include_str!("../example.txt")).unwrap();
    assert_eq!(lhs, [3, 4, 2, 1, 3, 3]);
    assert_eq!(rhs, [4, 3, 5, 3, 9, 3]);
}

fn do_part1(input: &str) -> u32 {
    let (mut lhs, mut rhs) = parse_lists(input).unwrap();
    lhs.sort();
    rhs.sort();
    let paired_locations = lhs.into_iter().zip(rhs.into_iter());
    let distances = paired_locations.map(|(x, y)| if x > y { x - y } else { y - x });
    distances.sum()
}

#[test]
fn part1_example() {
    let total_distance = do_part1(include_str!("../example.txt"));
    assert_eq!(total_distance, 11);
}

fn do_part2(input: &str) -> u32 {
    let (lhs, rhs) = parse_lists(input).unwrap();
    let mut rhs_counts = HashMap::new();
    for rhs_item in rhs {
        rhs_counts.entry(rhs_item).and_modify(|count| *count += 1).or_insert(1);
    }
    let similarities = lhs.into_iter().map(|x| x * rhs_counts.get(&x).unwrap_or(&0));
    similarities.sum()
}

#[test]
fn part2_example() {
    let total_similarity = do_part2(include_str!("../example.txt"));
    assert_eq!(total_similarity, 31);
}

fn main() {
    let input = include_str!("../input.txt");
    let part1 = do_part1(input);
    println!("Part 1: {part1}");
    let part2 = do_part2(input);
    println!("Part 2: {part2}");
}
