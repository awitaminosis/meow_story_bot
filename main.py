import asyncio
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

from logger.airtables import logger


from helper.app import dp, bot
from kernel.models.db_helper import db_helper
from places.controller import StateController

StateController().include_classes()


# Dummy HTTP handler for Render health checks
class RenderHealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Check telegram bot: @pi_meow_fir_story_bot")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress logs to keep Render output clean
        pass


def run_health_server():
    """Run a dummy HTTP server on $PORT for Render."""
    port = int(os.environ.get("PORT", 1000))  # Render sets $PORT; default for local dev
    server_address = ("0.0.0.0", port)  # Bind to all interfaces
    httpd = HTTPServer(server_address, RenderHealthHandler)
    # logger.info(f"Health server running on port {port}")
    httpd.serve_forever()


async def main():
    try:
        await db_helper.init_db()
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    # Start the health server in a background thread (non-blocking)
    server_thread = threading.Thread(target=run_health_server, daemon=True)
    server_thread.start()
    asyncio.run(main())
