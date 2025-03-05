from process_cv import start_process
import asyncio

async def main():
    cv_data = {
        "file_path": "data/senior.pdf"
    }
    await start_process(cv_data)

if __name__ == "__main__":
    asyncio.run(main())