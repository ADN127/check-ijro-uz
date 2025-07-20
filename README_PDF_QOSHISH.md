# PDF Fayllar Qo'shish Yo'riqnomasi

## Qanday qilib yangi PDF fayl qo'shish

### 1-usul: Manual qo'shish

1. PDF faylni `/src/static/pdfs/` papkasiga joylashtiring
2. Fayl nomi ingliz harflari va raqamlardan iborat bo'lishi kerak
3. URL orqali kirish: `https://sayt.manus.space/d/FAYL_NOMI`

**Misol:**
- Fayl: `OJ2038108378.pdf` → URL: `/d/OJ2038108378`
- Fayl: `don12345678.pdf` → URL: `/d/don12345678`

### 2-usul: Script yordamida

```bash
# PDF faylni qo'shish
./add_pdf.sh FAYL_YOLI YANGI_NOM

# Misol:
./add_pdf.sh /path/to/document.pdf mydocument
```

### Mavjud fayllar

- `don12345678.pdf` - Test fayl
- `OJ2038108378.pdf` - Yangi qo'shilgan fayl

### URL'lar

- https://xlhyimc3gwm8.manus.space/d/don12345678
- https://xlhyimc3gwm8.manus.space/d/OJ2038108378

### Eslatma

- Fayl nomlari `.pdf` kengaytmasiz URL da ishlatiladi
- Fayllar avtomatik ravishda PDF.js viewer da ochiladi
- Sayt avtomatik ravishda yangi fayllarni taniydi

