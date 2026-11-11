# Rebuild da página /gut/ (besthealthadvice.online)
python3 _tools/atomicat2html.py _tools/gut/builder.json /tmp/gut.html --video-id 6af1f780ffc8452284b8696b --account dc39396a-fce0-4c6e-a398-29b2d73580ef --title "Gut Active" --max-width 100% --ratio 56.25% --delay 2277 --hide-from 2 --hide-to 6 --src-map "$(head -1 _tools/gut-active-build.txt)"
sed -i 's/<section class="ac-sec esconder o-9e645154"/<section id="kits" class="ac-sec esconder o-9e645154"/' /tmp/gut.html
sed -i '0,/<\/style>/s//html{scroll-behavior:smooth}<\/style>/' /tmp/gut.html
cp /tmp/gut.html besthealthadvice.online/public/gut/index.html
# depois do rebuild, reinserir a barra do operador antes de </body> (ver commit "dados da empresa")
