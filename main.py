import subprocess

# List your Python files here in the order you want to run them
python_files = [
    "scr/1webs_finder.py",
    "scr/2cleaner.py",
    "scr/3cleaner2.py",
    "scr/4contact_scraper.py",
    "scr/5final_cleaner.py"
]

for script in python_files:
    print(f"\nRunning: {script}")
    try:
        subprocess.run(["python", script], check=True)
        print(f"Finished: {script}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e}")
        break  # Optional: stop on error
