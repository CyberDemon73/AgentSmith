import json
import random
import os
import re
import sys

class UserAgentError(Exception):
    """Base exception class for user agent generation errors"""
    pass

class InvalidJSONFormatError(UserAgentError):
    """Exception raised when JSON format is invalid"""
    pass

class FileNotFoundError(UserAgentError):
    """Exception raised when file is not found"""
    pass

class EmptyDataError(UserAgentError):
    """Exception raised when data is empty"""
    pass

class InvalidUserAgentError(UserAgentError):
    """Exception raised when a generated user agent is invalid"""
    pass

def validate_json_structure(data):
    """Validate the structure of the JSON data"""
    if not isinstance(data, dict):
        raise InvalidJSONFormatError("JSON data must be a dictionary")
    
    if "browsers" not in data:
        raise InvalidJSONFormatError("JSON data must contain a 'browsers' key")
    
    if not isinstance(data["browsers"], list) or len(data["browsers"]) == 0:
        raise InvalidJSONFormatError("'browsers' must be a non-empty list")
    
    for i, browser in enumerate(data["browsers"]):
        if not isinstance(browser, dict):
            raise InvalidJSONFormatError(f"Browser at index {i} must be a dictionary")
        
        # Check required fields
        required_fields = ["name", "versions", "os"]
        for field in required_fields:
            if field not in browser:
                raise InvalidJSONFormatError(f"Browser at index {i} is missing '{field}' field")
        
        # Validate versions
        if not isinstance(browser["versions"], list) or len(browser["versions"]) == 0:
            raise InvalidJSONFormatError(f"Browser '{browser.get('name', f'at index {i}')}' must have non-empty 'versions' list")
        
        # Validate OS entries
        if not isinstance(browser["os"], list) or len(browser["os"]) == 0:
            raise InvalidJSONFormatError(f"Browser '{browser.get('name', f'at index {i}')}' must have non-empty 'os' list")
        
        for j, os_info in enumerate(browser["os"]):
            if not isinstance(os_info, dict):
                raise InvalidJSONFormatError(f"OS at index {j} for browser '{browser.get('name', f'at index {i}')}' must be a dictionary")
            
            if "name" not in os_info:
                raise InvalidJSONFormatError(f"OS at index {j} for browser '{browser.get('name', f'at index {i}')}' is missing 'name' field")
            
            if "versions" not in os_info or not isinstance(os_info["versions"], list) or len(os_info["versions"]) == 0:
                raise InvalidJSONFormatError(f"OS '{os_info.get('name', f'at index {j}')}' for browser '{browser.get('name', f'at index {i}')}' must have non-empty 'versions' list")

