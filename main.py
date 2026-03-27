import math
import csv
from collections import defaultdict
from colorama import Fore, Style, init

init(autoreset=True)

# =======================
# Stylish Banner
# =======================
def show_banner():
    print(Fore.CYAN + "=" * 70)
    print(Fore.GREEN + "   🔎 MARKOV PASSWORD STRENGTH ANALYZER 🔎")
    print(Fore.CYAN + "=" * 70)
    print(Fore.YELLOW + "   Built with ❤️ by " + Fore.MAGENTA + Style.BRIGHT + "ARIHANT")
    print(Fore.CYAN + "=" * 70)


# =======================
# Load CSV
# =======================
def load_passwords_from_csv(file_path):
    passwords = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    passwords.append(row[0].strip().lower())
    except FileNotFoundError:
        print(Fore.RED + "[ ERROR ] CSV file not found.")
        exit()

    return passwords


# =======================
# Train Model
# =======================
def train_model(password_list):
    model = defaultdict(lambda: defaultdict(int))
    for password in password_list:
        for i in range(len(password) - 1):
            model[password[i]][password[i + 1]] += 1
    return model


# =======================
# Markov Score
# =======================
def calculate_score(password, model):
    score = 0
    for i in range(len(password) - 1):
        char = password[i]
        next_char = password[i + 1]

        if char in model:
            total = sum(model[char].values())
            prob = model[char].get(next_char, 0) / total
            score += -math.log2(prob) if prob > 0 else 5
        else:
            score += 5

    return round(score, 2)


# =======================
# Strength
# =======================
def evaluate_strength(score):
    if score < 20:
        return Fore.RED + "WEAK ❌"
    elif score < 40:
        return Fore.YELLOW + "MODERATE ⚠"
    else:
        return Fore.GREEN + "STRONG ✅"


# =======================
# Entropy
# =======================
def calculate_entropy(password):
    charset = 0

    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(not c.isalnum() for c in password):
        charset += 32

    entropy = len(password) * math.log2(charset) if charset > 0 else 0
    return entropy


# =======================
# Format Time
# =======================
def format_time(seconds):
    if seconds < 1:
        return f"{seconds:.6f} seconds"
    elif seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    else:
        return f"{seconds/31536000:.2f} years"


# =======================
# Crack Time
# =======================
def estimate_crack_time(password, dataset):
    password_lower = password.lower()

    # Dataset check
    if password_lower in dataset:
        return Fore.RED + "0.000001 seconds (Instant - Common password)"

    # Pattern check
    patterns = ["123", "password", "qwerty", "abc", "admin"]
    for p in patterns:
        if p in password_lower:
            return Fore.YELLOW + "0.01 - 1 seconds (Common pattern)"

    entropy = calculate_entropy(password)

    guesses_per_second = 1e10
    total_combinations = 2 ** entropy
    seconds = total_combinations / guesses_per_second

    return Fore.GREEN + format_time(seconds)


# =======================
# Feedback
# =======================
def give_feedback(password):
    feedback = []

    if len(password) < 8:
        feedback.append("Increase password length (8+)")
    if password.islower() or password.isupper():
        feedback.append("Avoid single-case passwords")
    if password.isalpha():
        feedback.append("Add numbers & symbols")
    if password.isalnum():
        feedback.append("Include special characters")

    return feedback


# =======================
# Main Loop
# =======================
def main():
    show_banner()

    file_path = r"C:\Users\Shainee Singh\PycharmProjects\MPSA\common_passwords.csv"

    dataset = load_passwords_from_csv(file_path)
    print(Fore.CYAN + f"[ INFO ] Loaded {len(dataset)} passwords\n")

    model = train_model(dataset)

    while True:
        password = input(Fore.WHITE + "\nEnter password (or type 'quit' to exit): ")

        if password.lower() == "quit":
            print(Fore.CYAN + "\n[ SYSTEM ] Exiting... Stay secure! 🔐")
            break

        score = calculate_score(password, model)
        strength = evaluate_strength(score)
        crack_time = estimate_crack_time(password, dataset)

        print(Fore.CYAN + "\n[ RESULT ]")
        print(f"Score               : {score}")
        print(f"Strength            : {strength}")
        print(f"Estimated Crack Time: {crack_time}")

        feedback = give_feedback(password)

        if feedback:
            print(Fore.YELLOW + "\n[ SUGGESTIONS ]")
            for f in feedback:
                print(f"- {f}")
        else:
            print(Fore.GREEN + "\n[ ✔ ] Strong password")


if __name__ == "__main__":
    main()