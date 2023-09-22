import search


def run_test(side_length):
    print("Running for a side length of " + str(side_length))

    total_insert, total_delete, total_depth, total_time, total_timeouts = 0, 0, 0, 0, 0
    denominator = 100  # the number of times we run the program
    for x in range(denominator):
        results = search.search(side_length)

        total_depth += len(results[0][0][1])
        total_insert += results[1]
        total_delete += results[2]
        total_time += results[3]
        if results[3] == 100:
            total_timeouts += 1  # total_timeouts tallies how many times the algorithm times out

    average_insert = total_insert / denominator
    average_delete = total_delete / denominator
    average_depth = total_depth / denominator
    average_time = total_time / denominator

    print("Average depth: " + str(average_depth))
    print("Average inserts: " + str(average_insert))
    print("Average removes: " + str(average_delete))
    print("Average time in seconds: " + str(average_time))
    print("Number of timeouts: " + str(total_timeouts) + "\n")


run_test(2)
run_test(3)
run_test(4)
