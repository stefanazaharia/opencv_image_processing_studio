# OpenCV Image Processing Studio

O aplicație desktop dedicată procesării imaginilor și viziunii computerizate, dezvoltată în Python folosind Tkinter și OpenCV. Aplicația oferă o interfață interactivă cu două panouri pentru compararea directă între imaginea originală și rezultatul procesat, incluzând peste 16 transformări algoritmice — de la convoluții spațiale clasice la deformări geometrice neliniare.

---

## Funcționalități principale

- **Interfață cu două panouri:** Comparare vizuală în timp real între imaginea inițială și cea modificată.
- **Detecție de muchii și praguri:** Detectorul de contur Canny și binarizare pe bază de prag (*thresholding*).
- **Filtrare spațială și convoluții:** Filtru Gaussian, Stack Blur, Box filter și clarificare (*sharpening*) prin kernel matricial Laplacian 2D.
- **Deformări afine și geometrice:**
  - Rotire standard la 90° și transformare afină la 45° cu scalare (`warpAffine`).
  - Remapare spațială neliniară a coordonatelor: **Efect de Vârtej / Twirl** în coordonate polare și **Deplasare Sinusoidală (Valuri)** (`cv2.remap`).
  - Piramide gaussiene (`pyrUp`) pentru mărire digitală centrată (*zoom*).
- **Efecte stilistice și utilitare:** Pixelare (micșorare bilineară urmată de mărire prin *nearest-neighbor*), inversie pe biți (negativ), watermark cu fundal mat, ramă colorată și linii de trasare.
- **Gestiune fișiere:** Încărcare imagini locale, selector aleatoriu dintr-un folder de test și export automat al rezultatelor fără suprascrierea fișierului original.

---

## Structura proiectului

```text
opencv-image-processing-studio/
├── app.py                # Interfața grafică Tkinter și gestionarea evenimentelor
├── script.py             # Algoritmii OpenCV și logica de procesare a imaginilor
├── imagini_test/         # Director opțional pentru imagini de testare
├── requirements.txt      # Dependențele necesare proiectului
└── README.md             # Documentația proiectului<img width="976" height="532" alt="Screenshot 2026-10-09 200048" src="https://github.com/user-attachments/assets/530d33dd-a89c-4e64-be82-a41060371461" />

![Uploading Screenshot 2026-10-09 200048.png…]()


