@echo off
REM Script batch pour afficher les étapes d'ajout du port 5506 à Google Cloud Console

cls
echo.
echo ==========================================
echo   ^!ERREUR DETECTEE: Port 5506 manquant^!
echo ==========================================
echo.
echo Vous tentez de vous connecter depuis:
echo   http://127.0.0.1:5506
echo.
echo SOLUTION RAPIDE (3 minutes):
echo.
echo 1. Ouvrez Google Cloud Console:
echo    https://console.cloud.google.com/apis/credentials
echo.
echo 2. Selectionnez le projet: "Prestige Shop Express New"
echo.
echo 3. Cliquez sur l'ID client OAuth:
echo    722931671687-fj2ph80jpqvlqmqnmc3aepdfqtsl7eqe.apps.googleusercontent.com
echo.
echo 4. Trouvez "Origines JavaScript autorisees"
echo.
echo 5. Cliquez "+ Ajouter URI" ou "+ ADD URI"
echo.
echo 6. AJOUTEZ CES DEUX ORIGINES:
echo    * http://localhost:5506
echo    * http://127.0.0.1:5506
echo.
echo 7. Cliquez "Enregistrer" ou "Save"
echo.
echo 8. ATTENDEZ 3-5 MINUTES!
echo.
echo 9. Videz le cache (Ctrl+Shift+Delete):
echo    Selectionnez "Cache" et "Cookies" et supprimez
echo.
echo 10. Rechargez la page (Ctrl+F5)
echo.
echo 11. Essayez de vous connecter avec Google
echo.
echo ==========================================
echo   Si ca fonctionne: Bravo! ✅
echo ==========================================
echo.
pause
