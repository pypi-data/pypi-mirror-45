use nested_intervals::{IntervalSet, NestedIntervalError};
use pyo3::exceptions;
use pyo3::prelude::*;
use pyo3::class::PyObjectProtocol;
use pyo3::types::PyType;
use pyo3::Py;
mod numpy;
use numpy::numpy_from_vec_u32;
use std::collections::HashSet;

#[pyclass(name=IntervalSet)]
struct PyIntervalSet {
    inner: IntervalSet,
}

struct TupleResult<T> {
    pub inner: Vec<T>,
}

impl<T> TupleResult<T> {
    fn new() -> TupleResult<T> {
        TupleResult::<T> {
            inner: Vec::<T>::new(),
        }
    }
}

impl IntoPyObject for TupleResult<(u32, u32, Vec<u32>)> {
    fn into_object(self, py: Python) -> PyObject {
        self.inner.into_object(py)
    }
}
impl IntoPyObject for TupleResult<(u32, u32, u32)> {
    fn into_object(self, py: Python) -> PyObject {
        self.inner.into_object(py)
    }
}
impl IntoPyObject for TupleResult<(u32, u32)> {
    fn into_object(self, py: Python) -> PyObject {
        self.inner.into_object(py)
    }
}

#[pyproto]
    impl<'p> PyObjectProtocol<'p> for PyIntervalSet {
        fn __str__(&self) -> PyResult<String> {
            Ok(format!("IntervalSet(with {} intervals)",self.inner.len()))
        }
        /*fn __repr__(&self) -> PyResult<String> {
            Ok(format!("{:?}", ZZZ))
        }
        */
    }

/// Helper for returning interval sets as python objects
fn return_interval_set(py: Python, iv: IntervalSet) -> PyResult<Py<PyIntervalSet>> {
    let obj = Py::new(py, PyIntervalSet { inner: iv }).unwrap();
    Ok(obj)
}

fn adapt_error<T>(input: Result<T, NestedIntervalError>) -> Result<T, PyErr> {
    match input {
        Ok(x) => Ok(x),
        Err(x) => 
                Err(PyErr::new::<exceptions::ValueError, _>(format!("{:?}", x)))
    }
}

#[pymethods]
impl PyIntervalSet {
    /// Create an IntervalSet from a list of tuples (start, stop)
    ///
    /// Example:
    /// IntervalSet.from_tuples([(0,10), (30, 40)]
    #[classmethod]
    pub fn from_tuples(_cls: &PyType, tups: Vec<(u32, u32)>) -> PyResult<Py<PyIntervalSet>> {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let mut intervals = Vec::new();
        for tup in tups.iter() {
            if tup.0 > tup.1 {
                return Err(PyErr::new::<exceptions::ValueError, _>("Negative interval"));
            }
            intervals.push(tup.0..tup.1);
        }
        return_interval_set(py, adapt_error(IntervalSet::new(&intervals))?)
    }

    /// Create an IntervalSet from a list of tuples (start, stop, id (integer))
    ///
    /// Example:
    /// IntervalSet.from_tuples_with_id([(0,10,0), (30, 40, 2)]
    #[classmethod]
    pub fn from_tuples_with_id(
        _cls: &PyType,
        tups: Vec<(u32, u32, u32)>,
    ) -> PyResult<Py<PyIntervalSet>> {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let mut intervals = Vec::new();
        let mut ids = Vec::new();
        for tup in tups.iter() {
            if tup.0 > tup.1 {
                return Err(PyErr::new::<exceptions::ValueError, _>("Negative interval"));
            }
            intervals.push(tup.0..tup.1);
            ids.push(tup.2);
        }
        return_interval_set(py, adapt_error(IntervalSet::new_with_ids(&intervals, &ids))?)
    }

    /// Convert an IntervalSet into a list of tuples (start, stop, [ids])
    pub fn to_tuples(&self, py: Python) -> PyResult<PyObject> {
        let mut res: TupleResult<(u32, u32)> = TupleResult::new();
        for (iv, _ids) in self.inner.iter() {
            let tup = (iv.start, iv.end);
            res.inner.push(tup);
        }
        Ok(res.into_object(py))
    }
    ///
    /// Convert an IntervalSet into a list of tuples (start, stop, [ids])
    pub fn to_tuples_with_id(&self, py: Python) -> PyResult<PyObject> {
        let mut res: TupleResult<(u32, u32, Vec<u32>)> = TupleResult::new();
        for (iv, ids) in self.inner.iter() {
            let tup = (iv.start, iv.end, ids.clone());
            res.inner.push(tup);
        }
        Ok(res.into_object(py))
    }

