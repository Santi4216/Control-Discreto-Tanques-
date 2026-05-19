@echo off
cd /d "d:\Documents\Archivos UMNG\8. OCTAVO SEMESTRE\3. Control y Laboratorio\Laboratorio\2. Informes\lab-control-Discreto"
git init
git config user.name "Santi4216"
git config user.email "your-email@example.com"
git add .
git commit -m "Initial commit: Lab control discreto project"
git branch -M main
git remote add origin https://github.com/Santi4216/Control-Discreto-Tanques-.git
git push -u origin main
pause
