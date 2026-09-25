from flask import Flask, render_template, request, redirect

app = Flask(__name__)

employees = [
    {"id": 1, "name": "Shiva", "role": "DevOps Engineer"},
    {"id": 2, "name": "Rahul", "role": "Developer"}
]


@app.route("/")
def home():
    search = request.args.get("search", "").strip()

    if search:
        filtered_employees = [
            employee for employee in employees
            if search.lower() in employee["name"].lower()
        ]
    else:
        filtered_employees = employees

    return render_template(
        "index.html",
        employees=filtered_employees,
        search=search
    )


@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        name = request.form["name"]
        role = request.form["role"]

        new_id = len(employees) + 1

        employees.append({
            "id": new_id,
            "name": name,
            "role": role
        })

        return redirect("/")

    return render_template("add_employee.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
