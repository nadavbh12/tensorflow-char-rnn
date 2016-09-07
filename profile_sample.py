import cProfile
# import sys
import sample_jazz

if __name__ == '__main__':
    import sys
    cProfile.run(sample_jazz.main(sys.argv[1:]))
