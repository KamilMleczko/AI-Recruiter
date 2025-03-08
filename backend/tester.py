from process_cv import start_process
import asyncio
#test how the backend works, output of agents in console.
async def main():
    cv_data = {
        "file_path": "data/senior.pdf"
    }
   
    ctx = await start_process(cv_data)
    count = 0
    while ctx["status"] == "no_jobs_matched" and count < 3:
        print(ctx["error"])
        count += 1
        ctx = await start_process(cv_data)
if __name__ == "__main__":
    asyncio.run(main())