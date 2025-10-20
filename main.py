# ============================================================================
# PYTHON PROJECT COLLECTION
# Level 1 (Basic), Level 2 (Intermediate), Level 3 (Advanced)
# ============================================================================

import random
import json
import csv
import os
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet

# ============================================================================
# LEVEL 1 - BASIC
# ============================================================================

# Task 1: Simple Calculator
def calculator():
    """Simple calculator with four basic operations"""
    
    def add(x, y):
        return x + y
    
    def subtract(x, y):
        return x - y
    
    def multiply(x, y):
        return x * y
    
    def divide(x, y):
        if y == 0:
            raise ValueError("Error: Division by zero is not allowed!")
        return x / y
    
    print("\n=== Simple Calculator ===")
    print("Operations:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    
    try:
        choice = input("\nSelect operation (1/2/3/4): ")
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        operations = {
            '1': (add, '+'),
            '2': (subtract, '-'),
            '3': (multiply, '*'),
            '4': (divide, '/')
        }
        
        if choice in operations:
            func, symbol = operations[choice]
            result = func(num1, num2)
            print(f"\nResult: {num1} {symbol} {num2} = {result}")
        else:
            print("Invalid operation choice!")
            
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Task 2: Number Guessing Game
def number_guessing_game():
    """Number guessing game with limited attempts"""
    
    print("\n=== Number Guessing Game ===")
    print("I'm thinking of a number between 1 and 100.")
    
    secret_number = random.randint(1, 100)
    max_attempts = 10
    attempts = 0
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"\nAttempt {attempts + 1}/{max_attempts} - Enter your guess: "))
            attempts += 1
            
            if guess < 1 or guess > 100:
                print("Please enter a number between 1 and 100!")
                continue
            
            if guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print(f"\n🎉 Congratulations! You guessed it in {attempts} attempts!")
                return
                
        except ValueError:
            print("Invalid input! Please enter a number.")
    
    print(f"\n😞 Game Over! The number was {secret_number}")


# Task 3: Word Counter
def word_counter():
    """Count words in a text file"""
    
    print("\n=== Word Counter ===")
    filename = input("Enter the filename to count words: ")
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            words = content.split()
            word_count = len(words)
            
            print(f"\nFile: {filename}")
            print(f"Total words: {word_count}")
            print(f"Total characters: {len(content)}")
            print(f"Total lines: {len(content.splitlines())}")
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
    except Exception as e:
        print(f"An error occurred: {e}")


# ============================================================================
# LEVEL 2 - INTERMEDIATE
# ============================================================================

