import json
import random
import argparse
import string


def generate_id(prefix, index, pad=3):
    return f"{prefix}{str(index).zfill(pad)}"


def generate_data(num_students=100, num_schools=10, max_prefs=7, capacity_range=(5, 20)):
    student_ids = [generate_id("s", i) for i in range(num_students)]
    school_ids = [generate_id("sch", i) for i in range(num_schools)]

    students = {}
    schools = {school: [] for school in school_ids}
    capacities = {school: random.randint(*capacity_range) for school in school_ids}

    for student in student_ids:
        prefs = random.sample(school_ids, k=min(max_prefs, len(school_ids)))
        students[student] = prefs
        for school in prefs:
            schools[school].append(student)

    return {
        "students": students,
        "schools": schools,
        "capacity": capacities
    }


def main():
    parser = argparse.ArgumentParser(description="Generate student-school preference data as JSON.")
    parser.add_argument("--students", type=int, default=100, help="Number of students to generate.")
    parser.add_argument("--schools", type=int, default=10, help="Number of schools to generate.")
    parser.add_argument("--max_prefs", type=int, default=7, help="Maximum number of preferences per student.")
    parser.add_argument("--min_capacity", type=int, default=5, help="Minimum capacity of each school.")
    parser.add_argument("--max_capacity", type=int, default=20, help="Maximum capacity of each school.")
    parser.add_argument("--output", type=str, default="data.json", help="Output file name.")

    args = parser.parse_args()

    data = generate_data(
        num_students=args.students,
        num_schools=args.schools,
        max_prefs=args.max_prefs,
        capacity_range=(args.min_capacity, args.max_capacity)
    )

    with open(args.output, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Generated data saved to {args.output}")


if __name__ == "__main__":
    main()
