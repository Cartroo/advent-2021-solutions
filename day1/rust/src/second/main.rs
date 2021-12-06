use std::collections::VecDeque;
use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();

    let mut window: VecDeque<i32> = VecDeque::new();
    let mut increment_count = 0;

    // Use fact that (b+c+d > a+b+c) is equivalent to (d > a)
    while let Some(line) = lines.next() {
        let value: i32 = line.unwrap().trim().parse().unwrap();
        if window.len() > 2 {
            let old_value = window.pop_front();
            if let Some(old) = old_value {
                if value > old {
                    increment_count += 1;
                }
            }
        }
        window.push_back(value);
    }
    println!("{}", increment_count);
}

