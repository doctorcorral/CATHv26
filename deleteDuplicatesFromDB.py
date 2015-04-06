import sys


def main():
    fin = open(sys.argv[1])

    already = set()

    for l in fin:
        l = l.strip().split(',')
        domname, vector, clase = l[0], l[1:-1], l[-1]

        if domname in already: continue

        print "%s,%s,%s" % (domname,','.join(vector),clase)
        already.add(domname)

if __name__ == '__main__':
    main()
