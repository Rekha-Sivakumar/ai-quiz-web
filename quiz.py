import re
from ai_generator import AIGenerator
from pdf_handler import PDFHandler


class Quiz:

    def start_topic_quiz(self):
        topic = input("Enter topic: ")

        while True:
            questions = AIGenerator.generate_questions(topic)

            if not questions:
                print("❌ No questions generated!")
                return

            self.run_quiz(questions)

            if not self.ask_continue():
                break

    def start_pdf_quiz(self):
        path = input("Enter PDF path: ")
        content = PDFHandler.read_pdf(path)

        if not content:
            print("❌ Empty PDF!")
            return

        while True:
            questions = AIGenerator.generate_questions(content)

            if not questions:
                print("❌ No questions generated!")
                return

            self.run_quiz(questions)

            if not self.ask_continue():
                break

    def run_quiz(self, questions):
        score = 0

        for i, q in enumerate(questions, 1):
            print(f"\nQ{i}:")
            question_text = q['question']
            question_text = question_text.replace("'''", "\n")
            print(question_text)

            for idx, opt in enumerate(q['options'], 1):
                clean = opt[3:] if len(opt) > 2 and opt[1] == '.' else opt
                print(f"{idx}. {clean}")

            while True:
                user = input("Enter option (1-4 or A-D): ").upper()

                if user in ['1','2','3','4']:
                    index = int(user) - 1
                    break
                elif user in ['A','B','C','D']:
                    index = ord(user) - ord('A')
                    break
                else:
                    print("Invalid input!")

            selected = q['options'][index]

            sel_letter = re.findall(r"[A-D]", selected.upper())[0]
            ans_letter = re.findall(r"[A-D]", q['answer'].upper())[0]

            if sel_letter == ans_letter:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Wrong! Correct: {ans_letter}")

            print("💡", q['explanation'])

        print(f"\n🎯 Score: {score}/{len(questions)}")

    def ask_continue(self):
        return input("\nMore questions? (yes/no): ").lower() == "yes"