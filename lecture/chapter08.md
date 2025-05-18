## **Chapter 8: Interactive ORM with Jupyter & `django-extensions`**

Jupyter Notebooks transform the Python interpreter into an explorable laboratory; `django-extensions` turns the traditional Django shell into a power console that auto-imports every model and helper you own.  Marry the two and you gain an IDE-in-the-browser that speaks SQL-through-Python in real time.  Instead of sprinkling `print()` statements or writing temporary view functions, you can query production-like data, plot histograms, or massage CSV files—all while your normal Django settings (middleware, custom managers, timezone) remain intact.  This chapter demonstrates how to set up a container-safe notebook environment, how `shell_plus --notebook` injects your ORM objects, and how to avoid common pitfalls such as accidental data tampering or exposing the notebook server on the open internet.  By the end, you will be able to run ad-hoc analytics, craft migration prototypes, and even embed Pandas and Matplotlib plots, all without leaving the comfort of your browser.

---

### **1. Theories**

**1.1 Why Interactive Notebooks?**
Classic Django development cycles follow a *code–save–run–refresh* loop.  When the question is purely exploratory—*Which user rented the most bikes last quarter?*—opening Vim, writing a management command, and re-deploying is wasteful.  Jupyter provides an *interactive REPL with memory*: each code cell can be executed, modified, and re-executed in isolation.  Markdown cells allow rich-text explanations, making notebooks both executable scripts and living documentation.  In data science, this paradigm is a given; in web development it remains underutilised even though ORM queries, admin data fixes, and one-time reports benefit just as much.

**1.2 What Is `django-extensions`?**
`django-extensions` is a community package that augments Django’s management command arsenal.  Key commands include:

| Command                                 | Purpose                                                                                              |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `shell_plus`                            | Starts an enhanced shell that auto-imports all models, settings, and selected third-party utilities. |
| `shell_plus --notebook`                 | Boots a Jupyter kernel pre-loaded with the same objects.                                             |
| `runserver_plus`                        | Development server with Werkzeug debugger.                                                           |
| `graph_models`                          | Generates ER diagrams in DOT, PNG, SVG, or PDF formats.                                              |
| `clean_pyc`, `show_urls`, `create_jobs` | Miscellaneous productivity helpers.                                                                  |

Because `shell_plus` introspects `INSTALLED_APPS`, it saves the mental overhead of typing `from catalog.models import Bike` fifty times a day.

**1.3 Jupyter Kernel Lifecycle**
A Jupyter session begins with `python manage.py shell_plus --notebook`.  Behind the curtain, Django initialises settings, connects to the database, *then* hands control to IPython.  Each code cell executes in the same process; variables persist until the kernel is restarted.  This persistence is a double-edged sword: long-lived objects may hold open DB cursors or stale cache data.  Best practice is to restart the kernel after large schema changes or when memory balloons.

**1.4 Security Considerations**
Running `jupyter notebook --ip 0.0.0.0` in production is a career-limiting move.  Notebooks can execute arbitrary shell commands (`!rm -rf /`).  Therefore:

1. Bind to `127.0.0.1` and use SSH port-forwarding if remote access is required.
2. Always set a strong token or password (Jupyter prompts on first launch).
3. Mount production data read-only in staging; never grant write credentials unless absolutely necessary.
4. Put notebooks in `.gitignore`; convert to scripts (`jupyter nbconvert --to script`) for reproducible deployments.

**1.5 ORM Introspection Patterns**
With `shell_plus`, your models appear as bare symbols—`Bike`, `Rental`, `User`.  QuerySets can be chained and profiled on the fly:

```python
%%timeit
Rental.objects.filter(start_time__year=2025).select_related("bike")[:1000]
```

Under IPython, `%timeit` wraps the expression and reports wall-clock mean and standard deviation.  Another gem is the `query` attribute:

```python
qs = Bike.objects.filter(hourly_rate__gt=50)
print(qs.query)
```

