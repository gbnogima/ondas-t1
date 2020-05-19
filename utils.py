class Utils():
   def print_result(current, voltage):
    print("Corrente: \n")
    for i in current:
        for j in i:
            print("%.5f" % j, end = '    ')
        print("")

    print("\n\nTensão: \n")
    for i in voltage:
        for j in i:
            print("%.5f" % j, end = '    ')
        print("")
