// Сгенерировано компилятором Сибиряк → Rust
#![allow(non_snake_case, non_camel_case_types, unused_variables, dead_code, unused_mut)]
#![allow(unused_imports, clippy::all)]

use std::io::{self, Write};
use std::fmt;
use std::collections::HashMap;

// ─── Рантайм Сибиряк ────────────────────────────────────────────────────────

/// Динамический срез (аналог Go slice)
#[derive(Clone, Debug)]
pub struct Срез<T: Clone> {
    данные: Vec<T>,
}

impl<T: Clone> Срез<T> {
    pub fn новый() -> Self { Срез { данные: Vec::new() } }
    pub fn с_ёмкостью(ёмкость: usize) -> Self { Срез { данные: Vec::with_capacity(ёмкость) } }
    pub fn длина(&self) -> i64 { self.данные.len() as i64 }
    pub fn ёмкость(&self) -> i64 { self.данные.capacity() as i64 }
    pub fn добавить(&mut self, эл: T) { self.данные.push(эл); }
    pub fn получить(&self, i: i64) -> &T { &self.данные[i as usize] }
    pub fn установить(&mut self, i: i64, v: T) { self.данные[i as usize] = v; }
    pub fn срез(&self, от: i64, до: i64) -> Срез<T> {
        Срез { данные: self.данные[от as usize..до as usize].to_vec() }
    }
}

impl<T: Clone + fmt::Display> fmt::Display for Срез<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[")?;
        for (i, v) in self.данные.iter().enumerate() {
            if i > 0 { write!(f, " ")?; }
            write!(f, "{}", v)?;
        }
        write!(f, "]")
    }
}

/// Паника — аварийный выход
#[cold]
pub fn паника(сообщение: &str) -> ! {
    eprintln!("паника: {}", сообщение);
    std::process::exit(1);
}

/// Печать без форматирования (аналог fmt.Println)
macro_rules! печать {
    () => { println!() };
    ($($arg:tt)*) => { println!("{}", format!($($arg)*)) };
}

/// Форматированная печать (аналог fmt.Printf)
macro_rules! печатьф {
    ($fmt:expr $(, $arg:expr)*) => {
        print!($fmt $(, $arg)*);
        let _ = io::stdout().flush();
    };
}

/// Печать в stderr
macro_rules! печатьс {
    ($fmt:expr $(, $arg:expr)*) => { eprint!($fmt $(, $arg)*); };
}

// ─── Встроенные функции ─────────────────────────────────────────────────────

fn длина_строки(с: &str) -> i64 { с.chars().count() as i64 }


fn main() {
}

