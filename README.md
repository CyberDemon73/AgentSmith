# AgentSmith: User Agent Generator

**AgentSmith** is a lightweight and reliable Python tool designed to generate random, valid user agent strings. It uses a JSON configuration file (`user_agents.json`) to control the variance of browsers, versions, and operating systems. Perfect for web scraping, testing, or simulating different browser environments, **AgentSmith** is streamlined for simplicity, reliability, and easy integration.

---

## Features

- **Single User Agent Generation**: Generates one random user agent string per run.
- **Streamlined Output**: Prints only the generated user agent string to `stdout` without additional clutter.
- **Error Handling**: Directs error messages to `stderr` and returns appropriate exit codes (`0` for success, `1` for error).
- **Validation**: Ensures all generated user agents are valid and properly formatted.
- **Customizable Configuration**: Uses a JSON file (`user_agents.json`) to define the variance of browsers, versions, and operating systems.

---

## Installation

No installation is required! Simply download the `agent_smith.py` script and ensure you have Python 3.x installed.

```bash
git clone https://github.com/CyberDemon73/AgentSmith.git
cd agent-smith
```

---

## Usage

### 1. Run the Script

Run the script from the command line:

```bash
python AgentSmith.py
```

By default, the script looks for a `user_agents.json` file in the current directory. You can also specify a custom JSON file:

```bash
python AgentSmith.py path/to/custom_user_agents.json
```

### 2. Output

The script will output a randomly generated user agent string to `stdout`, such as:

```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36
```

If an error occurs, it will be printed to `stderr`, and the script will exit with a non-zero status code.

---

## Integration Guide

You can integrate **AgentSmith** into your projects in two ways:

### 1. Call as a Subprocess

Use Python's `subprocess` module to call **AgentSmith** and capture its output:

```python
import subprocess

try:
    result = subprocess.run(
        ['python', 'agent_smith.py'],
        capture_output=True, text=True, check=True
    )
    user_agent = result.stdout.strip()
    print(f"Using user agent: {user_agent}")
except subprocess.CalledProcessError as e:
    print(f"Error generating user agent: {e.stderr}")
```

### 2. Import Directly

Import the `load_user_agents` and `generate_user_agent` functions directly into your Python script:

```python
from agent_smith import load_user_agents, generate_user_agent

try:
    data = load_user_agents('user_agents.json')  # Default file
    user_agent = generate_user_agent(data)
    print(f"Using user agent: {user_agent}")
except Exception as e:
    print(f"Error: {e}")
```

---

## Configuration

The `user_agents.json` file controls the variance of the generated user agents. Here's an example structure:

```json
{
    "browsers": [
        {
            "name": "Chrome",
            "versions": ["90.0.4430.212", "91.0.4472.124"],
            "os": [
                {
                    "name": "Windows",
                    "versions": ["10.0", "8.1"]
                },
                {
                    "name": "Mac OS",
                    "versions": ["10_15_7", "11_2_3"]
                }
            ]
        },
        {
            "name": "Firefox",
            "versions": ["89.0", "90.0"],
            "os": [
                {
                    "name": "Linux",
                    "versions": ["x86_64"]
                }
            ]
        }
    ]
}
```

---

## Error Handling

**AgentSmith** provides robust error handling with clear error messages and appropriate exit codes:

- **Exit Code `0`**: Successfully generated a user agent.
- **Exit Code `1`**: An error occurred (e.g., invalid JSON, file not found, or invalid user agent).

Errors are printed to `stderr`, making it easy to separate them from the generated user agent string.

---

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you'd like to change.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/CyberDemon73/AgentSmith/issues).
