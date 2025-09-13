import streamlit as st
import itertools

st.title("Pipe Cutting Optimization Tool")

# Step 1: Section
section = st.text_input("Under which section you have to cut the pipe:")

# Step 2: Available lengths (floats allowed)
available_lengths = st.text_area("Enter available pipe lengths (comma separated, e.g. 12, 8.5, 6):")
if available_lengths:
    available_lengths = list(map(float, available_lengths.split(",")))
else:
    available_lengths = []

# Step 3: How many pipes to form
num_pipes = st.number_input("How many pipes you have to form (max 4):", min_value=1, max_value=4, step=1)

# Step 4: Required lengths (floats allowed)
required_pipes = []
for i in range(num_pipes):
    length = st.number_input(f"Enter required length for pipe {i+1}:", min_value=0.1, format="%.2f")
    required_pipes.append(length)

# --- Optimization function (all combos with scrap) ---
def find_combinations(available, target):
    solutions = []
    n = len(available)

    for r in range(1, n + 1):
        for combo in itertools.combinations(available, r):
            total = round(sum(combo), 2)  # support floats
            if total >= target:  # must be enough to form required pipe
                scrap = round(total - target, 2)
                normalized = tuple(sorted(combo))  # avoid (6,4) vs (4,6)
                solutions.append((normalized, scrap))

    if not solutions:
        return None

    # Remove duplicates
    solutions = list(set(solutions))

    # Sort by scrap first, then combo
    solutions.sort(key=lambda x: (x[1], x[0]))
    return solutions

# --- Run optimization ---
if st.button("Optimize Cutting"):
    if not available_lengths or not required_pipes:
        st.error("Please enter available lengths and required lengths.")
    else:
        for target in required_pipes:
            st.subheader(f"Required pipe length: {target}")
            results = find_combinations(available_lengths, target)
            if results:
                for combo, scrap in results:
                    st.write(f"Combo: {combo} → Scrap = {scrap}")
            else:
                st.error("No possible combination found.")
