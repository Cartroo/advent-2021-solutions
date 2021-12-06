use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();

    let mut last_value = None;
    let mut increment_count = 0;
    while let Some(line) = lines.next() {
        let value: i32 = line.unwrap().trim().parse().unwrap();
        if let Some(prev) = last_value {
            if value > prev {
                increment_count += 1;
            }
        }
        last_value = Some(value);
    }
    println!("{}", increment_count);
}

