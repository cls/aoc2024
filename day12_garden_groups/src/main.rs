use ndarray::{Array2, Dim, Dimension, Ix2, ShapeError, arr2};

struct Garden {
    plants: Array2<char>
}

#[derive(Debug)]
enum InputError {
    Empty,
    Ragged,
    #[allow(dead_code)]
    Shape(ShapeError),
}

impl Garden {
    pub fn parse(input: &str) -> Result<Self, InputError> {
        let mut expected_width = None;
        let mut vec = Vec::new();
        for line in input.lines() {
            let len = line.len();
            if *expected_width.get_or_insert(len) != len {
                return Err(InputError::Ragged)
            }
            vec.extend(line.chars())
        }
        let width = expected_width.ok_or(InputError::Empty)?;
        let shape = (width, vec.len() / width);
        let plants = Array2::from_shape_vec(shape, vec).map_err(|err| InputError::Shape(err))?;
        Ok(Self{plants})
    }

    pub fn raw_dim(&self) -> Ix2 {
        self.plants.raw_dim()
    }
}

#[test]
fn parse_example1() {
    let garden = Garden::parse(include_str!("../example1.txt")).unwrap();
    let mut fencing = Fencing::new(garden.raw_dim());
    fencing.fence(&garden);
    assert_eq!(garden.plants, arr2(&[['A', 'A', 'A', 'A'],
                                     ['B', 'B', 'C', 'D'],
                                     ['B', 'B', 'C', 'C'],
                                     ['E', 'E', 'E', 'C']]));
}

struct Plot {
    parent: Ix2,
    area: usize,
    perimeter: usize,
}

impl Plot {
    pub fn new(pos: Ix2) -> Self {
        Self{parent: pos, area: 1, perimeter: 4}
    }

    pub fn price(&self) -> usize {
        self.area * self.perimeter
    }
}

struct Fencing {
    plots: Array2<Plot>,
}

impl Fencing {
    pub fn new(shape: Ix2) -> Self {
        Self{plots: Array2::from_shape_fn(shape, |pos| Plot::new(Dim(pos)))}
    }

    pub fn fence(&mut self, garden: &Garden) {
        for ((x, y), plant) in garden.plants.indexed_iter() {
            let &[w, h] = self.plots.shape() else { panic!("Unexpected shape") };
            Self::visit_neighbours((x, y), (w, h), |neighbour| {
                if plant == garden.plants.get(neighbour).unwrap() {
                    self.merge_plots(Dim((x, y)), neighbour);
                }
            })
        }
    }

    pub fn total_price(&self) -> usize {
        let mut price = 0;
        for ((x, y), plot) in self.plots.indexed_iter() {
            if plot.parent == Dim((x, y)) {
                price += plot.price();
            }
        }
        price
    }

    fn visit_neighbours<F>((x, y): (usize, usize), (w, h): (usize, usize), mut f: F) where F: FnMut(Ix2) {
        if x > 0 {
            f(Dim((x-1, y)))
        }
        if y > 0 {
            f(Dim((x, y-1)))
        }
        if x+1 < w {
            f(Dim((x+1, y)))
        }
        if y+1 < h {
            f(Dim((x, y+1)))
        }
    }

    fn find_root(&self, mut pos: Ix2) -> Option<(Ix2, usize)> {
        loop {
            let plot = self.plots.get(pos)?;
            if pos == plot.parent {
                return Some((pos, plot.area))
            }
            pos = plot.parent
        }
    }

    fn merge_plots(&mut self, pos1: Ix2, pos2: Ix2) {
        let (root1, size1) = self.find_root(pos1).unwrap();
        let (root2, size2) = self.find_root(pos2).unwrap();
        if root1 == root2 {
            return
        }
        if size1 >= size2 {
            self.merge_plot_roots(root1, root2, pos2)
        } else {
            self.merge_plot_roots(root2, root1, pos1)
        }
    }

    fn merge_plot_roots(&mut self, root1: Ix2, root2: Ix2, pos: Ix2) {
        let (x, y) = pos.into_pattern();
        let &[w, h] = self.plots.shape() else { panic!("Unexpected shape") };
        let mut shared_perimeter = 0;
        Self::visit_neighbours((x, y), (w, h), |neighbour| {
            let (neighbour_root, _neighbour_size) = self.find_root(neighbour).unwrap();
            if neighbour_root == root1 {
                shared_perimeter += 2;
            }
        });
        let plot2 = self.plots.get_mut(root2).unwrap();
        plot2.parent = root1;
        let area2 = plot2.area;
        let perimeter2 = plot2.perimeter;
        let plot1 = self.plots.get_mut(root1).unwrap();
        plot1.area += area2;
        plot1.perimeter += perimeter2 - shared_perimeter;
    }
}

#[test]
fn fence_example1() {
    let garden = Garden::parse(include_str!("../example1.txt")).unwrap();
    let mut fencing = Fencing::new(garden.raw_dim());
    fencing.fence(&garden);
    assert_eq!(fencing.total_price(), 140);
}

#[test]
fn fence_example2() {
    let garden = Garden::parse(include_str!("../example2.txt")).unwrap();
    let mut fencing = Fencing::new(garden.raw_dim());
    fencing.fence(&garden);
    assert_eq!(fencing.total_price(), 772);
}

#[test]
fn fence_example3() {
    let garden = Garden::parse(include_str!("../example3.txt")).unwrap();
    let mut fencing = Fencing::new(garden.raw_dim());
    fencing.fence(&garden);
    assert_eq!(fencing.total_price(), 1930);
}

fn main() {
    let garden = Garden::parse(include_str!("../input.txt")).unwrap();
    let mut fencing = Fencing::new(garden.raw_dim());
    fencing.fence(&garden);
    let part1 = fencing.total_price();
    println!("Part 1: {part1}");
}
