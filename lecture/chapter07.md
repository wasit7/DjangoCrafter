## **Chapter 7: Django Views—Function-Based vs Class-Based**

In the Model-View-Template (MVT) triad, *views* mediate between persistent data and the HTML (or JSON) ultimately delivered to the client. For newcomers, the two canonical ways to write a view in Django—**Function-Based Views (FBVs)** and **Class-Based Views (CBVs)**—can feel like a fork in the road. This chapter situates that choice in a principled way. We begin with a historical lens on how FBVs gave Django its early reputation for clarity, before exploring how CBVs arose to tame repetition in large code-bases. We will contrast their signatures, inheritance patterns, introspection costs, and their interaction with middleware and decorators. You will then build the same endpoint twice—once as a Python function, once as a class that inherits from `ListView`—so that the trade-offs become visceral. By the end, you should possess a decision rubric that tells you, *at a glance*, when a one-off FBV suffices and when a DRY-oriented CBV is the pragmatic path forward.

---

### **1. Theories**

**1.1  Anatomy of an FBV**
An FBV is simply a Python callable that accepts an `HttpRequest` instance and returns an `HttpResponse` (or subclass). Inside, you are free to orchestrate ORM queries, form handling, business logic, and template rendering. Because the body is *linear*, the cognitive path from request to response is literally top-to-bottom, which makes FBVs self-documenting. Decorating an FBV with `@login_required` (or any custom decorator) is nothing more than function composition—a first-class notion in Python. Under the hood, Django resolves the URL, calls your function, then hands its return value to the WSGI layer. There is zero metaclass magic, so `print()` debugging and IDE “go-to definition” both work flawlessly.

**1.2  Anatomy of a CBV**
A CBV is a Python class whose *methods* correspond to HTTP verbs (`get()`, `post()`, `patch()`, etc.). The class is itself callable because Django’s `View` base class implements `__call__`, delegating to `dispatch()`, which performs method routing and middleware-like hooks (`setup()`, `initial()`, `dispatch()`, `finalize_response()`). In practice, you rarely inherit from `View` directly. Instead, you choose a *generic view* such as `ListView`, `DetailView`, or `CreateView`, which arrives pre-wired with querysets, context naming, pagination, and form handling. Through **mixins** (`LoginRequiredMixin`, `PermissionRequiredMixin`, `JsonResponseMixin`) you compose cross-cutting concerns with declarative brevity. The trade-off is indirection: to understand a single line—`class BikeListView(LoginRequiredMixin, ListView):`—you must follow the Method Resolution Order (MRO) across three or more classes.

**1.3  When FBVs Shine**

* **Atomicity**: One-off pages (health-check, Webhook endpoint) are easier to express as a function.
* **Performance profiling**: A flat call-stack makes flame charts readable.
* **Learning curve**: Junior developers grok them immediately.
* **Decorators**: Wrapping with `@cache_page` or `@require_http_methods` is ergonomic.

**1.4  When CBVs Shine**

* **Boilerplate reduction**: CRUD pages differ only in model name and template; CBVs compress them to a four-line class.
* **Consistency**: Team conventions around `get_queryset()` and `get_context_data()` ensure predictable extension points.
* **Multiple verbs**: `FormView` elegantly handles GET (render) vs POST (process) without `if request.method == "POST"`.
* **DRY mixins**: Orthogonal behaviours—authentication, rate limiting, JSON serialization—compose without nested `if` blocks.

**1.5  Internals, Hooks, and Extensibility**

* *FBV decorators* operate pre- or post-execution; they cannot easily intercept class attributes.
* *CBV hooks*: `setup()`, `dispatch()`, `get_template_names()` allow deep customisation while preserving superclass logic via `super()`.
* *URL patterns*: An FBV is passed directly, whereas a CBV must be *adapted* through `.as_view()`, which instantiates the class per request.

**1.6  Decision Rubric**

| Dimension                 | FBV    | CBV    |
| ------------------------- | ------ | ------ |
| Lines of code for CRUD    | 40–60  | 8–12   |
| On-boarding cost          | 1 hour | 1 day  |
| Readability               | ★★★★★  | ★★★☆☆  |
| Extensibility (large app) | ★★☆☆☆  | ★★★★★  |

**1.7  Anti-Patterns**

* Huge FBVs with intertwined GET/POST logic → split into CBV.
* CBVs overloaded with `if self.request.user.is_superuser` branches → revert to FBV or separate class.
* Copy–pasted FBVs differing only by model → generic CBV with `model` attribute.


---

### **2. Step-by-Step Workshop**

1. **Scaffold**:

   * `docker compose run web python manage.py startapp catalog`
   * Add `catalog` to `INSTALLED_APPS`.
2. **Models**: create simple `Bike` model if not existing (`name`, `hourly_rate`).
3. **FBV Implementation**:

   ```python
   # catalog/views.py
   from django.shortcuts import render
   from .models import Bike

   def bike_list(request):
       bikes = Bike.objects.all()
       return render(request, "catalog/bike_list.html", {"bikes": bikes})
   ```
4. **CBV Implementation**:

   ```python
   from django.views.generic import ListView
   from .models import Bike

   class BikeListView(ListView):
       model = Bike
       template_name = "catalog/bike_list.html"
       context_object_name = "bikes"
   ```
5. **URLs**:

   ```python
   urlpatterns = [
       path("fbv/bikes/", bike_list, name="bike_list_fbv"),
       path("cbv/bikes/", BikeListView.as_view(), name="bike_list_cbv"),
   ]
   ```
6. **Templates**: minimal table printing `{{ bikes }}`.
7. **Mixin demo**: prepend `LoginRequiredMixin` to `BikeListView`.
8. **Benchmark**: count lines of code; run `python -m timeit` for each endpoint.
9. **Reflect**: discuss readability vs reusability on whiteboard.

---

### **3. Assignment**

* **Task 1**: Implement both FBV *and* CBV versions of `BookList` and `BookDetail` pages.
* **Task 2**: Decorate the CBV with `LoginRequiredMixin`; leave FBV public.
* **Task 3**: Capture screenshots of each endpoint and a snippet of the diff in LOC between approaches.
* **Deliverable**: Zip containing `views.py`, `urls.py`, templates, and a one-paragraph reflection on which style you would choose for a full e-commerce site and why.

---

### **4. Conclusion**

Views are the hinge on which every Django request swings. Function-based views reward immediacy and step-through debugging, whereas class-based views unlock inheritance and mixin superpowers for larger systems. A mature engineer wields both: reaching for an FBV when shipping a quick health probe, pivoting to a generic CBV when cloning list–detail–form patterns. By articulating their differences in signature, flow, and extensibility, you can now justify your choice to teammates—and refactor with confidence when project scale or team dynamics change.
