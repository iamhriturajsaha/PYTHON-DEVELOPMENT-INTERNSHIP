# 🎯 Simple Quiz Game

# Features -
# 1. Multiple players can play one after another.
# 2. Each player gets random questions from a shared pool.
# 3. Once a question is asked, it is removed from the pool (no repetition).
# 4. A scoreboard keeps track of all players’ scores.
# 5. Final scoreboard is displayed at the end (ranked by score).

# Question Bank
import random
quiz_questions = [
    {
        "question": "What is the capital of France?",
        "options": ["A. Paris", "B. London", "C. Rome", "D. Berlin"],
        "answer": "A"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["A. Venus", "B. Mars", "C. Jupiter", "D. Saturn"],
        "answer": "B"
    },
    {
        "question": "Who developed the theory of relativity?",
        "options": ["A. Newton", "B. Tesla", "C. Einstein", "D. Galileo"],
        "answer": "C"
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["A. Elephant", "B. Blue Whale", "C. Giraffe", "D. Hippopotamus"],
        "answer": "B"
    },
    {
        "question": "Which language is used to write web pages?",
        "options": ["A. Python", "B. HTML", "C. Java", "D. C++"],
        "answer": "B"
    },
    {
        "question": "What is the chemical symbol for water?",
        "options": ["A. CO2", "B. H2O", "C. O2", "D. HO"],
        "answer": "B"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["A. Van Gogh", "B. Picasso", "C. Da Vinci", "D. Michelangelo"],
        "answer": "C"
    },
    {
        "question": "Which is the smallest prime number?",
        "options": ["A. 1", "B. 2", "C. 3", "D. 5"],
        "answer": "B"
    },
    {
        "question": "Which country is known as the Land of the Rising Sun?",
        "options": ["A. China", "B. Japan", "C. Korea", "D. Thailand"],
        "answer": "B"
    },
    {
        "question": "Which gas do plants absorb during photosynthesis?",
        "options": ["A. Oxygen", "B. Carbon Dioxide", "C. Nitrogen", "D. Hydrogen"],
        "answer": "B"
    },
    {
        "question": "Who was the first man to step on the moon?",
        "options": ["A. Neil Armstrong", "B. Buzz Aldrin", "C. Yuri Gagarin", "D. Michael Collins"],
        "answer": "A"
    },
    {
        "question": "Which ocean is the largest?",
        "options": ["A. Atlantic", "B. Indian", "C. Arctic", "D. Pacific"],
        "answer": "D"
    },
    {
        "question": "What is the capital of Australia?",
        "options": ["A. Sydney", "B. Melbourne", "C. Canberra", "D. Perth"],
        "answer": "C"
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["A. Charles Dickens", "B. William Shakespeare", "C. Mark Twain", "D. Jane Austen"],
        "answer": "B"
    },
    {
        "question": "Which is the hardest natural substance on Earth?",
        "options": ["A. Gold", "B. Diamond", "C. Iron", "D. Platinum"],
        "answer": "B"
    }
]
# Function to Run Quiz for a Single Player
def play_quiz(player_name, question_pool, num_questions=5):
    """
    Run the quiz for one player.
    Args:
        player_name (str): The name of the player.
        question_pool (list): Shared pool of available questions.
        num_questions (int): Number of questions to ask (default = 5).
    Returns:
        int: Final score of the player.
    """
    print(f"\n👤 Welcome, {player_name}! Let's start the quiz.\n")
    score = 0
    # Select random questions from the shared pool
    selected_questions = random.sample(question_pool, min(num_questions, len(question_pool)))
    for q in selected_questions:
        print(f"Q: {q['question']}")
        for option in q['options']:
            print(option)
        # Get player's answer
        answer = input("Your choice (A/B/C/D): ").strip().upper()
        # Validate and check answer
        if answer == q["answer"]:
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Wrong! The correct answer was: {q['answer']}\n")
        # Remove asked question so it won’t repeat for other players
        question_pool.remove(q)
    # Show player's final score
    print(f"🎯 {player_name}, your final score: {score}/{len(selected_questions)}\n")
    return score
# Main Program
def main():
    """
    Main function to manage the quiz game.
    Allows multiple players to play until question pool is exhausted.
    """
    question_pool = quiz_questions.copy()  # Shared pool for all players
    scoreboard = {}  # Dictionary to store player names and scores
    print("===== 🎮 Welcome to the Quiz Game! 🎮 =====")
    # Keep playing while there are questions left
    while question_pool:
        # Get player name
        player_name = input("\nEnter player name: ").strip()
        # Run quiz for the player
        score = play_quiz(player_name, question_pool)
        scoreboard[player_name] = score
        # If no questions remain, stop
        if not question_pool:
            print("\n⚠ No more questions left in the pool!")
            break
        # Ask if another player wants to join
        choice = input("Do you want another player to play? (yes/no): ").strip().lower()
        if choice != "yes":
            break
    # Display final scoreboard (ranked by score)
    print("\n===== 🏆 Final Scoreboard 🏆 =====")
    ranked_scores = sorted(scoreboard.items(), key=lambda x: x[1], reverse=True)
    for rank, (player, score) in enumerate(ranked_scores, start=1):
        print(f"{rank}. {player}: {score}")
    print("\n✅ Game Over! Thanks for playing.")
# Run the Game
if __name__ == "__main__":
    main()
