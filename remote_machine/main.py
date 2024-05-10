import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileSystemEvent

import pandas as pd 

class FileProcessor:
    def __init__(self, path: str):
        self.path = path

    def process(self) -> bytes:
        df = pd.read_excel(self.path)
        csv_file = df.to_csv()
        csv_file_bytes = csv_file.encode('utf-8')

        return csv_file_bytes

class XslFileEventHandler(PatternMatchingEventHandler):
    def __init__(self):
        #include only the excel files, the events for other file types are ignored
        super().__init__(['*.xls', '*.xlsx', '*.ods'], ignore_directories=True)

    def on_created(self, event: FileSystemEvent) -> None:
        fileProcessor = FileProcessor(event.src_path)
        csv_file_bytes = fileProcessor.process()

        # show only the first 10 byte of a CSV
        csv_overview = str(csv_file_bytes[0:10]) + ('...' if len(csv_file_bytes) > 10 else '')
        logging.info(f'Excel file found: {event.src_path}: {csv_overview}')

        # TODO: publish on kafka

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    logging.info(f'Start watching directory {path!r}')

    event_handler = XslFileEventHandler()
    
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()