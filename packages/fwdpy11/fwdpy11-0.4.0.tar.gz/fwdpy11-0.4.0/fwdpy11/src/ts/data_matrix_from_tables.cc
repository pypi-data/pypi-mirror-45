#include <fwdpp/ts/generate_data_matrix.hpp>
#include <fwdpy11/types/Population.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MAKE_OPAQUE(std::vector<fwdpy11::Mutation>);

fwdpp::data_matrix
generate_data_matrix(const fwdpp::ts::table_collection& tables,
                     const std::vector<fwdpy11::Mutation>& mutations,
                     const std::vector<fwdpp::ts::TS_NODE_INT>& samples,
                     bool record_neutral, bool record_selected,
                     py::object start, py::object stop)
{
    double b = 0.0;
    double e = tables.genome_length();
    if (!start.is_none())
        {
            b = start.cast<double>();
        }
    if (!stop.is_none())
        {
            e = stop.cast<double>();
        }
    return fwdpp::ts::generate_data_matrix(
        tables, samples, mutations, record_neutral, record_selected, b, e);
}

void
init_data_matrix_from_tables(py::module& m)
{
    m.def("make_data_matrix",
          [](const fwdpy11::Population& pop,
             const std::vector<fwdpp::ts::TS_NODE_INT>& samples,
             const bool record_neutral, const bool record_selected) {
              return fwdpp::ts::generate_data_matrix(
                  pop.tables, samples, pop.mutations, record_neutral,
                  record_selected);
          },
          py::arg("pop"), py::arg("samples"), py::arg("record_neutral"),
          py::arg("record_selected"),
          R"delim(
     Create a :class:`fwdpy11.sampling.DataMatrix` from a table collection.
     
     :param pop: A population
     :type pop: :class:`fwdpy11.Population`
     :param samples: A list of sample nodes
     :type samples: list
     :param record_neutral: If True, generate data for neutral variants
     :type record_neutral: boolean
     :param record_selected: If True, generate data for selected variants
     :type record_selected: boolean

     .. deprecated:: 0.3.0

        Prefer :func:`fwdpy11.ts.data_matrix_from_tables`.
     )delim");

    m.def("data_matrix_from_tables", &generate_data_matrix, py::arg("tables"),
          py::arg("mutations"), py::arg("samples"), py::arg("record_neutral"),
          py::arg("record_selected"), py::arg("begin") = py::none(),
          py::arg("end") = py::none(),
          R"delim(
     Create a :class:`fwdpy11.sampling.DataMatrix` from a table collection.
     
     :param tables: A TableCollection
     :type tables: :class:`fwdpy11.ts.TableCollection`
     :param mutations: Container of mutations
     :type mutations: :class:`fwdpy11.VecMutation`
     :param samples: A list of sample nodes
     :type samples: list or array
     :param record_neutral: If True, generate data for neutral variants
     :type record_neutral: boolean
     :param record_selected: If True, generate data for selected variants
     :type record_selected: boolean
     :param begin: (None) Start of range, inclusive
     :param end: (None) End of range, exclusive

     :rtype: :class:`fwdpy11.sampling.DataMatrix`

     If None is passed in for begin or end, 0 and tables.genome_length are used,
     respectively.

     .. versionadded:: 0.3.0
     )delim");
}
