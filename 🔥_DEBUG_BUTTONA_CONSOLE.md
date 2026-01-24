🔥 DEBUGGING BUTTONA - KORACI

Sad sam dodao DETALJAN console.log u sve buttonima!

✅ ŠTAS SAM DODAO:
1. updateSettings - vidiš će log PRIJE negotiira API
2. clearAllChats - vidiš će log PRIJE brisanja
3. Delete chat button - vidiš će log PRIJE brisanja

✅ KAKO TESTIRATI:

1. Otvori http://localhost:3000 u browser-u
2. Login: admin / admin123
3. Pritisni F12 (Developer Tools)
4. Klikni na "Console" tab
5. **ČEKAJ 5 SEKUNDI** dok React recompile Dashboard.js (trebat će refresh)
6. Refresh stranicu (F5)
7. Sada testiraj button:
   - Idi u Settings tab
   - Promijeni Temperature na 0.9
   - Klikni "SAVE AI Settings"
   
8. U Console-u ćeš vidjeti:
   ```
   🔥 DEBUG: updateSettings called with: {temperature: 0.9}
   🔥 DEBUG: apiUrl: http://localhost:8000
   🔥 DEBUG: getConfig(): {headers: {Authorization: "Bearer ..."}}
   🔥 DEBUG: Sending PUT to: http://localhost:8000/user/settings
   🔥 DEBUG: Response: {...}
   ✅ AI Settings saved successfully!
   ```

9. Ako vidiš ERRORS (crveni tekst), KOPIRAJ točan tekst greške i pošalji mi!

OČEKIVANI REDOSLIJED:
- Ako vidiš sve logove do "Sending PUT" = React radi OK
- Ako nema "Response" logline = API problem
- Ako nema "updateSettings called" = Button se ne aktivira

Trebam da vidim exact onde se zaustavlja!
