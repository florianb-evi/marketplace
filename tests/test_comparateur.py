import asyncio
from playwright.async_api import async_playwright
U='file://'+__import__('os').path.abspath('prototypes/comparateur-reference.html')+''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w,h,name in [(1440,900,'d'),(390,844,'m')]:
            pg=await b.new_page(viewport={'width':w,'height':h})
            errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
            await pg.goto(U);await pg.wait_for_timeout(900)
            ov=lambda: pg.evaluate('document.documentElement.scrollWidth>document.documentElement.clientWidth')
            o1=await ov();await pg.screenshot(path=f'v5-{name}-10.png',full_page=True)
            first=await pg.evaluate("document.querySelector('.row b').textContent")
            await pg.fill('#qin','25');await pg.press('#qin','Enter');await pg.dispatch_event('#qin','change');await pg.wait_for_timeout(700)
            first25=await pg.evaluate("document.querySelector('.row b').textContent")
            tot=await pg.evaluate("document.querySelector('.row .tot b').textContent")
            await pg.screenshot(path=f'v5-{name}-25.png',full_page=True);o2=await ov()
            await pg.click('[data-det=dg]');await pg.wait_for_timeout(200)
            await pg.click(('[data-sort=delay]' if name=='d' else '[data-msort=delay]'));await pg.wait_for_timeout(600)
            firstDelay=await pg.evaluate("document.querySelector('.row b').textContent")
            await pg.click('#seg [data-tax=ttc]');await pg.wait_for_timeout(200)
            ttc=await pg.evaluate("document.querySelector('.ans .val b').textContent")
            print(name,'errors',errs,'overflow',o1,o2,'| q10 first:',first,'| q25 first:',first25,tot,'| by delay:',firstDelay,'| ttc ans:',ttc)
        await b.close()
asyncio.run(main())
