## **Chapter 10: API & Endpoint Testing with `curl`**

Whether you are validating a brand-new Django REST endpoint, reproducing a production bug at 3 a.m., or wiring an endpoint into a CI pipeline, you need a *minimal, scriptable* client that speaks raw HTTP. Enter **`curl`**—one of the oldest yet still indispensable command-line utilities in a web developer’s toolkit. Although Postman, Insomnia, and Swagger-UI offer glossy GUIs, `curl` remains unrivalled for headless automation, shell scripting, and quick ad-hoc checks. In this chapter we investigate HTTP semantics from a tester’s vantage: crafting headers, streaming JSON payloads, following redirects, extracting response codes, and chaining calls in bash. We position `curl` as the Rosetta Stone that bridges browser, mobile, and server interactions, allowing you to mimic each with surgical precision. By the end, you will be able to author repeatable test scripts that issue GET → POST → PATCH → DELETE sequences, assert status codes, and log timings—laying a foundation for smoke testing in GitHub Actions or GitLab CI.

---

### **1. Theories**

**1.1  Brief History of `curl`**
Daniel Stenberg released cURL (Client for URLs) in 1997 to automate currency exchange queries. Over time it added protocols—FTP, SMTP, LDAP, and most famously HTTP/S. Today, `curl` ships by default on macOS and most Linux distros; on Windows it arrived with PowerShell 5. The program’s DNA emphasises composability: every flag is a building block that *prints* to STDOUT, meaning you can pipe, redirect, or subshell the output in any POSIX shell.

**1.2  Anatomy of an HTTP Request**
A request comprises:

1. **Method** (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`).
2. **Request-URI** (`https://api.example.com/bikes/`).
3. **Headers** (`Accept`, `Authorization`, `Content-Type`, `User-Agent`).
4. **Body** (for non-idempotent verbs, commonly JSON).
5. **TLS handshake** if scheme is HTTPS.

`curl` defaults to `GET`. Use `-X` or method-specific shortcuts (`-d` implies `POST`, `-T` implies `PUT`). Content negotiation occurs via `Accept` header; servers may fallback to default media types. Authentication tokens ride inside `Authorization: Bearer <jwt>` or `Authorization: Token <key>` for DRF token auth.

**1.3  Core Flags Cheat Sheet**

| Flag                          | Purpose                                |
| ----------------------------- | -------------------------------------- |
| `-X <VERB>`                   | Explicit HTTP method.                  |
| `-H "Header: value"`          | Add or override header.                |
| `-d '{"json":1}'`             | Inline body; implies `POST`.           |
| `--data-binary @payload.json` | Stream file contents verbatim.         |
| `-u user:pass`                | Basic-auth credentials.                |
| `-I`                          | Fetch headers only (`HEAD`).           |
| `-o filename`                 | Write body to file (binary downloads). |
| `-w "%{http_code}\n"`         | Custom output (status codes, time).    |
| `-s`                          | Silent (no progress bar).              |
| `-S`                          | Show error even in silent mode.        |
| `-L`                          | Follow 3xx redirects.                  |
| `--http2`                     | Negotiate HTTP/2.                      |

Flags may be combined; long options (`--header`) equal short ones (`-H`).

**1.4  JSON Handling and Escaping**
Shell quoting of JSON can bite newcomers because `{}` and `" "` carry meaning. Safest strategy: place payloads in a file (`payload.json`) and use `--data @payload.json`. If inline, single-quote the whole string on POSIX shells:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"Road Bike","hourly_rate":60}' \
     http://localhost:8000/api/bikes/
```

On Windows cmd, double-quotes wrap JSON but you must escape inner quotes with `\"`.

**1.5  Authenticated Requests **
*Session cookies* work when `curl` reuses `-c cookies.txt -b cookies.txt`. For token auth:

```bash
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/bikes/
```

JWT often prefixes “Bearer”:

```bash
curl -H "Authorization: Bearer $JWT" ...
```

In CI pipelines inject secrets via environment variables; avoid seeing them in logs by piping output to `grep -v TOKEN`.

