import os
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# Playwright-কে হেডলেস মোডে চালানোর জন্য ভেরিয়েবল সেট করুন
os.environ["PLAYWRIGHT_HEADLESS"] = "1"
os.environ["DISPLAY"] = ":99"

load_dotenv()

async def run():
    async with async_playwright() as p:
        # হেডলেস মোডে ব্রাউজার চালু করুন
        browser = await p.chromium.launch(headless=True)
        
        # প্রোক্সি সেটআপ (যদি থাকে)
        proxy = {"server": os.getenv("PROXY")} if os.getenv("PROXY") else None
        context = await browser.new_context(proxy=proxy) if proxy else await browser.new_context()
        
        page = await context.new_page()

        # ইউটিউব ভিডিও লিংক (আপনার .env ফাইল থেকে নেওয়া)
        video_url = os.getenv("VIDEO_URL")
        if not video_url:
            print("[ERROR] VIDEO_URL not found in .env file!")
            await browser.close()
            return

        print(f"[INFO] Navigating to video: {video_url}")
        
        try:
            # সরাসরি ভিডিও লিংকে যান
            await page.goto(video_url, timeout=60000)
            
            # ভিডিও লোড হওয়ার জন্য অপেক্ষা
            await page.wait_for_timeout(5000)
            
            # ভিডিও প্লেয়ারে ক্লিক করে প্লে করুন (যদি প্রয়োজন হয়)
            try:
                await page.click("button.ytp-large-play-button")
                print("[INFO] Clicked play button")
            except:
                print("[INFO] Video started playing automatically")
            
            # ৩০ সেকেন্ড ভিডিও দেখুন (ভিউ কাউন্ট হওয়ার জন্য পর্যাপ্ত সময়)
            print("[INFO] Watching video for 30 seconds...")
            await page.wait_for_timeout(30000)
            
            print("[SUCCESS] Video view completed!")
            
        except Exception as e:
            print(f"[ERROR] Failed to play video: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
