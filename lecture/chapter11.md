## **Chapter 11  Google Social Login with Django Allauth**

Modern users expect to click a familiar Google button and enter your application without inventing yet another password.  Implementing that magic from scratch—OAuth 2 handshakes, token exchanges, email-verification, and edge-case revocations—would consume weeks and risk subtle security bugs.  **Django Allauth** wraps these complexities in an opinionated yet flexible package that supports username + password *and* dozens of social providers.  In this chapter we concentrate on Google, because its OAuth 2 workflow—authorization code grant, consent screen, access & ID tokens—exemplifies best practice.  We will dissect Allauth’s architecture (`account`, `socialaccount`, `providers`), configure environment-driven secrets, and explore signals for post-signup business logic.  You will then implement Google login end-to-end, customise consent scopes, and restrict new accounts to *@your-university.edu*.  By the end you will understand how Allauth offloads authentication while still allowing you to enforce fine-grained permissions and brand-consistent templates.

---

### **1. Theories**

**1.1 OAuth 2 Flow in a Nutshell**
Google’s implementation follows the *Authorization Code* grant:

1. **Client Redirect** – User clicks “Sign in with Google,” your site redirects to Google’s `/o/oauth2/v2/auth` with client\_id, redirect\_uri, scope, state.
2. **Consent Screen** – Google authenticates the user (if needed) and asks for scope approval (`openid email profile`).
3. **Authorization Code** – Browser is redirected back to `redirect_uri` (`/accounts/google/login/callback/`) with `code` and `state`.
4. **Token Exchange** – Your backend exchanges `code` for an **access token** and an **ID token (JWT)** via Google’s token endpoint.
5. **User Info** – Access token fetches profile; ID token already contains email, sub, picture.
6. **Session Creation** – Allauth either logs the user in or provisions a new Django `User`, emits signals, and sets a session cookie.

**1.2 Allauth Package Layout**

| App                                      | Purpose                                                          |
| ---------------------------------------- | ---------------------------------------------------------------- |
| `allauth.account`                        | Local accounts: signup, email confirmation, password reset.      |
| `allauth.socialaccount`                  | Abstract layer for social providers, social tokens, social apps. |
| `allauth.socialaccount.providers.google` | Google-specific OAuth client & default scopes.                   |

The table **`socialaccount_socialapp`** stores `client_id`, `secret`, and domain restrictions; **`socialaccount_socialtoken`** stores refresh tokens if offline access is granted.

**1.3 Django Settings Checklist**

```python
INSTALLED_APPS += [
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
LOGIN_REDIRECT_URL = "dashboard"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # or "none"
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}
```

Leave `client_id` and `secret` in the **admin** via Social App or load from environment variables with `django-environ`.

**1.4 Consent Screen Configuration**
In Google Cloud Console:

* Set *OAuth consent screen* type = *External* (or *Internal* for Workspace).
* Whitelist your primary domain.
* Add authorised redirect URIs e.g.

  ```
  http://localhost:8000/accounts/google/login/callback/
  https://prod.example.com/accounts/google/login/callback/
  ```
* Publish the app; in *Testing* mode only test users can authenticate.

**1.5 State Parameter and CSRF**
Allauth stores a cryptographically random `state` in session; Google echoes it back.  The callback view verifies equality, thwarting CSRF login attacks.  Ensure cookies use `SameSite=Lax` (Django 4 default) or `Strict` if feasible.

**1.6 Email-Domain Whitelisting**
Hook `socialaccount.adapter.DefaultSocialAccountAdapter`:

```python
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
class GoogleDomainAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        email = sociallogin.account.extra_data.get("email", "")
        return email.endswith("@wasit7.edu")
```

Set `SOCIALACCOUNT_ADAPTER = "myapp.adapters.GoogleDomainAdapter"`.

**1.7 Signals for Post-Signup Logic**
`user_signed_up` and `social_account_added` fire after database commit.  Example:

```python
@receiver(user_signed_up)
def create_profile(sender, request, user, **kwargs):
    Picture = kwargs["sociallogin"].account.extra_data["picture"]
    Profile.objects.create(user=user, avatar=Picture)
```

This keeps view code clean and respects Allauth’s transaction boundaries.

**1.8 Template Overrides**
Copy Allauth templates into `templates/account/` and `templates/socialaccount/` to brand the login page.  Ensure `{% provider_login_url "google" %}` renders the dynamic auth link.

**1.9 Testing Strategies**

* **Unit**: Mock `allauth.socialaccount.providers.google.views.oauth2_client`.
* **Integration**: Use Google’s *OAuth 2 Playground* or a service account to obtain a short-lived code.
* **CI**: Mark social-login tests as `@pytest.mark.social` and skip on PR builds to avoid secret leakage.
* **e2e**: Use Cypress; stub the Google consent screen with fixtures.

**1.10 Production Hardening**

1. Enforce HTTPS—Google rejects localhost over HTTP except `127.0.0.1`.
2. Rotate client secret annually.
3. Limit *Your OAuth Client* to your prod/stage origins; use separate credentials per environment.
4. Set `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True`.
5. Monitor token refresh errors; Google invalidates refresh tokens upon password change or 6-month inactivity.


---

### **2. Step-by-Step Workshop**

* **Install packages**

  ```bash
  pip install django-allauth python-dotenv
  ```
* **Add apps & backends** in `settings.py` (see §1.3).
* **Create `.env`**

  ```
  GOOGLE_CLIENT_ID=...
  GOOGLE_SECRET=...
  ```
* **Load secrets**

  ```python
  import environ
  env = environ.Env()
  SOCIALACCOUNT_PROVIDERS["google"]["APP"] = {
      "client_id": env("GOOGLE_CLIENT_ID"),
      "secret": env("GOOGLE_SECRET"),
      "key": "",
  }
  ```
* **Migrate & superuser**

  ```bash
  python manage.py migrate
  python manage.py createsuperuser
  ```
* **Admin setup** – add *Social App* “Google,” select *Sites = example.com*.
* **Runserver** and visit `/accounts/login/`; click “Sign in with Google.”
* **Observe** new `User`, `SocialAccount`, `SocialToken` rows.
* **Customise template** – copy `login.html`, replace button style with Tailwind classes.
* **Restrict domain** – implement `GoogleDomainAdapter` from §1.6.

---

### **3. Assignment**

* **Task 1**: Implement domain-restricted signup (`@wasit7.edu`) via a custom adapter.
* **Task 2**: Add `user_signed_up` signal to create a `Profile` with Google avatar.
* **Task 3**: Override login template to use your faculty colours.  Screenshot before & after.
* **Task 4**: Write an integration test that asserts a 302 redirect to Google when hitting `provider_login_url`.
* **Deliverable**: PR containing adapter, signal, template, test, and screenshots.

---

### **4. Conclusion**

Django Allauth condenses Google’s labyrinthine OAuth 2 dance into a handful of settings and one admin record, freeing you to focus on domain logic rather than token plumbing.  Yet the library remains porous enough—through adapters, signals, and template overrides—to enforce institutional policy, enrich user profiles, and maintain brand fidelity.  Mastery of Allauth therefore equips you to onboard users effortlessly while preserving robust security hygiene and an extensible codebase.

