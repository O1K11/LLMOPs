# LLMOPs Engineer Take Home Assessment
How to run the python code:
1) clone the repo and navigate to the project directory.
2) make sure python 3.9 (or higher) is installed.
3) run the monitoring proof of concept:
   $ python part3_proofOfConcept.py

the script uses python's standard library and doesn't need any external LLM or API keys. 
it simulates LLM requests, applies configuration based A/B routing and logs telemetry and demonstrates provider failover using mock responses.

The JSON config drives provider selection, prompt versioning and A/B testing behavior at runtime.

Assumptions:
1) LLM responses are mocked to keep the focus on system behavior rather than API integration.
2) Average request size is approx 500 tokens (input + output)
3) Configuration files are versioned JSON stored in Git and loaded by the application at runtime.
4) Provider selection is driven entirely by configuration based A/B testing, not  hard coded priorities.
5) telemetry storage is file based for simplicity and demonstration purposes.

Future Improvements:
With more time I would extend this project by integrating real LLM APIs with secure key management and persisting telemetry to a database. I'd add dashboards for cost, latency and quality monitoring. I would also introduce a caching layer to reduce repeated calls, expand automated quality checks and add more experimentation and analysis to support long term optimization
