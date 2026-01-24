# 🔥 DEBUGGING BUTTONA - TAČNE KORAKE

## KORAK 1: Zatvori KOMPLETNO browser
- Zatvori sve tabove
- Zatvori cijeli browser
- Wait 5 sekundi

## KORAK 2: Otvori browser + Developer Tools
```
1. Otvori Firefox/Chrome
2. Incognito mode
3. Idi na http://localhost:8000
4. Prije nego učitaš stranicu, pritisni F12
5. Klikni na "Console" tab
6. Ostavi Console otvoren tijekom testiranja
```

## KORAK 3: Login
```
Username: admin
Password: admin123
Klikni LOGIN
```

## KORAK 4: TEST BUTTON
Idemo testirati JEDAN button:

### TEST A: SAVE AI SETTINGS
```
1. Klikni Settings tab
2. Promijeni Temperature sa 0.7 na 0.9
3. Klikni SAVE AI Settings button (💾)
4. PAZI NA CONSOLE - što se dogodilo?
   - Vidiš li ALERT u kodu?
   - Vidiš li ERROR koji je crven?
   - Što točno piše?
```

**PROVJERA 1: Vidiš li Alert popup?**
- DA = button radi, JavaScript se izvršava
- NE = problem je u kodu ili buttonu

**PROVJERA 2: Pročitaj Console**
- Vidiš li: "✅ AI Settings saved successfully!"
- Ili vidiš ERROR (crveno teksto)?
- Kopira točan tekst greške!

### TEST B: NETWORK TAB
```
1. Klikni F12 Network tab
2. Promijeni nešto u Settings
3. Klikni SAVE
4. U Network tab-u, traži /user/settings (PUT request)
5. Provjeri:
   - Status: 200 OK? Ili nešto drugo?
   - Response: Što piše u Response tab-u?
```

## KORAK 5: PROVJERA BUILD-a

U Network tab-u, kad se stranica učitava:
```
1. Traži main.*.js file
2. Provjeri veličinu - treba biti ~275KB
3. Provjeri vrijeme - trebam vidjeti točnu verziju
```

---

## 🔴 AKO NEŠTO NE RADI - POŠALJI MU SLIKU:

Trebam ti screenshot od:
1. **Console tab** - što piše nakon klika na button?
2. **Network tab** - koja API request se šalje i koji je status?
3. **Notifications/Alerts** - vidiš li popup ili ne?

---

## ⚠️ MOGUĆA RJEŠENJA PO PRIORITETU:

**1. Button se NE klikuje**
- Problem: CSS disabled ili onClick ne attachan
- Fix: Provjerit ću HTML strukturi

**2. onClick se pokreće ALI nema API requesta**
- Problem: JavaScript error unutar funkcije
- Fix: Trebam vidjeti Console error

**3. API request ide ALI vraća grešku (non-200 status)**
- Problem: Backend nije spreman ili route je kriv
- Fix: Trebam vidjeti Network Response

**4. API vraća 200 ALI alert ne prikazuje**
- Problem: setTimeout ili catch block je kriv
- Fix: Trebam debug u kodu

---

**URADI OVO SADA I POŠALJI MU:**
1. Screenshot F12 Console nakon klika na SAVE button
2. Screenshot F12 Network tab nakon istog klika
3. Točan tekst greške ako je ima
