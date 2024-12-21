
# راهنمای پیاده‌سازی درگاه پرداخت پی‌پینگ در Flask

  

## توضیحات

این پروژه مبتنی بر فلسک ایجاد شده است برای استفاده از درگاه پرداخت پی پینگ با ساختاری کاملا ساده و صفحه ساده فروش محصولات

## پیش‌نیازها

- Python 3.7 یا بالاتر

- Flask

- Requests

- توکن API پی‌پینگ

  

## نصب و راه‌اندازی

  

### ۱. نصب وابستگی‌ها

```bash

pip  install  flask  requests

```

  

### ۲. تنظیمات پروژه

۱. کلون کردن مخزن:

```bash

git  clone <repository-url>

cd <project-directory>

```

  

۲. ایجاد پوشه templates و کپی کردن فایل‌های HTML در آن

  

۳. تنظیم متغیرهای محیطی:

- تغییر `PAYPING_API_TOKEN` به توکن API دریافتی از پی‌پینگ

- تغییر `app.secret_key` به یک کلید امن

  

### ۳. اجرای پروژه

```bash

python  app.py

```
 

پس از اجرا، برنامه روی آدرس `http://localhost:5000` در دسترس خواهد بود.
در محیط پروداکشن از Gunicorn یا Hypercorn بهره بگیرید.
  
  

## کلاس‌های اصلی

  

### PaymentRequest

این کلاس برای ساخت درخواست پرداخت استفاده می‌شود:

```python

PaymentRequest(

amount=10000, # مبلغ به تومان

return_url="...", # آدرس بازگشت

payer_identity="...", # شناسه پرداخت‌کننده (اختیاری)

payer_name="...", # نام پرداخت‌کننده (اختیاری)

description="...", # توضیحات پرداخت (اختیاری)

client_ref_id="..."  # شناسه مرجع (اختیاری)

)

```

  

### PayPingGateway

کلاس اصلی برای تعامل با API پی‌پینگ:

-  `create_payment`: ایجاد پرداخت جدید

-  `verify_payment`: تایید پرداخت

-  `get_payment_gateway_url`: دریافت آدرس درگاه پرداخت

  

## مسیرهای (Routes) برنامه

  

| مسیر | توضیحات |



| `/` | صفحه اصلی - نمایش محصولات |

| `/initiate-payment/<product_id>` | شروع فرایند پرداخت |

| `/verify-payment` | تایید پرداخت (callback) |

| `/success` | صفحه موفقیت‌آمیز بودن پرداخت |

  

## فراینده

  

1. کاربر محصول را از صفحه اصلی انتخاب می‌کند

2. برنامه یک درخواست پرداخت در پی‌پینگ ایجاد می‌کند

3. کاربر به درگاه پرداخت پی‌پینگ هدایت می‌شود

4. پس از پرداخت، کاربر به endpoint تایید برنامه هدایت می‌شود

5. برنامه پرداخت را تایید و نتیجه را نمایش می‌دهد

  

## ویژگی‌های امنیتی

  

- مدیریت session برای جلوگیری از دستکاری

- تایید مبلغ پرداخت

- مدیریت خطاها در API

- محافظت CSRF

  

## نکات مهم

  

1. همیشه مبلغ پرداخت را در سمت سرور تایید کنید

2. از توکن API در محیط عمومی استفاده نکنید

3. حتماً پرداخت‌ها را در دیتابیس ذخیره کنید

4. برای محیط تولید، debug را غیرفعال کنید

  

## مثال استفاده

  

```

# gateway instance

gateway = PayPingGateway("your-api-token")

  

# ایجاد درخواست پرداخت

payment = PaymentRequest(

amount=10000,

return_url="https://yoursite.com/callback",

description="پرداخت سفارش #123"

)

  

# ارسال درخواست

result = gateway.create_payment(payment)

payment_code = result["code"]

  

# هدایت کاربر به درگاه

payment_url = gateway.get_payment_gateway_url(payment_code)

```

  

## مشارکت

برای مشارکت در پروژه:

1. پروژه را fork کنید

2. یک branch جدید ایجاد کنید

3. تغییرات خود را commit کنید

4. یک pull request ایجاد کنید

  

## پشتیبانی

برای پشتیبانی می‌توانید از طریق زیر اقدام کنید:

- ایمیل: amirdev2024@gmail.com

- https://www.linkedin.com/in/amir-ahmadabadiha-259113175/