def load_user_agents(json_file):
    """Load user agents from JSON file with error handling"""
    try:
        # Check if file exists
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"File not found: {json_file}")
        
        # Check if file is readable
        if not os.access(json_file, os.R_OK):
            raise PermissionError(f"Permission denied: Cannot read {json_file}")
        
        # Open and parse JSON file
        with open(json_file, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                raise InvalidJSONFormatError(f"Invalid JSON format: {str(e)}")
        
        # Validate JSON structure
        validate_json_structure(data)
        
        return data
        
    except Exception as e:
        if isinstance(e, UserAgentError):
            raise
        else:
            raise UserAgentError(f"Error loading user agents: {str(e)}")

def get_os_string(os_name, os_version):
    """Format OS string based on OS name and version"""
    try:
        if not isinstance(os_name, str) or not isinstance(os_version, str):
            raise TypeError("OS name and version must be strings")
        
        if os_name == "Windows":
            return f"Windows NT {os_version}; Win64; x64"
        elif os_name == "Mac OS":
            if "_" in os_version:  # Format: 10_15_7
                return f"Macintosh; Intel Mac OS X {os_version}"
            else:  # Format: 10.15
                formatted_version = os_version.replace(".", "_")
                return f"Macintosh; Intel Mac OS X {formatted_version}"
        elif os_name == "Linux":
            return f"X11; Linux {os_version}"
        else:
            return f"{os_name} {os_version}"
    except Exception as e:
        raise UserAgentError(f"Error formatting OS string: {str(e)}")

def validate_user_agent(user_agent):
    """Validate generated user agent format"""
    # Check for basic user agent structure
    if not user_agent.startswith("Mozilla/5.0"):
        return False
    
    # Check for parentheses balance
    if user_agent.count('(') != user_agent.count(')'):
        return False
    
    # Check for minimum length
    if len(user_agent) < 30:
        return False
    
    # Check if it contains basic browser info
    browser_patterns = ["Chrome", "Firefox", "Safari", "Edg"]
    if not any(pattern in user_agent for pattern in browser_patterns):
        return False
    
    # Check for common OS strings
    os_patterns = ["Windows", "Mac OS X", "Linux", "X11"]
    if not any(pattern in user_agent for pattern in os_patterns):
        return False
    
    return True

def generate_user_agent(data):
    """Generate a single feasible user agent"""
    try:
        if not data or not isinstance(data, dict) or "browsers" not in data:
            raise EmptyDataError("Invalid or empty data structure")
        
        if not data["browsers"]:
            raise EmptyDataError("No browser data available")
        
        # Filter out browsers with no OS data or invalid versions
        feasible_browsers = [
            browser for browser in data['browsers']
            if browser.get('os') and isinstance(browser.get('versions'), list) and browser['versions']
        ]
        
        if not feasible_browsers:
            raise EmptyDataError("No feasible browser data available")
        
        # Select a random browser from the feasible list
        browser = random.choice(feasible_browsers)
        browser_name = browser['name']
        browser_version = random.choice(browser['versions'])
        
        # Filter out OS entries with no versions or invalid data
        feasible_os = [
            os_info for os_info in browser['os']
            if os_info.get('versions') and isinstance(os_info['versions'], list) and os_info['versions']
        ]
        
        if not feasible_os:
            raise EmptyDataError(f"No feasible OS data available for browser: {browser_name}")
        
        # Select a random OS from the feasible list
        os_info = random.choice(feasible_os)
        os_name = os_info['name']
        os_version = random.choice(os_info['versions'])
        
        # Generate the user agent string based on the browser
        if browser_name == "Chrome":
            user_agent = f"Mozilla/5.0 ({get_os_string(os_name, os_version)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{browser_version} Safari/537.36"
        elif browser_name == "Firefox":
            user_agent = f"Mozilla/5.0 ({get_os_string(os_name, os_version)}; rv:{browser_version}) Gecko/20100101 Firefox/{browser_version}"
        elif browser_name == "Safari":
            user_agent = f"Mozilla/5.0 ({get_os_string(os_name, os_version)}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{browser_version} Safari/605.1.15"
        elif browser_name == "Edge":
            user_agent = f"Mozilla/5.0 ({get_os_string(os_name, os_version)}) AppleWebKit/537.36 (KHTML, like Gecko) Edg/{browser_version}"
        else:
            user_agent = f"Mozilla/5.0 ({get_os_string(os_name, os_version)}) AppleWebKit/537.36 (KHTML, like Gecko) {browser_name}/{browser_version}"
        
        # Validate the generated user agent
        if not validate_user_agent(user_agent):
            raise InvalidUserAgentError(f"Generated invalid user agent: {user_agent}")
        
        return user_agent
    
    except Exception as e:
        if isinstance(e, UserAgentError):
            raise
        else:
            raise UserAgentError(f"Error generating user agent: {str(e)}")

def main():
    """Main function to generate a single user agent"""
    try:
        # Get JSON file path from command line or use default
        json_file = sys.argv[1] if len(sys.argv) > 1 else 'user_agents.json'
        
        # Load and validate data
        data = load_user_agents(json_file)
        
        # Generate a user agent
        user_agent = generate_user_agent(data)
        
        # Print only the user agent string for easy integration
        print(user_agent)
        return 0
            
    except UserAgentError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())