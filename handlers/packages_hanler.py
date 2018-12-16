from tornado.web import RequestHandler


class PackagesHandler(RequestHandler):
    async def get(self):
        self.finish('handlers')

