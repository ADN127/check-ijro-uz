#!/bin/bash

# PDF fayl qo'shish scripti
# Foydalanish: ./add_pdf.sh FAYL_YOLI YANGI_NOM

if [ $# -ne 2 ]; then
    echo "Foydalanish: $0 FAYL_YOLI YANGI_NOM"
    echo "Misol: $0 /path/to/document.pdf mydocument"
    exit 1
fi

FAYL_YOLI="$1"
YANGI_NOM="$2"

# Fayl mavjudligini tekshirish
if [ ! -f "$FAYL_YOLI" ]; then
    echo "Xato: Fayl topilmadi - $FAYL_YOLI"
    exit 1
fi

# PDF kengaytmasini tekshirish
if [[ ! "$FAYL_YOLI" =~ \.pdf$ ]]; then
    echo "Xato: Fayl PDF formatida bo'lishi kerak"
    exit 1
fi

# Yangi nom to'g'riligini tekshirish
if [[ ! "$YANGI_NOM" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "Xato: Fayl nomi faqat ingliz harflari, raqamlar, _ va - belgilarini o'z ichiga olishi mumkin"
    exit 1
fi

# PDF faylni ko'chirish
MAQSAD_PAPKA="src/static/pdfs"
MAQSAD_FAYL="$MAQSAD_PAPKA/${YANGI_NOM}.pdf"

if [ -f "$MAQSAD_FAYL" ]; then
    echo "Ogohlantirish: $MAQSAD_FAYL allaqachon mavjud. Almashtirilsinmi? (y/n)"
    read -r javob
    if [[ ! "$javob" =~ ^[Yy]$ ]]; then
        echo "Bekor qilindi"
        exit 0
    fi
fi

cp "$FAYL_YOLI" "$MAQSAD_FAYL"

if [ $? -eq 0 ]; then
    echo "✅ PDF fayl muvaffaqiyatli qo'shildi!"
    echo "📁 Fayl joylashuvi: $MAQSAD_FAYL"
    echo "🌐 URL: /d/$YANGI_NOM"
    echo ""
    echo "Saytni qayta deploy qilishni unutmang:"
    echo "manus service deploy backend ."
else
    echo "❌ Xato: Fayl ko'chirishda muammo yuz berdi"
    exit 1
fi