    /// Convert an IntervalSet into a list of tuples (start, stop, first_id)
    ///
    /// Since many interval operations like filtering don't actually
    /// produce intervals with more than one associated id, this
    /// is a convenient way to go back to just integers
    pub fn to_tuples_first_id(&self, py: Python) -> PyResult<PyObject> {
        let mut res: TupleResult<(u32, u32, u32)> = TupleResult::new();
        for (iv, ids) in self.inner.iter() {
            let tup = (
                iv.start,
                iv.end,
                ids.iter()
                    .next()
                    .and_then(|i| Some(*i))
                    .ok_or(PyErr::new::<exceptions::ValueError, _>("Empty ids"))?,
            );
            res.inner.push(tup);
        }
        Ok(res.into_object(py))
    }
    /// Convert an IntervalSet into just the (unique) ids referenced
    ///
    pub fn to_ids(&self) -> PyResult<Vec<u32>> {
        let result: HashSet<u32> = self.inner.iter().map(|(_iv, ids) | ids).flatten().map(|x| *x).collect();
        let result = result.iter().map(|x| *x).collect();
        Ok(result)
    }
    

    /// Convert an IntervalSet into a list of tuples (start, stop, last_id)
    ///
    /// Since many interval operations like filtering don't actually
    /// produce intervals with more than one associated id, this
    /// is a convenient way to go back to just integers
    pub fn to_tuples_last_id(&self, py: Python) -> PyResult<PyObject> {
        let mut res: TupleResult<(u32, u32, u32)> = TupleResult::new();
        for (iv, ids) in self.inner.iter() {
            let tup = (
                iv.start,
                iv.end,
                ids.iter()
                    .last()
                    .and_then(|i| Some(*i))
                    .ok_or(PyErr::new::<exceptions::ValueError, _>("Empty ids"))?,
            );
            res.inner.push(tup);
        }
        Ok(res.into_object(py))
    }

    /// Convert an IntervalSet into a tuple of lists ([starts], [stops], [[ids]])
    pub fn to_lists(&self, py: Python) -> PyResult<PyObject> {
        let mut out_starts: Vec<u32> = Vec::new();
        let mut out_stops: Vec<u32> = Vec::new();
        let mut out_ids: Vec<Vec<u32>> = Vec::new();
        for (iv, ids) in self.inner.iter() {
            out_starts.push(iv.start);
            out_stops.push(iv.end);
            out_ids.push(ids.clone());
        }
        Ok((out_starts, out_stops, out_ids).into_object(py))
    }

    /// Convert an IntervalSet into a tuple of lists ([starts], [stops], [first_ids])
    ///
    /// Since many interval operations like filtering don't actually
    /// produce intervals with more than one associated id, this
    /// is a convenient way to go back to just integers

    pub fn to_lists_first_id(&self, py: Python) -> PyResult<PyObject> {
        let mut out_starts: Vec<u32> = Vec::new();
        let mut out_stops: Vec<u32> = Vec::new();
        let mut out_ids: Vec<u32> = Vec::new();
        for (iv, ids) in self.inner.iter() {
            out_starts.push(iv.start);
            out_stops.push(iv.end);
            out_ids.push(
                ids.iter()
                    .next()
                    .and_then(|i| Some(*i))
                    .ok_or(PyErr::new::<exceptions::ValueError, _>("Empty ids"))?,
            );
        }
        Ok((out_starts, out_stops, out_ids).into_object(py))
    }
    /// Convert an IntervalSet into a tuple of (array(starts), array(stops))
    pub fn to_numpy(&self, py: Python) -> PyResult<PyObject> {
        let mut out_starts: Vec<u32> = Vec::new();
        let mut out_stops: Vec<u32> = Vec::new();
        for (iv, _ids) in self.inner.iter() {
            out_starts.push(iv.start);
            out_stops.push(iv.end);
        }
        Ok((
            numpy_from_vec_u32(out_starts)?,
            numpy_from_vec_u32(out_stops)?,
        )
            .into_object(py))
    }

