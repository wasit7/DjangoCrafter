## **Chapter 9: Building REST APIs with Django REST Framework**

Representational State Transfer (REST) is the lingua franca that permits browsers, mobile apps, micro-services, and IoT devices to talk to your Django backend in a stateless, cache-friendly manner. Django itself can emit JSON, but the boilerplate soon becomes onerous: you hand-write `JsonResponse`, form validation, status codes, pagination, and authentication checks over and over. **Django REST Framework (DRF)** collapses this ceremony into a coherent toolkit whose Serializers validate data, whose ViewSets map HTTP verbs to CRUD semantics, and whose Routers auto-generate URLConf entries. Equally valuable is DRF’s browsable HTML interface, which turns every endpoint into an executable, self-documenting contract for front-end colleagues. In this chapter we dissect DRF’s architecture, clarify where it sits relative to classic views, and then scaffold a fully authenticated `Bike` API in fewer than fifty lines of code. By the end you will know how to expose resources, paginate large result sets, and lock endpoints behind token-based security—all while adhering to RESTful conventions.

---

### **1. Theories**

**1.1 REST Fundamentals**
REST, coined by Roy Fielding in 2000, defines six architectural constraints: client–server, statelessness, cacheability, layered system, uniform interface, and optional code-on-demand. In practical terms a *resource* (e.g., `/api/bikes/42/`) is addressable via a URL and manipulated through HTTP verbs: `GET` (read), `POST` (create), `PUT/PATCH` (update), and `DELETE` (remove). Idempotency and safety matter: `GET` should never mutate state, while `PUT` called twice should yield the same outcome. Well-behaved APIs accompany responses with status codes—`200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `401 Unauthorized`, `404 Not Found`, `500 Internal Server Error`—and expose pagination metadata to curb payload size.

**1.2 DRF’s Layer Cake**
DRF overlays Django with three concentric layers:

1. **Serializers** – Translate between Python objects (or QuerySets) and primitive Python types ready for JSON/BSON/YAML output while enforcing validation rules.
2. **Views / ViewSets** – Classes that route verbs to methods (`list()`, `retrieve()`, `create()`, `update()`, `destroy()`). `APIView` offers a low-level entry point; `GenericAPIView` adds mixins; `ModelViewSet` wraps all CRUD in one class.
3. **Routers** – Factory objects that inspect a ViewSet and auto-create URL patterns following REST style, e.g., `/bikes/`, `/bikes/{pk}/`.

**1.3 Serializers in Depth**
`class BikeSerializer(serializers.ModelSerializer):` automatically mirrors all model fields, but you can add calculated properties (`SerializerMethodField`), nested relationships (`depth = 1` or explicit sub-serializers), and custom validation through `validate_<fieldname>` or `validate()` (object-level). Unlike Django forms, serializers are decoupled from request cycle and render pure data, ideal for non-HTML clients.

**1.4 Authentication & Permissions**
DRF ships with session auth (good for browsers), basic auth, and token auth. In settings:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

Token authentication issues each user a `Token` row—typically created via signal or `/api-token-auth/`. Permissions run *after* authentication; `IsAuthenticated`, `IsAdminUser`, and `DjangoModelPermissions` are bundled, while custom permission classes override `has_permission()` or `has_object_permission()`.

**1.5 Pagination, Filtering, Versioning, Throttling**

* *Pagination* choices: `PageNumberPagination`, `LimitOffsetPagination`, `CursorPagination`. Clients receive `count`, `next`, and `previous` links.
* *Filtering* via `django-filter` allows `/api/bikes/?hourly_rate__gte=50`.
* *Versioning* (URL, namespace, header) supports `/v1/bikes/` vs `/v2/bikes/`.
* *Throttling* (user, anon, scoped) curtails abuse; example: 1,000 requests/day per user.

**1.6 Browsable API**
DRF’s renderer stack negotiates `text/html` by default. Visit `/api/bikes/` in a browser and you can POST payloads via a web form. This feature doubles as interactive documentation and manual testing harness, reducing friction for QA and front-end engineers.

**1.7 Classical Views vs DRF Views**
An `HttpResponse` from Chapter 07 could emit JSON, but you would lose automatic parsing, error serialisation, and content negotiation. DRF views inherit from Django’s but override the dispatch pipeline with `Request` (wrapping `HttpRequest` plus `.data`) and `Response` (wrapping `HttpResponse` plus renderer selection).

**1.8 Testing**
`APIClient` extends Django’s `Client` with JSON helpers (`.post(url, data, format="json")`). Use `force_authenticate()` for unit tests, or issue token headers. Status-code assertions: `self.assertEqual(resp.status_code, status.HTTP_201_CREATED)`.


---

### **2. Step-by-Step Workshop**

* **Install**

  ```bash
  pip install djangorestframework djangorestframework-simplejwt
  ```
* **Settings** – add `'rest_framework'` to `INSTALLED_APPS`; configure `DEFAULT_AUTHENTICATION_CLASSES` as JWT or Token.
* **Serializer**

  ```python
  class BikeSerializer(serializers.ModelSerializer):
      class Meta:
          model  = Bike
          fields = "__all__"
  ```
* **ViewSet**

  ```python
  class BikeViewSet(viewsets.ModelViewSet):
      queryset         = Bike.objects.all()
      serializer_class = BikeSerializer
  ```
* **Router & URLs**

  ```python
  router = routers.DefaultRouter()
  router.register("bikes", BikeViewSet)
  urlpatterns = [path("api/", include(router.urls))]
  ```
* **Migrate & create tokens**

  ```bash
  python manage.py migrate
  python manage.py drf_create_token <username>
  ```
* **Test with curl**

  ```bash
  curl -H "Authorization: Token <key>" http://localhost:8000/api/bikes/
  ```
* **Enable pagination** – set `DEFAULT_PAGINATION_CLASS` and `PAGE_SIZE` in settings.

---

### **3. Assignment**

* **Task 1**: Write `RentalSerializer` and `RentalViewSet`; register it at `/api/rentals/`.
* **Task 2**: Activate page-number pagination (page = 2, page\_size = 5).
* **Task 3**: Supply a bash script `rental_test.sh` that:

  * Lists rentals (GET).
  * Creates a rental (POST).
  * Updates with PATCH.
  * Deletes it.
* **Task 4**: Include JWT authentication in the script header.
* **Deliverable**: Pull request with code, script, and terminal screenshot of status codes `200 → 201 → 200 → 204`.

---

### **4. Conclusion**

Django REST Framework elevates your Django project from HTML templating engine to multi-tenant data platform. Through Serializers, ViewSets, and Routers you can expose complex relational data as clean JSON with validation, pagination, and authentication in minutes. The browsable API becomes living documentation, while token or JWT headers gatekeep critical endpoints. Armed with these abstractions, you are now equipped to service React front-ends, mobile apps, or partner integrations without duplicating boilerplate or compromising security.
