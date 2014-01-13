import sys
import nose

argv = sys.argv[:]
argv.insert(1, "-vs")
nose.main(argv=argv)
