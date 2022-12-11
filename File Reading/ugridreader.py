import vtk
import subprocess
import matplotlib.pyplot as plt
import time

def run_tachyon(folder, input_file, input_type, input_dim, cancel_param, simplify_param : tuple, output_file):
    """Runs tachyon to create vtk file."""

    try:
        subprocess.run([folder + "/tachyon",
                         "-in", input_file,
                         "-type", input_type,
                         "-dim", input_dim[0], input_dim[1], input_dim[2],
                         "-bundle",
                         "-cancel", cancel_param,
                         "-simplify", simplify_param[0], simplify_param[1],
                         "-out", output_file])
    except Exception as e:
        print(e)


def read_file(filename):
    """Reads a unsctructured grid file and returns the grid data."""

    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()

    # print metadata
    print("There are %d points." % reader.GetOutput().GetNumberOfPoints())
    print("There are %d cells." % reader.GetOutput().GetNumberOfCells())

    print("----------------------------")

    # point data
    point_data = reader.GetOutput().GetPointData()
    print("There are %d point arrays." % point_data.GetNumberOfArrays())
    for i in range(point_data.GetNumberOfArrays()):
        print("Array %d is named %s." % (i, point_data.GetArrayName(i)))

    # get MorseIndex array
    morse_index_array = point_data.GetArray("MorseIndex")
    print("MorseIndex array has %d tuples." % morse_index_array.GetNumberOfTuples())

    critical_points_indexes = [i for i in range(-1, 4)]
    print("Critical points indexes: %s" % critical_points_indexes)
    dict_critical_points = {i: [] for i in critical_points_indexes}
    for i in range(morse_index_array.GetNumberOfTuples()):
        dict_critical_points[morse_index_array.GetTuple1(i)].append(i)

    # print dict_critical_points
    for key, value in dict_critical_points.items():
        print("There are %d points with MorseIndex = %d." % (len(value), key))
    
    # print key == 3, values
    print("There are %d points with MorseIndex = %d." % (len(dict_critical_points[3]), 3))
    print(dict_critical_points[3])


    # FunctionVals array
    function_vals_array = point_data.GetArray("FunctionVals")
    # survivingCP array
    surviving_cp_status_array = point_data.GetArray("survivingCP")
    dead_cp3_array = []
    dead_cp2_array = []

    # iterate over all survivingCP values == 1
    dead_cp3_func_vals = []
    dead_cp2_func_vals = []
    for i in range(surviving_cp_status_array.GetNumberOfTuples()):
        if surviving_cp_status_array.GetTuple1(i) == 0 and morse_index_array.GetTuple1(i) == 3:
            # print("Function value at point %d is %f." % (i, function_vals_array.GetTuple1(i)))
            dead_cp3_func_vals.append(function_vals_array.GetTuple1(i))
            dead_cp3_array.append(i)
        elif surviving_cp_status_array.GetTuple1(i) == 0 and morse_index_array.GetTuple1(i) == 2:
            dead_cp2_func_vals.append(function_vals_array.GetTuple1(i))
            dead_cp2_array.append(i)
    
    print("There are %d dead critical points(3)" % len(dead_cp3_func_vals))
    print("dead critical points(3) : %s" % dead_cp3_array)

    print("There are %d dead critical points(2)" % len(dead_cp2_func_vals))
    print("dead critical points(2) : %s" % dead_cp2_array)

    # # plot cummalative line plot
    # sorted(surv_func_vals).reverse()
    # plt.plot(range(len(surv_func_vals)), surv_func_vals)
    # plt.xlabel("Persistence")
    # plt.ylabel("Survived critical points")
    # plt.title("Persistence curve")
    # plt.savefig("persistence_curve.png")

    print("----------------------------")

    cp_pairs = {k : set() for k in dict_critical_points[3]}


    # cell data
    cell_data = reader.GetOutput().GetCellData()
    print("There are %d cell arrays." % cell_data.GetNumberOfArrays())
    for i in range(cell_data.GetNumberOfArrays()):

        # print("=====================================")

        print("Array %d is named %s." % (i, cell_data.GetArrayName(i)))

        cell_data_array = cell_data.GetArray(i)
        print("Array %d has %d tuples." % (i, cell_data_array.GetNumberOfTuples()))

        # print("=====================================")
    
    # DestinationExtremum array
    destination_extremum_array = cell_data.GetArray("DestinationExtremum")

    # SourceSaddle array
    source_saddle_array = cell_data.GetArray("SourceSaddle")

    # print function values of dead critical points
    # print("Function values of dead critical points(3) : %s" % dead_cp3_func_vals)
    # print("Function values of dead critical points(2) : %s" % dead_cp2_func_vals)

    for i in range(destination_extremum_array.GetNumberOfTuples()):
        if destination_extremum_array.GetTuple1(i) in dead_cp3_array and source_saddle_array.GetTuple1(i) in dead_cp2_array:
            cp_pairs[source_saddle_array.GetTuple1(i)].add(destination_extremum_array.GetTuple1(i))

    print("Critical point pairs : %s" % cp_pairs)




if __name__ == "__main__":

    start_time = time.time()

    # run tachyon
    run_tachyon("/home/rathoddinesh/Bit Repos/tachyon/build_cpu",
                "/home/rathoddinesh/Bit Repos/morsegram/ChamferDistance/chamf_distance_Steel_Deposition_181_176_251.raw",
                "f32",
                ("251", "176", "181"),
                "1.0",
                ("0.05", "0.95"),
                "/home/rathoddinesh/Bit Repos/tachyon/build_cpu/steel.vtp")

    end_time = time.time()
    print("Time taken to run tachyon: %f seconds" % (end_time - start_time))


    # read_file("/home/rathoddinesh/Bit Repos/tachyon/build_cpu/steel.vtp")