This prints raw SQL, enabling DBA-level optimisation discussions without leaving the browser.

**1.6 Bridging Pandas and Django**
Pandas excels at columnar analytics—group-by, pivot, rolling windows—but it speaks NumPy arrays, not QuerySets.  The bridge is `DataFrame.from_records()`:

```python
import pandas as pd
df = pd.DataFrame.from_records(
    Rental.objects.values("bike__name", "total_fee", "start_time")
)
top = (
    df.groupby("bike__name")["total_fee"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)
```

Add `%matplotlib inline` and you can generate a bar chart in two lines.  Because the DataFrame is memory-resident, avoid loading millions of rows; filter in the ORM first.

**1.7 Visualising the Schema**
`graph_models` emits a DOT file, which Graphviz converts to SVG.  Example:

```bash
python manage.py graph_models catalog -o catalog.svg
```

When embedded in a notebook—`from IPython.display import SVG, display`—the ER diagram becomes interactive course material.

**1.8 Docker Integration**
Inside Docker, the typical command is:

```bash
docker compose exec web python manage.py shell_plus --notebook --ip=0.0.0.0 --port=8888 --no-browser
```

Expose port 8888 in `docker-compose.yml`.  Then visit `http://localhost:8888/?token=…`.  Because the container shares the same volume as your code, notebooks are saved alongside source files; but remember that notebook files can balloon with embedded PNGs.

**1.9 Performance Footprint**
Running a Jupyter kernel is no heavier than a `manage.py shell`, but plotting libraries can import huge native extensions (Matplotlib, NumPy).  Keep an eye on container memory; set `mem_limit` in Compose if colleagues share the same host.

**1.10 Beyond the Notebook**
Notebooks are superb for *exploration*; they are poor for *production jobs*.  The mantra: *Exploratory in notebooks, repeatable in scripts*.  Use `nbconvert` to export final analytics into `.py` scripts checked into `/management/commands/`.  Treat the notebook as scaffolding, not the cathedral.


---

### **2. Step-by-Step Workshop**

* **Install packages**

  ```bash
  pip install django-extensions jupyter pandas matplotlib
  ```
* **Enable app** – add `'django_extensions'` to `INSTALLED_APPS` in `settings.py`.
* **Launch notebook**

  ```bash
  python manage.py shell_plus --notebook
  ```
* **Create a new notebook** named **`rental_analytics.ipynb`**.
* **Warm-up cells**

  ```python
  Bike.objects.count()
  Rental.objects.select_related("bike")[:3]
  ```
* **Pandas bridge** – convert top-revenue bikes to a DataFrame, plot bar chart.
* **%timeit & .query** – profile a heavy join and inspect generated SQL.
* **Graph the schema** – run `!python manage.py graph_models catalog -o catalog.svg` then display inside notebook.
* **Kernel restart** – demonstrate memory reset after changing a model field.
* **Exit** – shut down Jupyter cleanly (`File → Close and Halt`) to avoid zombie kernels.

---

### **3. Assignment**

* **Notebook deliverable**

  * Query *all* rentals in 2025, compute total revenue per month, and plot a line chart.
  * List the three users with the highest cumulative spend.
  * Save notebook as `2025_revenue_analysis.ipynb`.
* **Version control**

  * Exclude notebook checkpoints (`.ipynb_checkpoints/`) via `.gitignore`.
* **Reflection paragraph**

  * 120 words on how the notebook accelerated insight compared with writing a management command.

---

### **4. Conclusion**

Coupling Jupyter with `django-extensions` elevates Django from a web framework into a full-stack data workbench.  You explored live database objects, profiled queries, visualised schemas, and rendered charts—all in one browser tab.  While notebooks are unsuited for production automation, they excel at hypothesis-driven analysis and quick remedial fixes.  Armed with this toolset, you can diagnose performance issues, prototype data migrations, or produce executive dashboards without context switching to separate BI platforms.  Treat the notebook as an intellectual sketchpad; once the idea crystallises, graduate the code into repeatable scripts.
