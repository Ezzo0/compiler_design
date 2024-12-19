class TopDownParser:
    def _init_(self):
        self.grammar = {}
        self.start_symbol = None

    def input_grammar(self):
        """
        Allows the user to input grammar rules dynamically.
        """
        print("Enter grammar rules in the format: NonTerminal -> productions.")
        print("Use a comma ',' to separate multiple productions. Type 'done' to finish.")
        self.grammar = {}
        while True:
            rule = input("Enter a rule (or 'done' to finish): ")
            if rule.lower() == 'done':
                break
            try:
                non_terminal, productions = rule.split("->")
                non_terminal = non_terminal.strip()
                productions = [p.strip() for p in productions.split(",")]
                if non_terminal in self.grammar:
                    self.grammar[non_terminal].extend(productions)
                else:
                    self.grammar[non_terminal] = productions
            except ValueError:
                print("Invalid format. Example: S -> aB, bC")

        self.start_symbol = input("Enter the start symbol: ").strip()

    def is_simple_grammar(self):
        """
        Checks if the entered grammar is a Simple Grammar.
        """
        if not self.grammar:
            print("No grammar rules have been entered.")
            return False

        for non_terminal, productions in self.grammar.items():
            for prod in productions:
                # Check if there are more than one non-terminal in a production
                if len([ch for ch in prod if ch.isupper()]) > 1:
                    print(f"The rule '{non_terminal} -> {prod}' is not simple (more than one Non-Terminal).")
                    return False

        print("The grammar is a Simple Grammar.")
        return True

    def parse(self, sequence):
        """
        Checks if a sequence is accepted by the grammar using a top-down approach.
        """
        def dfs(non_terminal, seq, pos):
            if pos == len(seq):
                return non_terminal == ""  # Only valid if the remaining rule is empty
            if non_terminal == "":
                return False

            current_symbol = non_terminal[0]
            rest = non_terminal[1:]

            if current_symbol.isupper():  # Non-Terminal
                if current_symbol not in self.grammar:
                    return False
                for production in self.grammar[current_symbol]:
                    if dfs(production + rest, seq, pos):
                        return True
            else:  # Terminal
                if pos < len(seq) and seq[pos] == current_symbol:
                    return dfs(rest, seq, pos + 1)
            return False

        return dfs(self.start_symbol, sequence, 0)

    def run(self):
        """
        Main user interface to interact with the parser.
        """
        while True:
            print("\n--- Main Menu ---")
            print("1. Input grammar rules")
            print("2. Check if the grammar is simple")
            print("3. Check a sequence")
            print("4. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.input_grammar()
            elif choice == "2":
                if self.is_simple_grammar():
                    print("The entered grammar is simple.")
                else:
                    print("The entered grammar is not simple.")
            elif choice == "3":
                if not self.grammar:
                    print("Please input grammar rules first.")
                    continue
                sequence = input("Enter the sequence to check: ").strip()
                if self.parse(sequence):
                    print(f"The sequence '{sequence}' is Accepted.")
                else:
                    print(f"The sequence '{sequence}' is Rejected.")
            elif choice == "4":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")

def main():
    parser = TopDownParser()
    parser.run()

if __name__ == "__main__":
    main()