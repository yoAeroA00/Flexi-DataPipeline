from app.main import app

if __name__ == "__main__":
    import os
    import asyncio
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    if os.name != 'nt':
        try:
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
            print("Event loop changed to uvloop.")
        except Exception as e:
            print(f"ERROR Changing event loop to uvloop : {e}")

    config = Config()
    hc_config = config.from_toml(os.path.join(os.path.dirname(__file__), 'app/core/config/hypercorn/config.toml'))

    asyncio.run(serve(app=app, config=hc_config, shutdown_trigger=lambda: asyncio.Future(), mode='asgi'))