    /// Convert an IntervalSet into a tuple of (array(starts), array(stops), [[ids]])
    pub fn to_numpy_with_id(&self, py: Python) -> PyResult<PyObject> {
        let mut out_starts: Vec<u32> = Vec::new();
        let mut out_stops: Vec<u32> = Vec::new();
        let mut out_ids: Vec<Vec<u32>> = Vec::new();
        for (iv, ids) in self.inner.iter() {
            out_starts.push(iv.start);
            out_stops.push(iv.end);
            out_ids.push(ids.clone());
        }
        Ok((
            numpy_from_vec_u32(out_starts)?,
            numpy_from_vec_u32(out_stops)?,
            out_ids.into_object(py),
        )
            .into_object(py))
    }

    /// Convert an IntervalSet into a tuple of numpy.u32 arrays (start, stops, first_ids)
    ///
    /// Since many interval operations like filtering don't actually
    /// produce intervals with more than one associated id, this
    /// is a convenient way to go back to just integers

    pub fn to_numpy_first_id(&self, py: Python) -> PyResult<PyObject> {
        let mut out_starts: Vec<u32> = Vec::new();
        let mut out_stops: Vec<u32> = Vec::new();
        let mut out_ids: Vec<u32> = Vec::new();
        for (iv, ids) in self.inner.iter() {
            out_starts.push(iv.start);
            out_stops.push(iv.end);
            out_ids.push(
                ids.iter()
                    .next()
                    .and_then(|i| Some(*i))
                    .ok_or(PyErr::new::<exceptions::ValueError, _>("Empty ids"))?,
            );
        }
        Ok((
            numpy_from_vec_u32(out_starts)?,
            numpy_from_vec_u32(out_stops)?,
            numpy_from_vec_u32(out_ids)?,
        )
            .into_object(py))
    }

    pub fn invert(
        &self,
        py: Python,
        lower_bound: u32,
        upper_bound: u32,
    ) -> PyResult<Py<PyIntervalSet>> {
        let iv = self.inner.invert(lower_bound, upper_bound);
        return_interval_set(py, iv)
    }

    pub fn merge_hull(&self, py: Python) -> PyResult<Py<PyIntervalSet>> {
        return_interval_set(py, self.inner.merge_hull())
    }

    pub fn merge_connected(&self, py: Python) -> PyResult<Py<PyIntervalSet>> {
        return_interval_set(py, self.inner.merge_connected())
    }
    pub fn merge_drop(&self, py: Python) -> PyResult<Py<PyIntervalSet>> {
        return_interval_set(py, self.inner.merge_drop())
    }
    pub fn merge_split(&mut self, py: Python) -> PyResult<Py<PyIntervalSet>> {
        return_interval_set(py, self.inner.merge_split())
    }

    pub fn remove_duplicates(&self, py: Python) -> PyResult<Py<PyIntervalSet>> {
        return_interval_set(py, self.inner.remove_duplicates())
    }

    pub fn any_overlapping(&self) -> PyResult<bool> {
        Ok(self.inner.any_overlapping())
    }

    pub fn overlap_status(&self) -> PyResult<Vec<bool>> {
        Ok(self.inner.overlap_status())
    }

    pub fn has_overlap(&mut self, start: u32, end: u32) -> PyResult<bool> {
        Ok(adapt_error(self.inner.has_overlap(&(start..end)))?)
    }

    pub fn get_overlap(&mut self, py: Python, start: u32, end: u32) -> PyResult<Py<PyIntervalSet>> {
        return_interval_set(py, self.inner.query_overlapping(&(start..end)))
    }

    pub fn find_closest_start(&mut self, pos: u32) -> PyResult<Option<(u32, u32, Vec<u32>)>> {
        let found = self.inner.find_closest_start(pos);
        Ok(match found {
            Some((interval, ids)) => Some((interval.start, interval.end, ids)),
            None => None,
        })
    }
    
}

/// Wrapper around nested intervals
#[pymodule]
fn mbf_nested_intervals(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyIntervalSet>()?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;

    Ok(())
}
