#!/usr/bin/env python3
r"""
================================================================
 FACEBOOK SMART COMMENTER - 2 AKUN MODE
 2 akun × 5 reels × 3 komentar = 30 komentar total
================================================================

 CARA ISI ACCOUNT:
 Setiap akun butuh 2 cookie wajib: c_user & xs
 Datr & fr opsional (tapi lebih bagus kalau ada)

 Ambil dari: F12 → Application → Storage → Cookies → facebook.com
================================================================
"""

import asyncio
import random
import sys
from datetime import datetime
from playwright.async_api import async_playwright

# ============================================================
#  DAFTAR 2 AKUN UJI
# ============================================================
ACCOUNTS = [
    {
        "name": "Akun-1",
        "c_user": "GANTI",  # GANTI
        "xs":     "GANTI",  # GANTI
        "datr":   "",  # Opsional
        "fr":     "",  # Opsional
    },
    {
        "name": "Akun-2",
        "c_user": "GANTI",  # GANTI
        "xs":     "GANTI",  # GANTI
        "datr":   "",  # Opsional
        "fr":     "",  # Opsional
    },
]

# ============================================================
#  TARGET & PENGATURAN
# ============================================================
TARGET_USERNAME = "GANTI"

HEADLESS = False

TARGET_COMMENT_COUNT = 3         # 3 komentar per reel
MAX_POSTS            = 5         # 5 reel terbaru per akun

# Delay antar komentar dalam 1 reel
COMMENT_DELAY_MIN = 5
COMMENT_DELAY_MAX = 12

# Delay antar reel (setelah selesai 3 komentar di 1 reel)
REEL_DELAY_MIN = 20
REEL_DELAY_MAX = 35

# Delay antar akun (setelah 1 akun selesai semua reel)
ACCOUNT_DELAY_MIN = 60
ACCOUNT_DELAY_MAX = 120

AUTO_LIKE = True
SCROLL_COUNT = 5

# ============================================================
#  BANK KOMENTAR
# ============================================================
COMMENT_BANK = [
    "Keren banget! 🔥", "Mantap jiwa!", "Bagus banget!", "Wah keren!",
    "Top banget!", "Gokil! 🔥", "Kece parah!", "Mantul!", "Sip banget!",
    "Oke banget!", "Cakep!", "Nais!", "Jos gandos!", "Solid! 💯",
    "Keren abis!", "Mantap pol!", "Gila sih ini 🔥", "Wah wah wah!",
    "Nice!", "Good!", "Top markotop!", "Keren cuy!", "Mantul bgt!",
    "Bagus bgt!", "Ciamik!", "Ngeri!", "Pro!", "Gass!", "Lanjut!",
    "Sip!", "Oke!", "Yes!", "Gas!", "Legit!", "Mantab!", "Joss!",
    "Terima kasih sharingnya!", "Makasih infonya!", "Berguna banget ini!",
    "Sangat bermanfaat!", "Nice share! 🙏", "Lanjutkan! 💪",
    "Semangat terus!", "Sukses selalu!", "Tetap berkarya!",
    "Jangan berhenti bikin konten!", "Thanks infonya bro!",
    "Bermanfaat banget buat aku!", "Ini yang aku cari!",
    "Baru tau ini, makasih!", "Info penting nih, thanks!",
    "Setuju banget!", "Bener banget sih ini!", "Nah ini dia!", "Fakta! 💯",
    "Real banget!", "Relate parah!", "Sama banget!", "Gue banget!",
    "This is me!", "Auto setuju!", "Setuju 100%!", "Bener bgt!",
    "Nah kan bener!", "Gue juga gitu!", "Sama dong!", "Akurat banget!",
    "Fakta lapangan!", "Real no fek!", "No debat!", "Fix bener!",
    "Boleh share lebih detail?", "Menarik nih, lanjut terus!",
    "Penasaran kelanjutannya!", "Tunggu part 2-nya!",
    "Bikin konten kayak gini terus ya!", "Suka sama konten beginian!",
    "Kontennya berbobot!", "Quality content! 👏", "Underrated banget ini!",
    "Wajib viral nih!", "Kenapa gak viral dari kemarin?",
    "Ini sih harusnya trending!", "Gimana kelanjutannya?",
    "Update terus ya min!", "Ada tips lain gak?",
    "Bikin senyum sendiri 😊", "Senyum-senyum sendiri baca ini",
    "Good vibes banget! ✨", "Bikin hari jadi lebih baik!",
    "Fresh banget infonya!", "Energi positif! 💫", "Hati jadi hangat! ❤️",
    "Legit banget!", "Gemas! 🥰", "Lucu banget! 😄",
    "Haha ngakak!", "Ketawa sendiri!", "Ngakak baca ini!",
    "Bikin nggak bisa berhenti senyum!", "Suasana hati membaik!",
    "Konten kayak gini yang gue tunggu-tunggu!",
    "Baru nemu akun sebagus ini, langsung follow!",
    "Kenapa baru nemu akun ini sekarang 😭",
    "Algoritma Facebook akhirnya nunjukin konten berkualitas!",
    "Ini nih yang namanya konten berbobot!",
    "Sumpah ya, kontennya selalu relatable!",
    "Nggak pernah nyesel follow akun ini!",
    "Selalu ditunggu konten barunya!",
    "Bahasanya enak dibaca, isinya berbobot!",
    "Ini sih wajib banget di-bookmark!",
    "Nggak pernah bosen baca kontennya!",
    "Sering-sering bikin konten kayak gini ya!",
    "Kontennya ngena banget di hati!",
    "Yang beginian nih yang aku butuhin!",
    "Suka banget sama gaya bahasanya!",
    "Wkwkwk gokil!", "Anjir keren!", "Gila gila gila!",
    "Edan sih ini!", "Bener-bener dah!", "Yakin deh ini bagus!",
    "Top dah pokoknya!", "Nice one!", "Good job! 👍", "Well done!",
    "Salam dari Indonesia! 🇮🇩", "Semangat dari sini! 💪",
    "Ditunggu konten selanjutnya ya!", "Keep up the good work!",
    "Sukses terus buat kamu!", "Semoga makin sukses!",
    "Sukses selalu ya min!", "Ditunggu update-nya!",
    "Salam satu hobi!", "Salam kenal dari aku!",
]

