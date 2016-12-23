examp_path = r'example.in'
small_path = r'B-small-practice.in'
large_path = r'B-large-practice.in'

def out(a, print_indices=True):
    for i in xrange(len(a)):
        if print_indices:
            print str(i) + ":\t" + str(a[i])
        else:
            print a[i]


def parse_customer(in_s, N):
    """
    :param in_s:
    :param N:
    :return: if a free costumer - returns None. else - tuple of unmelted set + melted index / None
    """
    cost_data = [int(s) for s in in_s.split(" ")]
    T = cost_data[0]
    unmelted_set = set()
    melted = None
    for i in xrange(T):
        x = cost_data[1 + 2 * i]
        y = cost_data[1 + 2 * i + 1]
        if (x in unmelted_set) or (x == melted):
            # x appears twice
            return None
        if y == 1:
            melted = x
        else:
            unmelted_set.add(x)
    return (unmelted_set, melted)


def parse(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    res = []
    C = int(lines[0])
    line_index = 1
    for t in xrange(C):
        cust_data = []
        N = int(lines[line_index])
        line_index += 1
        M = int(lines[line_index])
        line_index += 1
        for i in xrange(M):
            tmp_cust = parse_customer(lines[line_index], N)
            if tmp_cust is not None:
                cust_data.append(tmp_cust)
            line_index += 1
        res.append((N,M,cust_data))
    return res


def check_customer(unmelted_set, melted, cur_batches):
    """
    :param cust_data:
    :param cur_batches:
    :return: True if costumer is happy, false otherwise
    """
    # check first the melted:
    if (melted is not None) and (cur_batches[melted] == 1):
        return True
    # now check the unmelted:
    for x in unmelted_set:
        if cur_batches[x] == 0:
            return True
    return False


def test_one_set(in_data):
    N = in_data[0]
    M = in_data[1]
    cust_datas = in_data[2]
    cur_batches = [0] * (N+1)
    batches_changed = True
    while batches_changed:
        batches_changed = False
        for unmelted_set, melted in cust_datas:
            cust_happy = check_customer(unmelted_set, melted, cur_batches)
            if not cust_happy:
                if (melted is None) or (cur_batches[melted] == 1):
                    return "IMPOSSIBLE"
                cur_batches[melted] = 1
                batches_changed = True
                break
    return cur_batches[1:]


def do_everything(filename):
    all_sets = parse(filename)
    all_lines = []
    for i, s in enumerate(all_sets):
        tmp_out = "Case #" + str(i+1) + ": "
        tmp_res = test_one_set(s)
        if tmp_res == "IMPOSSIBLE":
            tmp_out += tmp_res
        else:
            for x in tmp_res:
                tmp_out += str(x) + " "
        all_lines.append(tmp_out + "\n")
    f = open(filename[:-2] + "out", 'w')
    f.writelines(all_lines)
    f.close()
