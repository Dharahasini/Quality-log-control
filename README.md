Log Management System
Overview
The Log Management System is a Python-based application designed to manage and search log data from different APIs. It provides functionalities to log messages, search logs based on various criteria, and retrieve relevant log data.

How to Run the Project
To run the Log Management System, follow these steps:

Clone the repository:


git clone <repository-url>
Navigate to the project directory:


cd log-management-system
Install dependencies:


pip install -r requirements.txt
Run the main script:


python main.py
System Design
The Log Management System consists of two main components:

Log Ingestor:

Logs messages from different APIs into separate log files.
Each log entry includes log level, log string, timestamp, and optional metadata.
Log Query Interface:

Allows users to search logs based on log level, log message, timestamp range, and source (metadata).
Features Implemented
Logging Messages:

Log messages from different APIs.
Each log entry includes log level, log string, timestamp, and optional metadata.
Searching Logs:

Search logs based on log level, log message, timestamp range, and source (metadata).
Sample Queries:

Choose from sample queries provided in the interface.
Identified Issues
JSON Decode Error:

May occur when reading log files if the file is not properly formatted as JSON. This issue is handled by ensuring each line in the log file is a valid JSON object.
Case Sensitivity in Log Level Comparison:

Log level comparison is case-sensitive. To address this, log level comparison is converted to uppercase for consistency.
Future Enhancements
User Authentication:

Implement user authentication to restrict access to log data.
Data Visualization:

Add data visualization features to analyze log data graphically.
Real-time Logging:

Implement real-time logging capabilities for live monitoring of logs.
Advanced Search Filters:

Provide more advanced search filters such as searching by log ID or specific metadata fields.
Contributing
Contributions are welcome! Please feel free to fork the repository and submit pull requests with any improvements or bug fixes.
