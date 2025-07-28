import time
from extraction import process_all_pdfs  # import from your main extraction module

if __name__ == "__main__":
    start_time = time.time()
    process_all_pdfs(input_dir="input", output_dir="output")
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"\nTotal execution time: {elapsed:.2f} seconds")
