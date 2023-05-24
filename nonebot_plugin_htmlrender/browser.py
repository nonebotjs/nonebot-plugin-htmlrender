from _htmlrender import ctx
from js import Object
from pyodide.ffi import to_js


class get_new_page():
  async def __aenter__(self):
    self.page = await ctx.puppeteer.page()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.page.close()
    return

  def __init__(self, viewport={}):
    pass

  async def goto(self, url: str):
    if url.startswith('file://'):
      url = 'file://' + ctx.nonebot.resolvePath(url[7:])
    await self.page.goto(url)

  async def wait_for_timeout(self, wait: int):
    await self.page.waitForTimeout(wait)

  async def set_content(self, html, wait_until=None):
    await self.page.setContent(html, waitUntil=None if wait_until is None else 'networkidle0')

  async def screenshot(self, type='png', full_page=False, quality=None):
    base64 = await self.page.screenshot(to_js({
      'type': type,
      'encoding': 'base64',
      'fullPage': full_page,
      'quality': quality,
    }, dict_converter=Object.fromEntries))
    return "data:image/png;base64," + base64
