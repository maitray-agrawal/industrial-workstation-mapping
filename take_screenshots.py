import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    docs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        
        try:
            # Home page
            await page.goto('http://127.0.0.1:5001')
            await page.wait_for_timeout(1000)
            await page.screenshot(path=os.path.join(docs_dir, 'homepage.png'))
            print("Homepage screenshot saved.")
            
            # Search Results page
            await page.goto('http://127.0.0.1:5001/search?q=tcf')
            await page.wait_for_timeout(1000)
            await page.screenshot(path=os.path.join(docs_dir, 'search_results.png'))
            print("Search results screenshot saved.")
            
        except Exception as e:
            print(f"Error taking screenshots: {e}")
            
        finally:
            await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
