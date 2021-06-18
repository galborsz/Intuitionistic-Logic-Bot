from formula_generation import formula_generator
import time
import globals

def main():
    globals.start_time = time.time()
    formula_generator()
    
if __name__ == '__main__':
    main()