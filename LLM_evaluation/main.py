from process_batches import process_all_batches

async def main():
    data_folder = r"Input Questions"
    output_folder = r"Output directory"
    models = [
        
        "openai/gpt-4o"
    ]

    # Process all batches and save results
    process_all_batches(data_folder, models, output_folder)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