**1.6  Assertions and Exit Codes**
`curl` exits non-zero on network errors, not HTTP errors. Capture status code using `-w`:

```bash
status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health/)
[ "$status" = "200" ] || echo "Health-check failed"
```

For JSON assertions, pipe to `jq`:

```bash
curl -s http://... | jq '.bikes | length'
```

**1.7  Timing and Performance**
`-w` supports `%{time_total}`, `%{size_download}`. Combine with `-o /dev/null` to benchmark API latency. Example:

```bash
curl -s -w "%{time_total}\n" -o /dev/null http://localhost:8000/api/bikes/
```

In load testing, wrap `curl` in `xargs -P` for parallel invocations or graduate to `hey`/`wrk` when concurrency matters.

**1.8  Safety Nets: Dry-Runs and Verbose**
`-v` prints request/response headers; `--trace-ascii` logs wire bytes. Use these flags before committing destructive `DELETE` calls. Pair with sandbox environment URLs to avoid data loss.

**1.9  Scripting Patterns**
Bash arrays store endpoints, loop over verbs; functions encapsulate common headers. Example snippet:

```bash
API=http://localhost:8000/api
auth() { echo "-H Authorization:Bearer $TOKEN"; }

curl $(auth) $API/bikes/ | jq '.results[].id' |
while read id; do
  curl -X DELETE $(auth) $API/bikes/$id/
done
```

Exit the loop on first non-204 to fail fast in CI.


---

### **2. Step-by-Step Workshop**

* **Prerequisite**: Ensure Chapter 09 DRF endpoints (`/api/bikes/`) are running.
* **Generate auth token** for a user (`python manage.py drf_create_token <user>`).
* **Store variables**

  ```bash
  export API=http://localhost:8000/api
  export TOKEN=<paste>
  ```
* **List bikes**

  ```bash
  curl -H "Authorization: Token $TOKEN" $API/bikes/
  ```
* **Create bike**

  ```bash
  curl -X POST -H "Content-Type: application/json" \
       -H "Authorization: Token $TOKEN" \
       -d '{"name":"Hybrid","hourly_rate":45}' \
       $API/bikes/
  ```
* **Capture ID** using `jq`

  ```bash
  ID=$(curl -s ... | jq '.id')
  ```
* **Update (PATCH)** hourly rate

  ```bash
  curl -X PATCH -H "Content-Type: application/json" \
       -H "Authorization: Token $TOKEN" \
       -d '{"hourly_rate":50}' \
       $API/bikes/$ID/
  ```
* **Delete**

  ```bash
  curl -X DELETE -H "Authorization: Token $TOKEN" \
       $API/bikes/$ID/
  ```
* **Wrap** all commands into `test_api.sh`; add `set -e` to abort on first error.
* **Run** script and verify exit code `0`.

---

### **3. Assignment**

* **Script deliverable**: `rental_test.sh` that

  1. Accepts `API_URL` and `TOKEN` as environment variables.
  2. Lists current rentals; stores initial count.
  3. Creates a rental (POST).
  4. Updates it (PATCH).
  5. Deletes it (DELETE).
  6. At end prints **“PASS”** if final count equals initial count; otherwise exits 1.
* **Add assertions** for status codes using `-w "%{http_code}"`.
* **Provide README** describing how to execute (`chmod +x`).
* **Screenshot** terminal output demonstrating 200 → 201 → 200 → 204 sequence.

---

### **4. Conclusion**

Mastering `curl` transforms you from GUI-dependent tester to command-line virtuoso. You can reproduce client traffic byte-for-byte, embed sanity checks in shell scripts, and surface latency regressions before they ship to production. The tool’s ubiquity ensures that skills acquired here transfer seamlessly to Kubernetes health probes, AWS Lambda warm-ups, or GitHub workflow steps. When combined with JSON filters like `jq`, `curl` becomes a miniature integration-test framework that runs anywhere POSIX does—empowering you to validate APIs long before full-stack UIs or mobile clients exist.
