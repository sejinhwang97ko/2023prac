def custom_mean(*args):
    #print(len(args))
    sumv = 0
    for i in args:
        #print(i)
        sumv += i
    return sumv / len(args)

def custom_max(*_list):
    result = _list[0]

    for i in _list:
        if result < i:
            result = i

    return result