# ============================================================
#  UTIL
# ============================================================
def log(msg, indent=0):
    print("   " * indent + msg, flush=True)


async def random_delay(min_sec, max_sec, label=""):
    delay = random.uniform(min_sec, max_sec)
    mins = int(delay // 60)
    secs = int(delay % 60)
    time_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"
    log(f"⏳ {label} menunggu {time_str}...", 1)
    await asyncio.sleep(delay)


# ============================================================
#  BROWSER SETUP (PER AKUN)
# ============================================================
async def setup_browser_for_account(playwright, account):
    log(f"🌐 Membuka browser untuk {account['name']}...")

    browser = await playwright.chromium.launch(
        headless=HEADLESS,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--start-maximized",
        ]
    )

    context = await browser.new_context(
        viewport={"width": 1366, "height": 900},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        locale="id-ID",
        timezone_id="Asia/Jakarta",
    )

    cookies = [
        {"name": "c_user", "value": account["c_user"],
         "domain": ".facebook.com", "path": "/",
         "httpOnly": False, "secure": True},
        {"name": "xs", "value": account["xs"],
         "domain": ".facebook.com", "path": "/",
         "httpOnly": True, "secure": True},
    ]
    if account.get("datr"):
        cookies.append({"name": "datr", "value": account["datr"],
                        "domain": ".facebook.com", "path": "/",
                        "httpOnly": True, "secure": True})
    if account.get("fr"):
        cookies.append({"name": "fr", "value": account["fr"],
                        "domain": ".facebook.com", "path": "/",
                        "httpOnly": True, "secure": True})

    await context.add_cookies(cookies)
    page = await context.new_page()

    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'languages', {get: () => ['id-ID', 'id', 'en-US']});
    """)

    return browser, context, page


async def check_login(page, account_name):
    log(f"🔐 [{account_name}] Memeriksa status login...")
    try:
        await page.goto("https://www.facebook.com/",
                        wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(5)

        for sel in [
            '[aria-label="Facebook"]',
            '[role="navigation"]',
            'div[aria-label="Buat postingan"]',
        ]:
            try:
                await page.wait_for_selector(sel, timeout=4000, state="attached")
                log(f"✅ [{account_name}] Berhasil login!", 1)
                return True
            except Exception:
                continue

        log(f"⚠️  [{account_name}] Tidak yakin login, coba lanjut...", 1)
        return True
    except Exception as e:
        log(f"❌ [{account_name}] Gagal buka Facebook: {e}", 1)
        return False


# ============================================================
#  KUMPULKAN LINK REEL
# ============================================================
async def collect_reel_links(page, username, max_links):
    log(f"📋 Mencari REELS di @{username}...")
    reel_links = set()

    urls_to_try = [
        f"https://www.facebook.com/{username}/reels_tab",
        f"https://www.facebook.com/{username}/videos",
        f"https://www.facebook.com/{username}",
    ]

    for target_url in urls_to_try:
        if len(reel_links) >= max_links:
            break

        log(f"\n   🔗 Coba: {target_url}", 1)
        try:
            await page.goto(target_url, wait_until="domcontentloaded", timeout=45000)
            await asyncio.sleep(5)

            try:
                await page.keyboard.press("Escape")
                await asyncio.sleep(1)
            except:
                pass

            for i in range(SCROLL_COUNT):
                await page.evaluate("window.scrollBy(0, window.innerHeight * 0.9)")
                await asyncio.sleep(2)

            links = await page.evaluate("""
                () => {
                    const anchors = document.querySelectorAll('a[href]');
                    const reels = new Set();
                    for (const a of anchors) {
                        const h = a.getAttribute('href');
                        if (!h) continue;
                        const match = h.match(/\\/reel\\/(\\d+)/);
                        if (match) {
                            reels.add('https://www.facebook.com/reel/' + match[1] + '/');
                        }
                    }
                    return Array.from(reels);
                }
            """)

            log(f"      Ditemukan {len(links)} link /reel/", 1)
            for l in links:
                reel_links.add(l)
                if len(reel_links) >= max_links:
                    break

        except Exception as e:
            log(f"      ❌ Gagal: {e}", 1)
            continue

    reel_links = list(reel_links)[:max_links]
    log(f"\n   ✅ Total {len(reel_links)} link reel", 1)
    for i, l in enumerate(reel_links):
        log(f"      [{i}] {l}", 1)

    return reel_links


# ============================================================
#  LIKE
# ============================================================
async def like_post(page):
    try:
        unlike = await page.query_selector('div[aria-label="Unlike"], div[aria-label="Batal Suka"]')
        if unlike:
            log("❤️  Sudah di-like", 2)
            return True

        for sel in ['div[aria-label="Like"]', 'div[aria-label="Suka"]']:
            try:
                btn = await page.query_selector(sel)
                if btn and await btn.is_visible():
                    await btn.click()
                    await asyncio.sleep(1.5)
                    log("❤️  Like berhasil", 2)
                    return True
            except:
                continue
    except:
        pass
    return False


# ============================================================
#  BUKA PANEL KOMENTAR
# ============================================================
async def open_comment_sidebar(page):
    log("   → Buka panel komentar...", 2)

    comment_btn_selectors = [
        'div[aria-label="Comment"]',
        'div[aria-label="Komentari"]',
        'div[aria-label="Beri komentar"]',
        'div[role="button"][aria-label*="Comment"]',
        'div[role="button"][aria-label*="Komentar"]',
        '[aria-label*="Comment" i][role="button"]',
        '[aria-label*="Komentar" i][role="button"]',
    ]

    for sel in comment_btn_selectors:
        try:
            btns = await page.query_selector_all(sel)
            for btn in btns:
                if await btn.is_visible():
                    await btn.click()
                    log(f"   ✅ Tombol komentar diklik", 2)
                    await asyncio.sleep(3)
                    return True
        except:
            continue

    try:
        clicked = await page.evaluate("""
            () => {
                const candidates = document.querySelectorAll(
                    '[aria-label*="Comment" i], [aria-label*="Komentar" i]'
                );
                for (let el of candidates) {
                    if (el.offsetParent !== null) {
                        el.click();
                        return true;
                    }
                }
                return false;
            }
        """)
        if clicked:
            log(f"   ✅ Tombol komentar diklik (JS)", 2)
            await asyncio.sleep(3)
            return True
    except:
        pass

    log("   ⚠️  Tidak bisa buka panel komentar", 2)
    return False


# ============================================================
#  CARI KOTAK INPUT KOMENTAR
# ============================================================
async def find_comment_input(page):
    selectors = [
        'div[contenteditable="true"][role="textbox"][aria-label*="Comment as"]',
        'div[contenteditable="true"][role="textbox"][aria-label*="Komentar sebagai"]',
        'div[contenteditable="true"][role="textbox"][aria-label*="Write a comment"]',
        'div[contenteditable="true"][role="textbox"][aria-label*="Tulis komentar"]',
        'div[contenteditable="true"][role="textbox"][aria-label*="komentar" i]',
        'div[contenteditable="true"][role="textbox"][aria-label*="comment" i]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"]',
    ]
    exclude = ["cari", "search", "pesan", "message", "chat"]

    for sel in selectors:
        try:
            boxes = await page.query_selector_all(sel)
            for b in boxes:
                if not await b.is_visible():
                    continue
                aria = (await b.get_attribute("aria-label") or "").lower()
                if any(x in aria for x in exclude):
                    continue
                return b
        except:
            continue
    return None


# ============================================================
#  KIRIM KOMENTAR
# ============================================================
async def send_comment(page, text):
    box = await find_comment_input(page)
    if not box:
        log("   ❌ Kotak komentar tidak ditemukan", 2)
        return False

    try:
        await page.evaluate("""(el) => {
            el.focus();
            const sel = window.getSelection();
            const range = document.createRange();
            range.selectNodeContents(el);
            sel.removeAllRanges();
            sel.addRange(range);
        }""", box)
        await asyncio.sleep(0.5)

        await page.keyboard.press("Control+A")
        await page.keyboard.press("Delete")
        await asyncio.sleep(0.3)

        await page.keyboard.type(text, delay=random.randint(40, 70))
        await asyncio.sleep(1.2)
        log(f"   📝 Diketik: \"{text[:40]}\"", 2)
    except Exception as e:
        log(f"   ❌ Gagal ketik: {e}", 2)
        return False

    try:
        await page.keyboard.press("Enter")
        await asyncio.sleep(3)
    except Exception as e:
        log(f"   ❌ Gagal Enter: {e}", 2)
        return False

    try:
        current = await page.evaluate(
            "(el) => el.innerText || el.textContent || ''", box
        )
        if not current or current.strip() == "":
            log("   ✅ Komentar TERKIRIM!", 2)
            return True
        else:
            await page.keyboard.press("Enter")
            await asyncio.sleep(2)
            current = await page.evaluate(
                "(el) => el.innerText || el.textContent || ''", box
            )
            if not current or current.strip() == "":
                log("   ✅ Komentar TERKIRIM!", 2)
                return True
            return False
    except:
        return True


# ============================================================
#  PROSES SATU REEL
# ============================================================
async def process_reel(page, reel_url, num, total, comments_count):
    print(f"\n{'='*60}")
    print(f"📌 REEL {num}/{total}")
    print(f"🔗 {reel_url}")
    print(f"{'='*60}")

    loaded = False
    for attempt in range(3):
        try:
            log(f"   🌐 Load (attempt {attempt+1}/3)...", 1)
            await page.goto(reel_url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(8)
            loaded = True
            break
        except Exception as e:
            log(f"   ⚠️  Timeout attempt {attempt+1}, retry...", 1)
            await asyncio.sleep(3)

    if not loaded:
        log(f"❌ Gagal load setelah 3x coba", 1)
        return 0

    if "login" in page.url.lower() or "checkpoint" in page.url.lower():
        log("❌ Redirect login", 1)
        return 0

    if AUTO_LIKE:
        await like_post(page)
        await asyncio.sleep(1)

    if not await open_comment_sidebar(page):
        log("⚠️  Panel komentar gagal dibuka", 1)

    await asyncio.sleep(2)

    used = set()
    sent = 0

    for i in range(comments_count):
        log(f"💭 Komentar {i+1}/{comments_count}", 2)

        pool = [c for c in COMMENT_BANK if c not in used]
        if not pool:
            used.clear()
            pool = COMMENT_BANK[:]

        text = random.choice(pool)
        used.add(text)

        box = await find_comment_input(page)
        if not box:
            log("   → Coba buka panel komentar lagi...", 2)
            await open_comment_sidebar(page)
            await asyncio.sleep(2)

        if await send_comment(page, text):
            sent += 1
        else:
            log("   ⚠️  Gagal kirim", 2)

        if i < comments_count - 1:
            await random_delay(COMMENT_DELAY_MIN, COMMENT_DELAY_MAX, "antar komentar:")

    log(f"📊 Reel {num}: {sent}/{comments_count} berhasil", 1)
    return sent


# ============================================================
#  PROSES SATU AKUN
# ============================================================
async def process_account(playwright, account, account_idx, total_accounts):
    print("\n" + "█" * 60)
    print(f"█  AKUN {account_idx}/{total_accounts}: {account['name']}")
    print(f"█  c_user: {account['c_user']}")
    print("█" * 60)

    browser = None
    account_success = 0
    account_target = MAX_POSTS * TARGET_COMMENT_COUNT

    try:
        browser, context, page = await setup_browser_for_account(playwright, account)

        if not await check_login(page, account["name"]):
            print(f"\n❌ [{account['name']}] Login gagal - skip akun ini")
            return 0, 0

        reel_links = await collect_reel_links(page, TARGET_USERNAME, MAX_POSTS)
        if not reel_links:
            print(f"\n⚠️  [{account['name']}] Tidak ada reel ditemukan")
            return 0, 0

        print(f"\n✅ [{account['name']}] Siap memproses {len(reel_links)} reels\n")

        for i, url in enumerate(reel_links, 1):
            sent = await process_reel(
                page, url, i, len(reel_links), TARGET_COMMENT_COUNT
            )
            account_success += sent

            if i < len(reel_links):
                await random_delay(REEL_DELAY_MIN, REEL_DELAY_MAX, "antar reel:")

        print(f"\n{'─'*60}")
        print(f"📊 [{account['name']}] SELESAI: {account_success}/{account_target} komentar")
        print(f"{'─'*60}")

    except Exception as e:
        print(f"\n❌ [{account['name']}] Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if browser:
            try:
                await browser.close()
                log(f"🔒 [{account['name']}] Browser ditutup", 1)
            except:
                pass

    return account_success, account_target


# ============================================================
#  MAIN
# ============================================================
async def main():
    print("=" * 60)
    print("  FACEBOOK MULTI-ACCOUNT COMMENTER (2 AKUN)")
    print("=" * 60)
    print(f"  Target        : {TARGET_USERNAME}")
    print(f"  Total akun    : {len(ACCOUNTS)}")
    print(f"  Reels/akun    : {MAX_POSTS}")
    print(f"  Komentar/reel : {TARGET_COMMENT_COUNT}")
    print(f"  Total target  : {len(ACCOUNTS) * MAX_POSTS * TARGET_COMMENT_COUNT} komentar")
    print()

    # Validasi akun
    valid_accounts = [a for a in ACCOUNTS if a["c_user"] and not a["c_user"].startswith("GANTI")]
    if not valid_accounts:
        print("❌ Tidak ada akun valid!")
        print("   Isi c_user & xs di bagian ACCOUNTS")
        return

    if len(valid_accounts) < len(ACCOUNTS):
        print(f"⚠️  Hanya {len(valid_accounts)} dari {len(ACCOUNTS)} akun yang valid")
        print(f"   Akun yang akan diproses:")
        for a in valid_accounts:
            print(f"     - {a['name']} (c_user: {a['c_user']})")
        print()

    confirm = input("Lanjutkan? (ketik 'ya'): ").strip().lower()
    if confirm != "ya":
        print("Dibatalkan.")
        return

    print()
    start_time = datetime.now()

    async with async_playwright() as p:
        grand_total_success = 0
        grand_total_target = 0
        account_results = []

        for idx, account in enumerate(valid_accounts, 1):
            success, target = await process_account(
                p, account, idx, len(valid_accounts)
            )
            grand_total_success += success
            grand_total_target += target
            account_results.append({
                "name": account["name"],
                "c_user": account["c_user"],
                "success": success,
                "target": target,
            })

            # Jeda antar akun (kecuali akun terakhir)
            if idx < len(valid_accounts):
                print(f"\n{'█'*60}")
                print(f"█  JEDA ANTAR AKUN...")
                print(f"{'█'*60}")
                await random_delay(ACCOUNT_DELAY_MIN, ACCOUNT_DELAY_MAX, "antar akun:")

        # === RINGKASAN AKHIR ===
        elapsed = (datetime.now() - start_time).total_seconds()
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)

        print("\n" + "█" * 60)
        print("█  📊 RINGKASAN AKHIR")
        print("█" * 60)

        for r in account_results:
            rate = (r["success"] / r["target"] * 100) if r["target"] > 0 else 0
            print(f"  {r['name']:10s} ({r['c_user']}): "
                  f"{r['success']}/{r['target']} ({rate:.0f}%)")

        print("─" * 60)
        total_rate = (grand_total_success / grand_total_target * 100) if grand_total_target > 0 else 0
        print(f"  TOTAL      : {grand_total_success}/{grand_total_target} ({total_rate:.1f}%)")
        print(f"  Waktu      : {mins}m {secs}s")
        print("█" * 60)

        print("\n🎉 Selesai!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDibatalkan.")
        sys.exit(0)