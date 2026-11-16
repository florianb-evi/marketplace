import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/marketplace/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w,h,name in [(1440,900,'d'),(390,844,'m')]:
            ctx=await b.new_context(viewport={'width':w,'height':h});pg=await ctx.new_page()
            errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
            ov=lambda: pg.evaluate('document.documentElement.scrollWidth>document.documentElement.clientWidth')
            res={}
            await pg.goto(U);await pg.wait_for_timeout(900);await pg.keyboard.press('Escape');await pg.wait_for_timeout(300)
            res['home']=await ov();await pg.screenshot(path=f'v6-home-{name}.png',full_page=True)
            # product gants via home
            await pg.click('[data-open-p=gants-jet-100]');await pg.wait_for_timeout(500)
            res['sheet']=await ov();res['hash']=await pg.evaluate('location.hash')
            first=await pg.evaluate("document.querySelector('.orow .oname').textContent.trim().split(' ').slice(0,2).join(' ')")
            await pg.fill('#cpQin','25');await pg.dispatch_event('#cpQin','change');await pg.wait_for_timeout(600)
            first25=await pg.evaluate("document.querySelector('.orow .oname').textContent.trim().split(' ').slice(0,2).join(' ')")
            await pg.screenshot(path=f'v6-sheet-{name}.png',full_page=True)
            # add from reco card
            await pg.click('.ans.reco .cta');await pg.wait_for_timeout(400);await pg.keyboard.press('Escape')
            # masks
            await pg.goto(U+'#produit-masque-3p');await pg.wait_for_timeout(600)
            res['mask']=await pg.evaluate("document.getElementById('cpName').textContent")+' / '+str(await pg.evaluate("document.querySelectorAll('.orow').length"))
            # sutures via category chir
            await pg.goto(U+'#categorie-chir');await pg.wait_for_timeout(600)
            res['chir']=await pg.evaluate("document.getElementById('catCount').textContent");res['chirOv']=await ov()
            await pg.screenshot(path=f'v6-chir-{name}.png',full_page=True)
            await pg.click('#view-cat [data-open-p=pgcl]');await pg.wait_for_timeout(500)
            res['pgcl']=await pg.evaluate("document.querySelectorAll('.orow').length")
            # ster
            await pg.goto(U+'#categorie-ster');await pg.wait_for_timeout(500)
            res['ster']=await pg.evaluate("document.getElementById('catCount').textContent")
            # cart warnings
            await pg.goto(U+'#panier');await pg.wait_for_timeout(600)
            res['warns']=await pg.evaluate("document.querySelectorAll('#view-cart .warnbox').length");res['cartOv']=await ov()
            await pg.screenshot(path=f'v6-cart-{name}.png',full_page=True)
            # pay blocked
            await pg.goto(U+'#paiement');await pg.wait_for_timeout(500)
            await pg.check('#cgv');await pg.click('#payBtn');await pg.wait_for_timeout(300)
            res['payBlock']=await pg.evaluate("!!document.querySelector('#payErr .errbox')")
            # resolve warnings
            await pg.goto(U+'#panier');await pg.wait_for_timeout(500)
            await pg.click('[data-accept-price]');await pg.wait_for_timeout(200)
            await pg.click('[data-split]');await pg.wait_for_timeout(200)
            res['warnsAfter']=await pg.evaluate("document.querySelectorAll('#view-cart .warnbox').length")
            res['lines']=await pg.evaluate("document.querySelectorAll('#view-cart .line').length")
            # virement error
            await pg.goto(U+'#paiement');await pg.wait_for_timeout(500)
            await pg.check('input[name=pay][value=vir]');await pg.check('#cgv');await pg.click('#payBtn');await pg.wait_for_timeout(300)
            res['virErr']=await pg.evaluate("document.querySelector('#payErr .errbox b')?.textContent")
            await pg.screenshot(path=f'v6-pay-{name}.png',full_page=True)
            await pg.click('[data-pay-cb]');await pg.click('#payBtn');await pg.wait_for_timeout(500)
            res['done']=await pg.evaluate("document.querySelector('.view.on').id")
            await pg.click('#view-done [data-go=orders]');await pg.wait_for_timeout(400)
            res['orders']=str(await pg.evaluate("document.querySelectorAll('#ordersBox .oc').length"))+' view '+str(await pg.evaluate("document.querySelector('.view.on').id"))
            await pg.screenshot(path=f'v6-orders-{name}.png',full_page=True)
            await pg.click('[data-reorder="EV-48211-2"]');await pg.wait_for_timeout(300);await pg.keyboard.press('Escape')
            # quote
            await pg.goto(U+'#devis-travaux');await pg.wait_for_timeout(500)
            await pg.click('[data-t="46"]');await pg.click('#qtSend');await pg.wait_for_timeout(300)
            res['quote']=await pg.evaluate("document.getElementById('qtSent').textContent.trim().slice(0,40)");res['qOv']=await ov()
            await pg.screenshot(path=f'v6-quote-{name}.png',full_page=True)
            # search
            await pg.goto(U+'#categorie-conso');await pg.wait_for_timeout(400)
            await pg.fill('#q','sutur');await pg.wait_for_timeout(200)
            res['sug']=await pg.evaluate("document.querySelectorAll('#sug button').length")
            await pg.press('#q','Enter');await pg.wait_for_timeout(400)
            res['searchView']=await pg.evaluate("document.querySelector('.view.on').id+' '+location.hash")
            print(name,'errors',errs);print(' ',res,'| gants q10:',first,'q25:',first25)
            await ctx.close()
        await b.close()
asyncio.run(main())
