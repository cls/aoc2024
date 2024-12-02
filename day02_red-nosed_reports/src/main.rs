use nom::{
    character::complete::{newline, space1, u32},
    combinator::all_consuming,
    error::Error,
    multi::{many1, separated_list1},
    sequence::terminated,
    Err,
};

fn parse_reports(input: &str) -> Result<Vec<Vec<u32>>, Err<Error<&str>>> {
    let (_eof, reports) = all_consuming(many1(terminated(separated_list1(space1, u32), newline)))(input)?;
    Ok(reports)
}

#[test]
fn parse_example() {
    let reports = parse_reports(include_str!("../example.txt")).unwrap();
    assert_eq!(reports, [
        [7, 6, 4, 2, 1],
        [1, 2, 7, 8, 9],
        [9, 7, 6, 2, 1],
        [1, 3, 2, 4, 5],
        [8, 6, 4, 4, 1],
        [1, 3, 6, 7, 9],
    ]);
}

#[derive(Debug, PartialEq)]
enum Safe {
    NoDataPoints,
    OneDataPoint(u32),
    Increasing(u32),
    Decreasing(u32),
}

#[derive(Debug, PartialEq)]
enum Unsafe {
    IncreaseOf(u32),
    DecreaseOf(u32),
    NeitherIncreaseNorDecrease(u32),
    IncreasingThenDecreasing(u32, u32),
    DecreasingThenIncreasing(u32, u32),
}

fn safety_check_update(prev_status: &Safe, curr_value: u32) -> Result<Safe, Unsafe> {
    let prev_status_value = match prev_status {
        Safe::NoDataPoints => None,
        Safe::OneDataPoint(x) => Some(x),
        Safe::Increasing(x) => Some(x),
        Safe::Decreasing(x) => Some(x),
    };
    if let Some(&prev_value) = prev_status_value {
        let curr_status = if prev_value > curr_value {
            if prev_value <= curr_value + 3 {
                Ok(Safe::Decreasing(curr_value))
            } else {
                Err(Unsafe::DecreaseOf(prev_value - curr_value))
            }
        } else if curr_value > prev_value {
            if curr_value <= prev_value + 3 {
                Ok(Safe::Increasing(curr_value))
            } else {
                Err(Unsafe::IncreaseOf(curr_value - prev_value))
            }
        } else {
            Err(Unsafe::NeitherIncreaseNorDecrease(curr_value))
        }?;
        match (prev_status, curr_status) {
            (Safe::Increasing(x), Safe::Decreasing(y)) => Err(Unsafe::IncreasingThenDecreasing(*x, y)),
            (Safe::Decreasing(x), Safe::Increasing(y)) => Err(Unsafe::DecreasingThenIncreasing(*x, y)),
            (_, status) => Ok(status),
        }
    } else {
        Ok(Safe::OneDataPoint(curr_value))
    }
}

fn safety_check(report: &[u32]) -> Result<Safe, Unsafe> {
    report.iter().fold(Ok(Safe::NoDataPoints), |overall_status, &value| overall_status.and_then(|prev_status| safety_check_update(&prev_status, value)))
}

#[test]
fn test_safety_check() {
    let reports = parse_reports(include_str!("../example.txt")).unwrap();
    let results = reports.iter().map(|report| safety_check(report)).collect::<Vec<_>>();
    assert_eq!(results, [
        Ok(Safe::Decreasing(1)),
        Err(Unsafe::IncreaseOf(5)),
        Err(Unsafe::DecreaseOf(4)),
        Err(Unsafe::IncreasingThenDecreasing(3, 2)),
        Err(Unsafe::NeitherIncreaseNorDecrease(4)),
        Ok(Safe::Increasing(9)),
    ]);
}

fn do_part1(input: &str) -> usize {
    let reports = parse_reports(input).unwrap();
    reports.iter().filter(|report| safety_check(report).is_ok()).count()
}

#[test]
fn part1_example() {
    let safe_count = do_part1(include_str!("../example.txt"));
    assert_eq!(safe_count, 2);
}

fn main() {
    let input = include_str!("../input.txt");
    let part1 = do_part1(input);
    println!("Part 1: {part1}");
}
