import logging
import json
import os
from datetime import datetime, timezone

class LogIngestor:
    def __init__(self):
        self.loggers = {}
        self.setup_logging()

    def setup_logging(self):
        # Setup loggers for different APIs
        for i in range(1, 10):
            logger = logging.getLogger(f"log{i}")
            logger.setLevel(logging.DEBUG)

            # Create file handler and set level to DEBUG
            file_handler = logging.FileHandler(f"log{i}.log")
            file_handler.setLevel(logging.DEBUG)

            # Create formatter
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

            # Add formatter to file handler
            file_handler.setFormatter(formatter)

            # Add file handler to logger
            logger.addHandler(file_handler)

            self.loggers[f"log{i}"] = logger

    def log(self, api_name, level, log_string, metadata={}):
        if api_name in self.loggers:
            logger = self.loggers[api_name]
            logger.log(level, json.dumps({
                "level": level,
                "log_string": log_string,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "metadata": metadata
            }))
        else:
            raise ValueError("Invalid API name")

class LogQueryInterface:
    def __init__(self, log_dir):
        self.log_dir = log_dir

    def search_logs(self, filters):
        print("Filters:", filters)  # Debug
        logs = []
        for log_file in os.listdir(self.log_dir):
            with open(os.path.join(self.log_dir, log_file), 'r') as f:
                for line in f:
                    try:
                        log = json.loads(line)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        continue
                    if self.matches_filters(log, filters):
                        logs.append(log)
        return logs

    def matches_filters(self, log, filters):
        for key, value in filters.items():
            if key == 'timestamp':
                log_time = datetime.fromisoformat(log[key].replace('Z', '+00:00'))
                if log_time < value[0] or log_time > value[1]:
                    return False
            elif key == 'level':
                if log[key] != value:
                    return False
            elif key == 'log_string':
                if value.lower() not in log[key].lower():
                    return False
            elif key == 'metadata.source':
                if log['metadata']['source'] != value:
                    return False
        return True

def main():
    ingestor = LogIngestor()
    query_interface = LogQueryInterface("logs")

    while True:
        print("\nChoose an option:")
        print("1. Log a message")
        print("2. Search logs")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            api_name = input("Enter API name (e.g., log1, log2, ...): ")
            level = input("Enter log level (info, error, success): ")
            log_string = input("Enter log message: ")
            source = input("Enter source: ")
            ingestor.log(api_name, getattr(logging, level.upper()), log_string, {"source": source})
            print("Message logged successfully!")

        elif choice == '2':
            print("\nSample Queries:")
            print("1. Find all logs with the level set to 'error'.")
            print("2. Search for logs with the message containing the term 'Failed to connect'.")
            print("3. Filter logs between two timestamps.")
            query_choice = input("Enter query number: ")

            if query_choice == '1':
                filters = {'level': 'error'}
            elif query_choice == '2':
                filters = {'log_string': 'Failed to connect'}
            elif query_choice == '3':
                start_time = input("Enter start timestamp (e.g., 2023-09-10T00:00:00Z): ")
                end_time = input("Enter end timestamp (e.g., 2023-09-15T23:59:59Z): ")
                start_time = datetime.fromisoformat(start_time)
                end_time = datetime.fromisoformat(end_time)
                filters = {'timestamp': (start_time, end_time)}
            else:
                print("Invalid query number.")
                continue

            results = query_interface.search_logs(filters)
            print("Results:", results)  # Debug
            if results:
                print("\nSearch results:")
                for log in results:
                    print(log)
            else:
                print("\nNo logs found matching the criteria.")

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
