import asyncio
import os
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright

async def main():
    root_dir = Path(__file__).resolve().parent.parent
    video_dir = root_dir / "scripts" / "videos"
    video_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = root_dir / "docs" / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    print("Iniciando Playwright Chromium...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            record_video_dir=str(video_dir),
            record_video_size={"width": 1080, "height": 720},
            viewport={"width": 1080, "height": 720},
            device_scale_factor=2,
        )
        page = await context.new_page()

        print("Navegando para http://localhost:3020...")
        await page.goto("http://localhost:3020", wait_until="networkidle")
        await asyncio.sleep(2)

        # 1. Localizar sugestão Taxa Selic e clicar
        print("Interagindo com sugestão rápida 'Taxa Selic'...")
        selic_btn = page.locator("button:has-text('Taxa Selic')").first
        if await selic_btn.is_visible():
            await selic_btn.hover()
            await asyncio.sleep(0.8)
            await selic_btn.click()
            await asyncio.sleep(1.2)

            # Enviar
            send_btn = page.locator("button:has-text('Enviar')").first
            await send_btn.click()
            print("Mensagem enviada, aguardando resposta...")
            await asyncio.sleep(4)

        # 2. Localizar sugestão 'Meta de Poupança' e clicar
        print("Interagindo com sugestão rápida 'Meta de Poupança'...")
        poupanca_btn = page.locator("button:has-text('Meta de Poupança')").first
        if await poupanca_btn.is_visible():
            await poupanca_btn.hover()
            await asyncio.sleep(0.8)
            await poupanca_btn.click()
            await asyncio.sleep(1.2)

            send_btn = page.locator("button:has-text('Enviar')").first
            await send_btn.click()
            print("Mensagem enviada, aguardando resposta...")
            await asyncio.sleep(4)

        # Pausa final para visualização
        await asyncio.sleep(2)

        print("Fechando gravação...")
        await context.close()
        await browser.close()

    # Encontrar vídeo gerado
    video_files = sorted(video_dir.glob("*.webm"), key=os.path.getmtime)
    if not video_files:
        raise RuntimeError("Nenhum arquivo de vídeo foi gerado pelo Playwright.")

    latest_video = video_files[-1]
    output_gif = assets_dir / "demo.gif"
    print(f"Convertendo {latest_video} para {output_gif} com ffmpeg...")

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(latest_video),
        "-vf",
        "fps=12,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        str(output_gif),
    ]

    subprocess.run(ffmpeg_cmd, check=True)
    print(f"GIF gerado com sucesso: {output_gif}")

if __name__ == "__main__":
    asyncio.run(main())