# Task 1: To-Do List Application
class TodoList:
    """Command-line to-do list application"""
    
    def __init__(self, filename='todos.json'):
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, description):
        """Add a new task"""
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'completed': False
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Task added: {description}")
    
    def list_tasks(self):
        """Display all tasks"""
        if not self.tasks:
            print("No tasks found!")
            return
        
        print("\n=== Your To-Do List ===")
        for task in self.tasks:
            status = "✓" if task['completed'] else "○"
            print(f"{task['id']}. [{status}] {task['description']}")
    
    def delete_task(self, task_id):
        """Delete a task by ID"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted = self.tasks.pop(i)
                self.save_tasks()
                print(f"✓ Deleted: {deleted['description']}")
                return
        print(f"Error: Task with ID {task_id} not found!")
    
    def mark_done(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_tasks()
                print(f"✓ Marked as done: {task['description']}")
                return
        print(f"Error: Task with ID {task_id} not found!")
    
    def run(self):
        """Main loop for the to-do list application"""
        while True:
            print("\n=== To-Do List Menu ===")
            print("1. Add task")
            print("2. List tasks")
            print("3. Mark task as done")
            print("4. Delete task")
            print("5. Exit")
            
            choice = input("\nChoose an option: ")
            
            if choice == '1':
                desc = input("Enter task description: ")
                self.add_task(desc)
            elif choice == '2':
                self.list_tasks()
            elif choice == '3':
                try:
                    task_id = int(input("Enter task ID to mark as done: "))
                    self.mark_done(task_id)
                except ValueError:
                    print("Invalid ID!")
            elif choice == '4':
                try:
                    task_id = int(input("Enter task ID to delete: "))
                    self.delete_task(task_id)
                except ValueError:
                    print("Invalid ID!")
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice!")


# Task 2: Data Scraper
def data_scraper():
    """Web scraper to extract data from websites"""
    
    print("\n=== Data Scraper ===")
    print("Example: Scraping quotes from quotes.toscrape.com")
    
    url = input("Enter URL to scrape (or press Enter for demo): ")
    if not url:
        url = "http://quotes.toscrape.com/"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Example: Scrape quotes
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')
        
        data = []
        for quote, author in zip(quotes, authors):
            data.append({
                'quote': quote.text,
                'author': author.text
            })
        
        # Save to CSV
        output_file = 'scraped_data.csv'
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if data:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        
        print(f"\n✓ Scraped {len(data)} items")
        print(f"✓ Data saved to {output_file}")
        
        # Display first 3 items
        for i, item in enumerate(data[:3], 1):
            print(f"\n{i}. {item}")
            
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Task 3: API Integration
def api_integration():
    """Fetch and display data from external API"""
    
    print("\n=== API Integration - Weather Data ===")
    
    # Using free API: Open-Meteo (no API key required)
    city = input("Enter city (or press Enter for Jakarta): ").strip()
    if not city:
        city = "Jakarta"
        latitude, longitude = -6.2088, 106.8456
    else:
        # For simplicity, using Jakarta coordinates
        latitude, longitude = -6.2088, 106.8456
    
    try:
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': True
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        weather = data.get('current_weather', {})
        
        print(f"\n=== Weather for {city} ===")
        print(f"Temperature: {weather.get('temperature', 'N/A')}°C")
        print(f"Wind Speed: {weather.get('windspeed', 'N/A')} km/h")
        print(f"Time: {weather.get('time', 'N/A')}")
        
    except requests.RequestException as e:
        print(f"Error: Failed to fetch data - {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# ============================================================================
# LEVEL 3 - ADVANCED
# ============================================================================

# Task 2: File Encryption/Decryption
class FileEncryptor:
    """Encrypt and decrypt files using Fernet encryption"""
    
    def __init__(self):
        self.key = None
    
    def generate_key(self):
        """Generate a new encryption key"""
        self.key = Fernet.generate_key()
        with open('encryption.key', 'wb') as key_file:
            key_file.write(self.key)
        print("✓ Encryption key generated and saved to 'encryption.key'")
    
    def load_key(self):
        """Load encryption key from file"""
        try:
            with open('encryption.key', 'rb') as key_file:
                self.key = key_file.read()
            print("✓ Encryption key loaded")
        except FileNotFoundError:
            print("Key file not found. Generating new key...")
            self.generate_key()
    
    def encrypt_file(self, filename):
        """Encrypt a file"""
        try:
            if not self.key:
                self.load_key()
            
            fernet = Fernet(self.key)
            
            with open(filename, 'rb') as file:
                original = file.read()
            
            encrypted = fernet.encrypt(original)
            
            encrypted_filename = f"{filename}.encrypted"
            with open(encrypted_filename, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)
            
            print(f"✓ File encrypted: {encrypted_filename}")
            
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found!")
        except Exception as e:
            print(f"Encryption error: {e}")
    
    def decrypt_file(self, filename):
        """Decrypt a file"""
        try:
            if not self.key:
                self.load_key()
            
            fernet = Fernet(self.key)
            
            with open(filename, 'rb') as encrypted_file:
                encrypted = encrypted_file.read()
            
            decrypted = fernet.decrypt(encrypted)
            
            decrypted_filename = filename.replace('.encrypted', '.decrypted')
            with open(decrypted_filename, 'wb') as decrypted_file:
                decrypted_file.write(decrypted)
            
            print(f"✓ File decrypted: {decrypted_filename}")
            
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found!")
        except Exception as e:
            print(f"Decryption error: {e}")
    
    def run(self):
        """Main loop for file encryption"""
        while True:
            print("\n=== File Encryption/Decryption ===")
            print("1. Generate new key")
            print("2. Encrypt file")
            print("3. Decrypt file")
            print("4. Exit")
            
            choice = input("\nChoose an option: ")
            
            if choice == '1':
                self.generate_key()
            elif choice == '2':
                filename = input("Enter filename to encrypt: ")
                self.encrypt_file(filename)
            elif choice == '3':
                filename = input("Enter filename to decrypt: ")
                self.decrypt_file(filename)
            elif choice == '4':
                break
            else:
                print("Invalid choice!")


# Task 3: N-Queens Problem
class NQueens:
    """Solve the N-Queens problem using backtracking"""
    
    def __init__(self, n):
        self.n = n
        self.solutions = []
    
    def is_safe(self, board, row, col):
        """Check if it's safe to place a queen at board[row][col]"""
        
        # Check column
        for i in range(row):
            if board[i][col] == 1:
                return False
        
        # Check upper left diagonal
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if board[i][j] == 1:
                return False
            i -= 1
            j -= 1
        
        # Check upper right diagonal
        i, j = row - 1, col + 1
        while i >= 0 and j < self.n:
            if board[i][j] == 1:
                return False
            i -= 1
            j += 1
        
        return True
    
    def solve(self, board, row):
        """Use backtracking to place queens"""
        
        if row >= self.n:
            # Found a solution
            self.solutions.append([row[:] for row in board])
            return True
        
        result = False
        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row][col] = 1
                result = self.solve(board, row + 1) or result
                board[row][col] = 0  # Backtrack
        
        return result
    
    def print_board(self, board):
        """Print the board"""
        for row in board:
            print(' '.join(['Q' if cell == 1 else '.' for cell in row]))
        print()
    
    def solve_n_queens(self):
        """Solve the N-Queens problem"""
        board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        
        print(f"\n=== Solving {self.n}-Queens Problem ===")
        self.solve(board, 0)
        
        print(f"\nFound {len(self.solutions)} solution(s)")
        
        if self.solutions:
            print("\nFirst solution:")
            self.print_board(self.solutions[0])
            
            if len(self.solutions) > 1:
                show_all = input("Show all solutions? (y/n): ")
                if show_all.lower() == 'y':
                    for i, solution in enumerate(self.solutions[1:], 2):
                        print(f"Solution {i}:")
                        self.print_board(solution)


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    """Main menu to run all projects"""
    
    while True:
        print("\n" + "="*60)
        print("PYTHON PROJECT COLLECTION")
        print("="*60)
        print("\nLEVEL 1 - BASIC")
        print("1. Simple Calculator")
        print("2. Number Guessing Game")
        print("3. Word Counter")
        print("\nLEVEL 2 - INTERMEDIATE")
        print("4. To-Do List Application")
        print("5. Data Scraper")
        print("6. API Integration")
        print("\nLEVEL 3 - ADVANCED")
        print("7. File Encryption/Decryption")
        print("8. N-Queens Problem")
        print("\n0. Exit")
        
        choice = input("\nSelect a project (0-8): ")
        
        if choice == '1':
            calculator()
        elif choice == '2':
            number_guessing_game()
        elif choice == '3':
            word_counter()
        elif choice == '4':
            todo = TodoList()
            todo.run()
        elif choice == '5':
            data_scraper()
        elif choice == '6':
            api_integration()
        elif choice == '7':
            encryptor = FileEncryptor()
            encryptor.run()
        elif choice == '8':
            try:
                n = int(input("Enter board size (e.g., 4 for 4x4): "))
                if n < 4:
                    print("Please enter a number >= 4")
                else:
                    solver = NQueens(n)
                    solver.solve_n_queens()
            except ValueError:
                print("Invalid input!")
        elif choice == '0':
            print("\nThank you for using Python Project Collection!")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()