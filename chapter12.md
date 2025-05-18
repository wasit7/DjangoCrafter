## **Chapter 12: QR-Enabled Bike-Rental Kiosk (Capstone)**

Digital self-service kiosks succeed only when three moving parts—*identity, inventory, and payment*—operate in seamless concert.  In the previous chapters we authenticated users with Google, exposed inventory via REST, and tested endpoints with `curl`.  Now we will complete the circle by attaching a **Thai PromptPay QR** code to each bike-rental transaction so that a customer can scan, pay, and ride away without staff intervention.  The objective is not merely to print a square barcode; it is to demonstrate how a payment reference propagates through the entire stack: generated in the view layer, stored in the database, retrieved by a mobile client, and reconciled in financial reports.  Because PromptPay follows the **EMVCo** QR specification—used from Bangkok street vendors to Singapore’s PayNow—mastery here translates directly to other Southeast-Asian markets.  By the end of this capstone you will appreciate how disparate competencies co-alesce into a production-ready micro-product.

---

### **1. Theories**

**1.1  Thai PromptPay and the EMVCo Standard**
PromptPay is Thailand’s real-time retail payment rail operated by the Bank of Thailand.  Its QR format adheres to **EMV® QR Code Specification**—a hierarchical tag-length-value (TLV) schema in which each element is a two-digit ID, two-digit length, and variable content.  The critical tags are:

| ID   | Purpose                                | Example                                     |
| ---- | -------------------------------------- | ------------------------------------------- |
| `00` | Payload Format Indicator (fixed `01`)  | `0102`                                      |
| `29` | Merchant Account Information–PromptPay | sub-tags `00` (AID) and `01` (PromptPay ID) |
| `54` | Transaction Amount (optional)          | `540750.00`                                 |
| `58` | Country Code (`TH`)                    | `5802TH`                                    |
| `63` | CRC-16/CCITT checksum                  | calculated over preceding text              |

Thai banks recognise **three identifiers**: mobile number, national ID, and e-wallet ID.  The checksum ensures tamper resistance at the point of scan.

**1.2  Static vs Dynamic QR**

* *Static* QR encodes only the PromptPay ID; payer specifies amount manually—useful for tips or donations.
* *Dynamic* QR includes an `invoice reference` (tag `62`) and amount; ideal for POS systems because it links *one distinct payment* to one backend order, enabling automated reconciliation.

**1.3  Mapping Payment Reference to Rental Records**
We extend the `Rental` model:

```python
import uuid
class Rental(models.Model):
    ...
    payment_ref = models.UUIDField(default=uuid.uuid4, unique=True)
    is_paid     = models.BooleanField(default=False)
```

`payment_ref` (UUID v4) is embedded in tag `62` of the QR payload.  When a bank webhook (or manual CSV file) confirms settlement, we lookup the rental:

```python
Rental.objects.filter(payment_ref=uuid_from_qr).update(is_paid=True)
```

Thus, payment status becomes a first-class field for API consumers and admin staff alike.

**1.4  Security & Fraud-Mitigation**
Although PromptPay transactions are push-payments (payer initiates), QR tampering can redirect funds.  Counter-measures:

1. Display last four digits of the registered phone number beneath the QR.
2. Sign the payload server-side; do **not** allow client JS to generate QR unchecked.
3. Update QR after five minutes or on page reload to thwart replay via screenshots.

**1.5  UX Considerations**

* Show a progress bar or polling spinner after scan; many Thai banking apps push a “success” notification that you can detect via webhook within 1–2 seconds.
* Provide a fallback payment channel (cash, card) for tourists without Thai banking apps.
* Store PNG at 512×512 px; retinal displays enlarge gracefully without scan errors.

**1.6  Notebook-Based Bulk Generation**
Using `django-extensions`’s `shell_plus --notebook`, operations can pre-generate 500 QR codes at the start of each day, cache them in S3, and embed URLs in the kiosk frontend—reducing runtime CPU cost and isolating payment logic to a single trusted environment.

---

### **2. Step-by-Step Workshop**

* **Install libraries**

  ```bash
  pip install promptpay qrcode Pillow
  ```
* **Utility function**

  ```python
  from promptpay import qrcode as pp
  import qrcode, io, base64
  def generate_promptpay_qr(rental):
      payload = pp.generate_payload(
          promptpay_id="0812345678",
          amount      = rental.total_fee,
          invoice     = str(rental.payment_ref)
      )
      img = qrcode.make(payload)
      buffer = io.BytesIO()
      img.save(buffer, format="PNG")
      return base64.b64encode(buffer.getvalue()).decode()
  ```
* **Model method** – add `get_qr_base64()` to `Rental`.
* **Protected detail view** (`LoginRequiredMixin`) returns JSON `{..., "qr": "<base64>"}`.
* **Template** – for staff UI display `<img src="data:image/png;base64,{{ qr }}">`.
* **Notebook bulk generation**

  ```python
  rentals = Rental.objects.filter(is_paid=False)[:10]
  for r in rentals:
      open(f"{r.id}.png","wb").write(base64.b64decode(r.get_qr_base64()))
  ```
* **Webhook stub** – create `/payments/promptpay/webhook/` endpoint; parse settlement CSV or receive POST from bank API, update `is_paid`.

---

### **3. Assignment**

* **Deliverables**

  * PNG or screenshot of one generated QR.
  * JSON response from `GET /api/rentals/{id}/` showing `"is_paid": false` before payment and `true` after simulated webhook.
  * *100-word* paragraph explaining how settlement flows from bank to database.

---

### **4. Conclusion**

This capstone unified every competency acquired so far: Dockerised Django, REST endpoints, Google-based identity, `curl` scripting, notebook exploration, and now EMV-compliant QR payments.  You have learned to embed a cryptographically validated reference inside a QR payload, surface it in a web or native client, and reconcile the resulting funds back to a domain object.  The same blueprint generalises to retail POS, charity kiosks, or e-ticketing platforms—any context where stateless pay-per-use meets digital identity and inventory management.
