try:
    import fitz
    print("fitz (PyMuPDF) is available!")
except Exception as e:
    print("fitz error:", e)

try:
    import pypdf
    print("pypdf is available!")
except Exception as e:
    print("pypdf error:", e)
