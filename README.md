# funis

Uma pasta por domínio. Cada pasta é um projeto separado na Cloudflare (Workers com static assets).

Estrutura de cada domínio:
- `<dominio>/wrangler.jsonc` → config do projeto (nome do projeto na Cloudflare)
- `<dominio>/public/` → páginas publicadas (ex.: `public/burntide/index.html` vira `/burntide/`)

Domínios:
- `besthealthadvice.online/` → projeto `besthealthadvice`
- `theamericanhealthjournal.online/` → projeto `theamericanhealthjournal`
- `thebakingsodarecipe.online/` → projeto `thebakingsodarecipe`
